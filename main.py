import traceback
from doctest import UnexpectedException
from typing import List

from bullet import Bullet, colors, utils


class PurchaseItem(object):
    def __init__(self, option):
        self.price = option.p
        self.name = str(option)


def get_total_order_amount(order: List[PurchaseItem]):
    total_amount = sum(item.price for item in order)
    return total_amount


def get_service_charge(order: List[PurchaseItem]):
    total_amount = get_total_order_amount(order)
    service_charge_percentage = min((total_amount // 100) * 0.01, 0.20)
    service_charge = total_amount * service_charge_percentage
    return service_charge


class Option(object):
    def __init__(self, n=None, pu=None, p=None, d=None):
        self.p = p
        self.n = n
        self.pu = pu
        if d:
            self.n = d.get("name")
            self.p = d.get("price")
        if self.p is None:
            self.p = 0
        if self.n is None:
            raise AttributeError
        self.pu = self.pu if self.pu else "Rs."

    def __str__(self):
        return f"{str(self.n)} {str(self.pu) + ' ' + str(self.p) if self.p else ''}"

    def __len__(self):
        return len(self.__str__())


MCDONALDS_FOOD_OPTIONS = [
    Option(d={"name": "Veg Burger", "price": 115.00}),
    Option(d={"name": "Veg Wrap", "price": 130.00}),
    Option(d={"name": "Veg Happy Meal", "price": 215.00}),
    Option(d={"name": "Chicken Burger", "price": 175.00}),
    Option(d={"name": "Chicken Wrap", "price": 195.00}),
    Option(d={"name": "No, that's all", "price": 0.00}),
]

MCDONALDS_BEVERAGES_OPTIONS = [
    Option(d={"name": "Sprite (M)", "price": 115.00}),
    Option(d={"name": "Sprite (L)", "price": 130.00}),
    Option(d={"name": "Mango Smoothie", "price": 215.00}),
    Option(d={"name": "Chocolate Smoothie", "price": 175.00}),
    Option(d={"name": "Chocolate Smoothie w/ Icecream", "price": 195.00}),
    Option(d={"name": "No, that's all", "price": 0.00}),
]


def get_option_from_result(result, options):
    for option in options:
        if str(option) == result:
            return option

    raise UnexpectedException


def print_order(order):
    print()

    try:
        total_amount = get_total_order_amount(order)
    except:
        traceback.print_exc()
        total_amount = "ERROR"

    service_charge = "ERROR"
    if total_amount != "ERROR":
        try:
            service_charge = get_service_charge(order)
        except:
            traceback.print_exc()
            service_charge = "ERROR"

    utils.cprint(
        "Final Order", color=colors.foreground["green"], on=colors.background["yellow"]
    )
    for i, item in enumerate(order):
        utils.cprint(
            f"{i + 1}. {item.name}",
            color=colors.foreground["yellow"],
            on=colors.background["green"],
        )

    utils.cprint(
        f"Order Amount: {str(total_amount)}",
        color=colors.foreground["green"],
        on=colors.background["yellow"],
    )
    utils.cprint(
        f"Service Charge: {str(service_charge)}",
        color=colors.foreground["green"],
        on=colors.background["yellow"],
    )
    utils.cprint(
        f"Final Amount: {str(total_amount + service_charge) if isinstance(total_amount, (int, float)) and isinstance(service_charge, (int, float)) else 'ERROR'}",
        color=colors.foreground["green"],
        on=colors.background["yellow"],
    )


def add_item_to_order(order, options, prompt):
    while True:
        option_strings = list(map(lambda x: str(x), options))
        bullet = Bullet(prompt=prompt, choices=option_strings, bullet="=> ")
        result = bullet.launch()
        utils.clearConsoleUp(7)
        option = get_option_from_result(result, options)
        if result == str(options[-1]):
            break
        order.append(PurchaseItem(option))
        utils.cprint(
            f"{result} is added to your order", on=colors.background["green"], end="\n"
        )


def main():
    print()
    utils.cprint(
        "Welcome to McDonalds on your shell :)",
        color=colors.foreground["blue"],
        on=colors.background["white"],
    )
    utils.cprint(
        "Here you can place your order        ",
        color=colors.foreground["blue"],
        on=colors.background["white"],
    )
    utils.cprint(
        "And then we will show you your bill  ",
        color=colors.foreground["blue"],
        on=colors.background["white"],
    )
    print()
    order = []

    add_item_to_order(order, MCDONALDS_FOOD_OPTIONS, "Add a food item")
    add_item_to_order(order, MCDONALDS_BEVERAGES_OPTIONS, "Add a beverage")

    utils.clearConsoleUp(1)
    print()
    print_order(order)


if __name__ == "__main__":
    main()
