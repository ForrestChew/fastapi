from app.calcs import add, sub, mult, div, BankAccount, InsufficientFunds
import pytest


@pytest.fixture
def zero_bank_account():
    return BankAccount()


@pytest.fixture
def bank_account():
    return BankAccount(50)


@pytest.mark.parametrize(
    "num1, num2, expected", [(3, 5, 8), (10, 10, 20), (100, 1, 101)]
)
def test_add(num1, num2, expected):
    res = add(num1, num2)
    assert res == expected


@pytest.mark.parametrize("num1, num2, expected", [(3, 5, -2), (10, 10, 0), (75, 1, 74)])
def test_sub(num1, num2, expected):
    res = sub(num1, num2)
    assert res == expected


@pytest.mark.parametrize(
    "num1, num2, expected", [(1, 1, 1), (2, 20, 40), (100, 9, 900)]
)
def test_mult(num1, num2, expected):
    res = mult(num1, num2)
    assert res == expected


@pytest.mark.parametrize(
    "num1, num2, expected", [(1, 2, 0.5), (20, 2, 10), (100, 5, 20)]
)
def test_div(num1, num2, expected):
    res = div(num1, num2)
    assert res == expected


def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50


def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0


def test_Deposit(zero_bank_account):
    zero_bank_account.deposit(50)
    assert zero_bank_account.balance == 50


def test_withdraw():
    bank_account = BankAccount(50)
    bank_account.withdraw(25)
    assert bank_account.balance == 25


def test_collect_interest():
    bank_account = BankAccount(10)
    bank_account.collect_interest()
    assert bank_account.balance == 11


@pytest.mark.parametrize(
    "deposit_amt, withdraw_amt, expected", [(20, 10, 10), (20, 2, 18), (100, 100, 0)]
)
def test_bank_tx(zero_bank_account, deposit_amt, withdraw_amt, expected):
    zero_bank_account.deposit(deposit_amt)
    zero_bank_account.withdraw(withdraw_amt)
    assert zero_bank_account.balance == expected


def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(100)
