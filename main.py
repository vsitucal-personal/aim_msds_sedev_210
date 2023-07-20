import os
import operator

WELCOME_MESSAGE = "Welcome to Tech Mart Management System What do you like to do?"
CHOICES = """1 - Add Product Inventory
2 - Update Product Quantity
3 - Remove a product from inventory
4 - Display Inventory Status
5 - Exit"""
INVALID_SELECTION_MESSAGE = "NOT IN CHOICES PICK AGAIN"
EXCEPTION_OCCURRED = "EXCEPTION OCCURRED BAD INPUT"
SUM = ["add", "+", operator.add]
DIFF = ["minus", "-", operator.sub]
OPERATION = SUM + DIFF


class TechMartInventory:
    def __init__(self):

        self.__techmart_inventory = {}
        self.__trigger_exit = True
        self.__menu_switcher = {
            "1": self.add_product,
            "2": self.update_product_qty,
            "3": self.remove_product,
            "4": self.display_inventory_status,
            "5": self.exit_tech_mart,
        }

    @staticmethod
    def clrscr():
        os.system('clear')

    @staticmethod
    def click_to_continue():
        input("Click any button to continue...")

    def restock_alert_check(self):
        for _, value in self.__techmart_inventory.items():
            items_to_restock = 0
            # zero stock items alert
            if value.get("qty") == 0:
                print(f"Restock needed for product_id: {value.get('product_id')} - {value.get('product_name')}"
                      f"qty remaining = {value.get('qty')}")
                items_to_restock += 1
            # TODO: THRESHOLD ALERTS

            if items_to_restock > 0:
                self.click_to_continue()

    def show_inventory(self):
        print("Inventory:")
        for _, value in self.__techmart_inventory.items():
            print(value)

    def add_product(self):
        self.clrscr()
        product_name = input("Product Name:").lower()
        qty = int(input("Qty:"))
        assert qty > 0
        future_inv_size = len(self.__techmart_inventory) + 1
        product = {
            "product_id": future_inv_size,
            "product_name": product_name,
            "qty": qty
        }
        self.__techmart_inventory[future_inv_size] = product
        self.clrscr()
        print(product)
        self.click_to_continue()

    def update_product_qty(self):
        self.clrscr()
        product_count = len(self.__techmart_inventory)
        print(f"Techmart inventory has {product_count} products")
        if product_count > 0:
            self.show_inventory()
            self.click_to_continue()
            to_update = int(input("product_id to update:"))
            item_updated = self.__techmart_inventory.get(to_update)
            if item_updated is not None:
                operation_to_do = input("Do you want to add/minus from qty? [add/minus/+/-] input:")
                assert operation_to_do in OPERATION
                if operation_to_do in SUM:
                    operators = SUM
                else:
                    operators = DIFF
                qty_to_op = int(input(f"Input qty to {operators[0]}:"))
                current_qty = item_updated.get("qty")
                resultant = operators[2](current_qty, qty_to_op)
                if not resultant >= 0:
                    raise AssertionError(f"You can't subtract more than {current_qty}")
                self.__techmart_inventory[to_update]["qty"] = resultant
                item_updated["qty"] = resultant
                print(f"Updated: {item_updated}")
                self.click_to_continue()
            else:
                print("product_id does not exist")
                self.click_to_continue()
        else:
            self.click_to_continue()

    def remove_product(self):
        self.clrscr()
        product_count = len(self.__techmart_inventory)
        print(f"Techmart inventory has {product_count} products")
        if product_count > 0:
            self.show_inventory()
            self.click_to_continue()
            to_remove = int(input("product_id to remove:"))
            item_removed = self.__techmart_inventory.get(to_remove)
            if item_removed is not None:
                self.__techmart_inventory.pop(to_remove)
                recalibrate_id_index = 1
                for k, _ in self.__techmart_inventory.items():
                    self.__techmart_inventory[k]["product_id"] = recalibrate_id_index
                    recalibrate_id_index += 1
                print(f"removed {item_removed}")
            else:
                print("product_id does not exist")
                self.click_to_continue()
        else:
            self.click_to_continue()

    def display_inventory_status(self):
        self.clrscr()
        product_count = len(self.__techmart_inventory)
        print(f"Techmart inventory has {product_count} products")
        if product_count > 0:
            self.click_to_continue()
            self.show_inventory()
        self.click_to_continue()

    def exit_tech_mart(self):
        self.clrscr()
        exit()

    def main(self):
        print(WELCOME_MESSAGE)
        while self.__trigger_exit:
            print(CHOICES)
            input_choice = input("What do you want to do: ")
            choice_method = self.__menu_switcher.get(input_choice)

            if choice_method:
                try:
                    choice_method()
                except Exception as e:
                    print(e)
                    print(EXCEPTION_OCCURRED)
                    self.click_to_continue()
                self.clrscr()
                self.restock_alert_check()
            else:
                self.clrscr()
                print(INVALID_SELECTION_MESSAGE)
                self.click_to_continue()
                self.restock_alert_check()


tech_mart = TechMartInventory()
tech_mart.main()
