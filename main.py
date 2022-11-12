# main class

import asyncio
import display
import operations as ops
import display as dis
from inventory import Inventory as Inv


async def full_order_process(io: Inv):
    raw_order_dct = ops.place_an_order()
    order_dct = await ops.get_updated_order_dct(io, raw_order_dct)
    task_get_price_dct = \
        asyncio.create_task(ops.get_items_names_and_prices_dct(io, order_dct))
    names_prices_dct = await task_get_price_dct
    summary = ops.get_order_summary(order_dct, names_prices_dct)
    dis.display_summary(summary, names_prices_dct)


async def main():
    # create inventory object io and catalogue
    io = Inv()
    catalogue = io.catalogue
    # display welcome message and catalogue
    display.welcome_message()
    display.display_catalogue(catalogue)
    # start main loop
    while True:
        await full_order_process(io)
        while True:
            another_order = input('Woud you like to make another order? (yes/no): ')
            if another_order == 'yes' or another_order == 'no':
                break
            else:
                print('Please enter yes/no')
        if another_order == 'no':
            print('Good bye!')
            quit()
        print()


if __name__ == "__main__":
    asyncio.run(main())
