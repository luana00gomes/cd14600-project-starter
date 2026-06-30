import unittest
from transaction.transaction_strategy import IncomeStrategy, ExpenseStrategy
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory
from balance.balance import Balance


class TestTransactionStrategy(unittest.TestCase):

    def test_income_strategy_adds_amount(self):
        strategy = IncomeStrategy()
        self.assertEqual(strategy.apply(100, 50), 150)

    def test_income_strategy_from_zero(self):
        strategy = IncomeStrategy()
        self.assertEqual(strategy.apply(0, 200), 200)

    def test_expense_strategy_subtracts_amount(self):
        strategy = ExpenseStrategy()
        self.assertEqual(strategy.apply(100, 40), 60)

    def test_expense_strategy_can_go_negative(self):
        strategy = ExpenseStrategy()
        self.assertEqual(strategy.apply(30, 50), -20)

    def test_balance_uses_income_strategy(self):
        balance = Balance.get_instance()
        balance.reset()
        balance.apply_transaction(Transaction(100, TransactionCategory.INCOME))
        self.assertEqual(balance.get_balance(), 100)

    def test_balance_uses_expense_strategy(self):
        balance = Balance.get_instance()
        balance.reset()
        balance.apply_transaction(Transaction(40, TransactionCategory.EXPENSE))
        self.assertEqual(balance.get_balance(), -40)

    def test_balance_raises_for_unknown_category(self):
        balance = Balance.get_instance()
        balance.reset()

        class UnknownCategory:
            pass

        t = Transaction(100, UnknownCategory())
        with self.assertRaises(ValueError):
            balance.apply_transaction(t)


if __name__ == "__main__":
    unittest.main()
