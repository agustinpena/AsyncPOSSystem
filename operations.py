# Operations module. Contains methods to
# interact with the user

from inventory import Inventory as Inv

INITIAL_MESSAGE: str = 'Please enter the item number that you ' \
                        'would like to add to your order.\n' \
                        'Enter q to complete your order.'


def _verify_value(string: str):
    if not(string.isdigit()):
        return 'Please enter a valid item id'
    num = int(string)
    if num > 20:
        return 'Please enter an id number below 21'
    return 'True'


def _classify_types(order_dct: dict, prices_dct: dict):
    # returns the number of possible combos and a 'types dict',
    # in the form: {'burguers':[], 'sides':[], 'drinks':[]}
    # list values are sorted by price in descending order
    classified_items = {'burgers': [], 'sides': [], 'drinks': []}
    # distribute ids in the lists
    for n in order_dct:
        item_type = 'drinks'
        if n < 7:
            item_type = 'burgers'
        if 6 < n < 12:
            item_type = 'sides'
        classified_items[item_type] += order_dct[n] * [n]
    # order the lists by item price, in ascending order
    for item_type in classified_items:
        classified_items[item_type].sort(key=lambda id_num: prices_dct[id_num])
    # get number of combos
    number_of_combos = min([len(x) for x in classified_items.values()])
    return number_of_combos, classified_items


def _create_a_combo(types_dct: dict):
    # funct returns a combo list and updated types_dct.
    combo = []
    # verify there are non-empty combos
    if 0 in [len(n) for n in types_dct.values()]:
        return combo, types_dct
    # extract one combo
    for item_type in types_dct:
        ids_lst = types_dct[item_type]
        max_price_id = ids_lst[-1]
        combo.append(max_price_id)
        ids_lst.remove(max_price_id)
    return combo, types_dct


def place_an_order():
    # outputs dict with item ids and their ordered amounts
    print(INITIAL_MESSAGE)
    order_dct = {}
    while (current_item_str := input('Enter an item id number: ')) != 'q':
        # validates current_item_str
        verify = _verify_value(current_item_str)
        if verify != 'True':
            print(verify)
            continue
        current_item_id = int(current_item_str)
        # populates 'order_dct'
        if current_item_id not in order_dct:
            order_dct[current_item_id] = 0
        order_dct[current_item_id] += 1
    # returns dictionary
    print('Placing order...')
    print()
    return order_dct


async def get_items_names_and_prices_dct(io: Inv, ids_dct: dict):
    # returns a dict in format {'id_num': ['item_name', 'price']}
    id_name_and_price_dct = {}
    items = {7: 'Fries', 8: 'Fries', 9: 'Fries', 10: 'Caesar Salad', 11: 'Caesar Salad',
             12: 'Coke', 13: 'Coke', 14: 'Coke', 15: 'Ginger Ale', 16: 'Ginger Ale',
             17: 'Ginger Ale', 18: 'Chocolate Milk Shake', 19: 'Chocolate Milk Shake',
             20: 'Chocolate Milk Shake'}
    for item_id in ids_dct:
        item_info = await io.get_item(item_id)
        if 1 <= item_id <= 6:
            item_name = item_info['name']
        else:
            item_name = item_info['size'] + ' ' + items[item_id]
        id_name_and_price_dct[item_id] = [item_name, item_info['price']]
    return id_name_and_price_dct


async def get_updated_order_dct(io: Inv, order_dct: dict):
    new_order_dct = {k: 0 for k in order_dct}
    for item_id in order_dct:
        n = order_dct[item_id]
        for _ in range(n):
            item_stock = await io.get_stock(item_id)
            if item_stock > 0:
                new_order_dct[item_id] += 1
                await io.decrement_stock(item_id)
            else:
                print(f'No stock left for ordered item {item_id}')
                print('It has been removed from your order')
                print('-'*30)

    return new_order_dct


def get_order_summary(order_dct: dict, names_prices_dct: dict):
    # returns a list with ordered combos and items as order_summary_lst
    prices_dct = {id_num: names_prices_dct[id_num][1] for id_num in order_dct}
    order_summary_lst = []
    num_of_combos, types_dct = _classify_types(order_dct, prices_dct)
    # add all combos, if any
    if num_of_combos > 0:
        current_types_dct = types_dct
        for _ in range(num_of_combos):
            current_combo, current_types_dict = _create_a_combo(current_types_dct)
            order_summary_lst.append(current_combo)
    # add remaining items
    for id_lst in types_dct.values():
        if len(id_lst) == 0:
            continue
        for ide in id_lst:
            order_summary_lst.append(ide)
    return order_summary_lst
