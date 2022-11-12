# display module; contains methods for
# displaying information to the user


def display_catalogue(catalogue: dict):
    burgers = catalogue["Burgers"]
    sides = catalogue["Sides"]
    drinks = catalogue["Drinks"]

    print("--------- Burgers -----------\n")
    for burger in burgers:
        item_id = burger["id"]
        name = burger["name"]
        price = burger["price"]
        print(f"{item_id}. {name} ${price}")

    print("\n---------- Sides ------------")
    for side in sides:
        sizes = sides[side]

        print(f"\n{side}")
        for size in sizes:
            item_id = size["id"]
            size_name = size["size"]
            price = size["price"]
            print(f"{item_id}. {size_name} ${price}")

    print("\n---------- Drinks ------------")
    for beverage in drinks:
        sizes = drinks[beverage]

        print(f"\n{beverage}")
        for size in sizes:
            item_id = size["id"]
            size_name = size["size"]
            price = size["price"]
            print(f"{item_id}. {size_name} ${price}")

    print("\n------------------------------\n")


def welcome_message():
    print('Welcome to the HungryGeek Burger Bar!')
    print('Loading catalogue...')


def _display_a_combo(combo_lst: list, names_prices_dct: dict):
    total = round(sum([names_prices_dct[item_id][1] for item_id in combo_lst]), 2)
    print(f'${total} Burger Combo')
    for item_id in combo_lst:
        print('  ' + names_prices_dct[item_id][0])
    return total


def display_summary(summary_lst: list, names_prices_dct: dict):
    if not summary_lst:
        return
    subtotal: float = 0.0
    print('Here is a summary of your order:')
    print()
    for element in summary_lst:
        if type(element) == list:
            combo_total = _display_a_combo(element, names_prices_dct)
            subtotal += combo_total
        else:
            item_price = names_prices_dct[element][1]
            subtotal += item_price
            name = names_prices_dct[element][0]
            price = '$' + str(item_price)
            print(price, name)
    subtotal = round(subtotal, 2)
    tax = round(subtotal * 0.05, 2)
    total = round(subtotal + tax, 2)
    print()
    print(f'Subtotal: ${subtotal}')
    print(f'Tax: ${tax}')
    print(f'Total: ${total}')
    while True:
        purchase = input(f'Would you like to purchase this order for ${total}? (yes/no): ')
        if purchase == 'yes':
            message = 'Thank you for your order!'
            break
        elif purchase == 'no':
            message = 'No problem, please come again!'
            break
        else:
            print('Please enter yes/no')
    print(message)
