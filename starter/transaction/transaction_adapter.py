# transaction_adapter.py

from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory

class TransactionAdapter:
    def __init__(self, external_transaction):
        self.external_transaction = external_transaction

    def to_transaction(self):
        """Convert an external transaction to a standard Transaction."""
        category = (
            TransactionCategory.INCOME
            if self.external_transaction.typ == "income"
            else TransactionCategory.EXPENSE
        )
        return Transaction(self.external_transaction.amount, category)
