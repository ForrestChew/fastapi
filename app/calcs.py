from tracemalloc import start


def add(a: int, b: int) -> int:
    return a + b


def sub(a: int, b: int) -> int:
    return a - b


def mult(a: int, b: int) -> int:
    return a * b


def div(a: int, b: int) -> int:
    return a / b


class InsufficientFunds(Exception):
    pass


class BankAccount:
    def __init__(self, starting_balance=0):
        self.balance = starting_balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFunds("not enough dollars")
        self.balance -= amount

    def collect_interest(self):
        self.balance *= 1.1
