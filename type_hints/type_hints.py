import os
import typing

TIP_DEFAULT = 0.22


def greeting(name: str) -> str:
    salutation: str = "Bonjour"
    return salutation + ' ' + name


def simple_test():
    greeting("Mon Cheri")


def split_meal_price(total: float, count: int, tip: float = TIP_DEFAULT) -> float:
    price_with_tip = total * (1.0 + tip)
    split_price = price_with_tip / count
    return split_price


def test_split_complex() -> None:
    price: float = float(input("What was the price of the meal?"))
    count: int = int(input("How many diners in you group?"))

    tip: float = TIP_DEFAULT
    tip_str: str = input(f"Optional tip fraction (hit Enter if {TIP_DEFAULT} is acceptable)?")
    if len(tip_str.strip()) != 0:
        tip = float(tip_str)

    split_price = split_meal_price(price, count, tip)
    print(f"Price per person for meal is {split_price}")


# def test_split_complex_bad():
#    split_meal_price()  // make one of inputs a string and then see it fail?


if __name__ == "__main__":

    simple_test()

    test_split_complex()

    pass
