"""
The openedx_ledger python API.
"""
from django.db.transaction import atomic

from openedx_ledger import models


def create_transaction(
    ledger, quantity, idempotency_key, lms_user_id=None, content_key=None, subsidy_access_policy_uuid=None, **metadata
):
    """
    Create a transaction.

    Should throw an exception when transaction would exceed balance of the ledger.
    Locking and DB transactions?
    (course id, ledger, user) are unique.
    Or support an idempotency key.
    """
    # Note that the default isolation level for MySQL provided by Django is `repeatable read`.
    # Therefore...this is good.  Because reasons.  TODO: better explanation.
    with atomic(durable=True):
        balance = ledger.balance()
        if (quantity < 0) and ((balance + quantity) < 0):
            # TODO: we definitely have to revisit this logic later to implement ADR 0002.
            raise Exception("d'oh!")  # pylint: disable=broad-exception-raised

        transaction, _ = models.Transaction.objects.get_or_create(
            ledger=ledger,
            idempotency_key=idempotency_key,
            defaults={
                "quantity": quantity,
                "content_key": content_key,
                "lms_user_id": lms_user_id,
                "subsidy_access_policy_uuid": subsidy_access_policy_uuid,
                "metadata": metadata,
            },
        )
        return transaction


def reverse_full_transaction(transaction, idempotency_key, **metadata):
    """
    Reverse a transaction, in full.

    Idempotency of reversals - reversing the same transaction twice
    produces the same output and has no side effect on the second invocation.
    Support idempotency key here, too.
    """
    with atomic(durable=True):
        # select the transaction and any reversals
        # if there is a reversal: return, no work to do here
        # if not, write a reversal for the transaction
        transaction.refresh_from_db()
        reversal, _ = models.Reversal.objects.get_or_create(
            transaction=transaction,
            idempotency_key=idempotency_key,
            defaults={
                'quantity': transaction.quantity * -1,
                'metadata': metadata,
            },
        )
        return reversal


def create_ledger(unit, idempotency_key, **metadata):
    """
    Idempotency key here, too.
    """
    ledger, _ = models.Ledger.objects.get_or_create(
        unit=unit,
        idempotency_key=idempotency_key,
        metadata=metadata,
    )
    return ledger


def update_ledger(ledger, **metadata):  # pylint: disable=unused-argument
    """
    TODO.
    """
