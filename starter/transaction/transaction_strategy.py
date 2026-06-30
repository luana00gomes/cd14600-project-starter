# transaction_strategy.py


class ITransactionStrategy:
    """Interface for applying a transaction amount to a running balance."""

    def apply(self, current_balance, amount):
        raise NotImplementedError("Subclasses must implement apply method.")


class IncomeStrategy(ITransactionStrategy):
    """Adds the amount to the balance."""

    def apply(self, current_balance, amount):
        return current_balance + amount


class ExpenseStrategy(ITransactionStrategy):
    """Subtracts the amount from the balance."""

    def apply(self, current_balance, amount):
        return current_balance - amount
