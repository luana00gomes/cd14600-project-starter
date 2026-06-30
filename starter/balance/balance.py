# balance.py

from transaction.transaction_category import TransactionCategory
from transaction.transaction_strategy import IncomeStrategy, ExpenseStrategy

_STRATEGY_MAP = {
    TransactionCategory.INCOME: IncomeStrategy(),
    TransactionCategory.EXPENSE: ExpenseStrategy(),
}


class Balance:
    """Singleton to track the balance."""

    _instance = None

    def __init__(self):
        self._net_balance = 0.0
        self._observers = []

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def reset(self):
        """Reset the net balance to zero and clear all observers."""
        self._net_balance = 0.0
        self._observers = []

    def register_observer(self, observer):
        self._observers.append(observer)

    def _notify_observers(self, transaction):
        for observer in self._observers:
            observer.update(self._net_balance, transaction)

    def add_income(self, amount):
        """Add income to the balance."""
        self._net_balance += amount

    def add_expense(self, amount):
        """Subtract expense from the balance."""
        self._net_balance -= amount

    def apply_transaction(self, transaction):
        """Apply a Transaction object to update the balance using the Strategy pattern."""
        strategy = _STRATEGY_MAP.get(transaction.category)
        if strategy is None:
            raise ValueError(f"Unknown transaction category: {transaction.category}")
        self._net_balance = strategy.apply(self._net_balance, transaction.amount)
        self._notify_observers(transaction)

    def get_balance(self):
        """Get the current net balance."""
        return self._net_balance

    def summary(self):
        """Return a summary string of the net balance."""
        return f"Net Balance: ${self._net_balance:.2f}"
