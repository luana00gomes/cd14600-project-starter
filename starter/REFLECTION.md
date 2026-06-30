# Design Patterns Reflection

## Patterns Used

### 1. Singleton — `Balance`

**Where:** `balance/balance.py`

The `Balance` class uses a class-level `_instance` variable and a `get_instance()` factory method to guarantee that only one balance object exists for the entire application lifetime. Direct instantiation via `Balance()` still works internally, but all external callers use `get_instance()`.

**How it improved the design:** Financial state is naturally global — there is one real account balance. The Singleton enforces this invariant at the code level rather than relying on discipline across call sites. Any module that needs the balance calls `Balance.get_instance()` and is guaranteed to see the same state as every other module.

**Trade-off:** Singletons share state across tests, so each test's `setUp` must call `balance.reset()` to start from a clean slate. Forgetting this leads to flaky tests with order-dependent failures.

---

### 2. Adapter — `TransactionAdapter`

**Where:** `transaction/transaction_adapter.py`

`ExternalFreelanceIncome` comes from a third-party system and has a different interface (`typ`, `invoice_id`, `description`) than the app's internal `Transaction` (`amount`, `category`). `TransactionAdapter` wraps the external object and exposes a `to_transaction()` method that returns a native `Transaction`.

**How it improved the design:** The rest of the application never needs to know that freelance income originates from an external system. New external sources (bank feeds, payroll APIs) can each get their own adapter without touching `Balance`, `Transaction`, or any business logic.

**Trade-off:** Every new external format requires a new adapter class. For very simple integrations this is extra ceremony, but it pays off quickly as the number of sources grows.

---

### 3. Observer — `LowBalanceAlertObserver` / `PrintObserver`

**Where:** `balance/balance_observer.py`, wired in `balance/balance.py`

`Balance` maintains a list of `IBalanceObserver` instances. After every `apply_transaction()` call it iterates the list and calls `observer.update(balance, transaction)` on each. `PrintObserver` logs every change; `LowBalanceAlertObserver` sets `alert_triggered` and prints a warning when the balance falls below a threshold.

**How it improved the design:** New reactions to balance changes (push notifications, database writes, UI refreshes) can be added by implementing `IBalanceObserver` and registering it — without modifying `Balance` at all. This keeps the core accounting logic free of notification concerns.

**Trade-off:** Observers run synchronously in sequence. A slow or failing observer blocks the transaction loop. For a production app, an async event queue would be preferable.

---

### 4. Strategy — `IncomeStrategy` / `ExpenseStrategy`

**Where:** `transaction/transaction_strategy.py`, used in `balance/balance.py`

`Balance.apply_transaction()` looks up the correct `ITransactionStrategy` from a `_STRATEGY_MAP` keyed by `TransactionCategory`. Each strategy implements `apply(current_balance, amount) -> new_balance`. Currently `IncomeStrategy` adds and `ExpenseStrategy` subtracts.

**Why this pattern:** The original skeleton had an `if/elif` block inside `apply_transaction`. Adding a new category (e.g. `TRANSFER`, `TAX_WITHHOLDING`) would require editing `Balance` every time — a violation of the Open/Closed Principle. With the Strategy map, a new category only requires a new strategy class and one entry in the map.

**How it improved the design:** The calculation logic is isolated and independently testable. `IncomeStrategy` and `ExpenseStrategy` are pure functions wrapped in objects — trivial to unit-test without instantiating `Balance` at all. It also makes it straightforward to add variants like a `TaxedIncomeStrategy` that applies a withholding rate before crediting the balance.

**Trade-off:** For just two categories the abstraction feels heavyweight. The payoff becomes clear as soon as a third category appears.
