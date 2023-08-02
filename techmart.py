import os
import csv
import uuid
import math
import numpy
from datetime import datetime
from typing import Optional
from decimal import Decimal
from math import floor


class TechMartConstants:
    WELCOME_MESSAGE = "Welcome to Tech Mart Management System!!!"
    MAIN_CHOICES = "1 - Add Product Inventory\n2 - Update Product Quantity\n3 - Remove a product from inventory\n4 - " \
                   "Display Inventory\n5 - Recover Deleted Product\n6 - Product Restock Level Alert\n" \
                   "7 - Show TechMart Insights\n8 - Exit "
    INVENTORY_HISTORY_CHOICES = "1 - Display Active Product Inventory\n2 - Display Inactive Product Inventory\n3 - " \
                                "Display Product Transaction History\n4 - Return to home"
    UPDATE_PRODUCT_CHOICES = "1 - Add Product Quantity Transaction\n2 - Remove Product Quantity Transaction\n3 - " \
                             "Return to home "
    INVALID_SELECTION_MESSAGE = "NOT IN CHOICES PICK AGAIN"
    EXCEPTION_OCCURRED = "EXCEPTION OCCURRED BAD INPUT"
    # inventory headers and padding
    INVENTORY_HEADERS = [
        ("Product ID", 36), ("Product Name", 16), ("Quantity", 8), ("Threshold1", 10), ("Threshold2", 10),
        ("Last Updated", 26),
    ]
    # history headers and padding
    HISTORY_HEADERS = [
        ("Transaction ID", 36), ("Transaction Type", 16), ("Start Qty", 9), ("Add", 9), ("Remove", 9), ("End Qty", 9),
        ("Unit Price", 11), ("Total Value", 11), ("Timestamp", 26)
    ]
    INVENTORY_FILE_NAME = "tech_mart_inventory.csv"
    REMOVED_INVENTORY_FILE_NAME = "inactive_tech_mart_inventory.csv"

    # Float Operations
    DEFAULT_STEP_VALUE = 0.00000001
    PRECISION = 8


class HelperFunctions:
    @staticmethod
    def clrscr():
        if os.name == 'nt':  # Check if the operating system is Windows
            os.system('cls')
        else:  # Assume Unix-based system (Linux, macOS, etc.)
            os.system('clear')

    @staticmethod
    def click_to_continue():
        input("Click any button to continue...")

    @staticmethod
    def read_from_file(inp_filename: str) -> list:
        try:
            with open(inp_filename, "r", newline="") as file:
                reader = csv.reader(file)
                data = list(reader)
        except IOError:
            # probably no inp file
            data = []
        return data

    def func_float_multiply(self, multiplicand: float, multiplier: float, step: Optional[float] = None) -> float:
        if step is None:
            step = TechMartConstants.DEFAULT_STEP_VALUE
        return self.func_adjust_value_to_step(
            float(Decimal(str(multiplicand)) * Decimal(str(multiplier))),
            step

        )

    @staticmethod
    def func_floor_to_precision(num: float, precision: int = TechMartConstants.PRECISION) -> float:
        """
        Returns a float value rounded down to a specific number of decimal places

        :param num: float
        :param precision: number of decimal places
        :return: float
        """
        result = num
        num_dp = Decimal(str(num)).as_tuple().exponent * -1

        if num_dp > precision:
            factor = 10 ** precision
            result = floor(num * factor) / factor
        return result

    @staticmethod
    def func_get_step_precision(step: float) -> int:
        """
        Returns the precision value for the step value

        :param step: original step value
        :return: int
        """
        if step % 1 == 0:
            # Drop excess dp
            step = int(step)

        step_dp = Decimal(str(step)).as_tuple().exponent * -1
        return step_dp

    def func_adjust_value_to_step(self, input_val: float, step: float) -> float:
        if step % 1 == 0:
            # Drop excess dp
            step = int(step)
        return self.func_floor_to_precision(
            input_val,
            self.func_get_step_precision(step)
        )

    @staticmethod
    def touch_file(out_filename: str):
        if not os.path.exists(out_filename.split("/")[0]):
            os.mkdir(out_filename.split("/")[0])
        open(out_filename, "a", newline="").close()

    @staticmethod
    def write_to_file(inp_list: list, out_filename: str) -> None:
        with open(out_filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(inp_list)

    @staticmethod
    def append_to_file(inp_list: list, out_filename: str) -> None:
        with open(out_filename, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(inp_list)

    @staticmethod
    def purge_line_of_file_and_add_to_another(
        id_to_purge: str, out_filename_orig: str, out_filename_del: str
    ):
        rows_to_keep = []
        rows_to_delete = []
        with open(out_filename_orig, 'r', newline="") as orig_list:
            reader = csv.reader(orig_list)
            for row in reader:
                if id_to_purge in row:
                    rows_to_delete.append(row)
                else:
                    rows_to_keep.append(row)

        with open(out_filename_orig, 'w', newline="") as new_list:
            writer = csv.writer(new_list)
            writer.writerows(rows_to_keep)

        with open(out_filename_del, 'a', newline="") as new_list:
            writer = csv.writer(new_list)
            row_to_write = rows_to_delete[0]
            # update last updated timestamp
            row_to_write[-1] = str(datetime.now())
            writer.writerow(row_to_write)

        return row_to_write

    @staticmethod
    def list_display_printer(list_to_print: list):
        for i in list_to_print:
            print(",".join(i))

    @staticmethod
    def format_display(inp_string, padding_int):
        print(str(inp_string).ljust(padding_int, " "), end=" | ")

    def list_display_printer2(self, list_to_print: list, header_tuple):
        headers = list(zip(*header_tuple))[0]
        padding = list(zip(*header_tuple))[1]
        for i, j in zip(headers, padding):
            self.format_display(i, j)
        print("")
        for line in list_to_print:
            for i, j in zip(line, padding):
                self.format_display(i, j)
            print("")

    @staticmethod
    def prompt_add_product_input():
        product_name = input("Enter Product Name: ")
        # Product name string should at least have len > 0
        assert len(product_name) > 0, "Product name string should at least have len > 0"
        # Thresholds should be integers
        threshold_1 = int(input("Enter Threshold 1: "))
        threshold_2 = int(input("Enter Threshold 2: "))
        assert threshold_1 > threshold_2, "Threshold 1 must be greater than threshold 2"
        product_id = str(uuid.uuid4())
        qty = 0
        last_updated = str(datetime.now())

        return [product_id, product_name, qty, threshold_1, threshold_2, last_updated]

    def prompt_add_qty_to_product_input(self, orig_qty: int):
        qty_to_add = int(input("Enter Quantity to Add: "))
        new_qty = str(int(orig_qty) + qty_to_add)
        price_bought = float(input("Enter Price Bought: "))
        total_value = self.func_float_multiply(price_bought, qty_to_add)
        txn_id = str(uuid.uuid4())
        timestamp = str(datetime.now())
        return txn_id, orig_qty, qty_to_add, new_qty, price_bought, total_value, timestamp

    def prompt_remove_qty_from_product_input(self, orig_qty: int):
        qty_to_remove = int(input("Enter Quantity to Remove: "))
        assert int(orig_qty) >= qty_to_remove, f"Remove quantity ({qty_to_remove}) is greater than current quantity " \
                                               f"({orig_qty})! "
        new_qty = str(int(orig_qty) - qty_to_remove)
        price_sold = float(input("Enter Price Sold: "))
        total_value = self.func_float_multiply(price_sold, qty_to_remove)
        txn_id = str(uuid.uuid4())
        timestamp = str(datetime.now())
        return txn_id, orig_qty, qty_to_remove, new_qty, price_sold, total_value, timestamp


class TechMart:
    def __init__(self):
        self.helper_funcs = HelperFunctions()
        self.constants = TechMartConstants()
        self.trigger_exit = True
        self.main_menu_switcher = {
            "1": self.add_product_menu,
            "2": self.update_product_menu,
            "3": self.remove_product_menu,
            "4": self.display_inventory_history_menu,
            "5": self.recover_deleted_product,
            "6": self.restock_level_alert,
            "7": self.show_techmart_insights,
            "8": self.exit_tech_mart,
        }
        self.inventory_and_history_switcher = {
            "1": self.display_active_inventory,
            "2": self.display_inactive_inventory,
            "3": self.display_history,
            "4": self.return_to_home,
        }
        self.update_product_switcher = {
            "1": self.add_product_qty_txn,
            "2": self.remove_product_qty_txn,
            "3": self.return_to_home,
        }
        self.techmart_insights_switcher = {
            "1": self.show_total_revenue,
            "2": self.show_total_value_bought,
            "3": self.show_total_value_sold,
            "4": self.show_ave_price_bought,
            "5": self.show_ave_price_sold,
            "6": self.show_txn_count,
            "7": self.show_all_stats,
        }

    @staticmethod
    def return_to_home():
        """
        Do nothing, returns to main choices
        """
        return None

    def get_active_inventory(self):
        return self.helper_funcs.read_from_file(self.constants.INVENTORY_FILE_NAME)

    def get_inactive_inventory(self):
        return self.helper_funcs.read_from_file(self.constants.REMOVED_INVENTORY_FILE_NAME)

    def add_product_menu(self):
        self.helper_funcs.clrscr()
        input_product = self.helper_funcs.prompt_add_product_input()
        self.helper_funcs.append_to_file(input_product, self.constants.INVENTORY_FILE_NAME)
        self.helper_funcs.touch_file(f"inventory/{input_product[0]}.csv")

    def add_product_qty_txn(self):
        product_id, index_of_product_id = self.update_product_id_input()
        if product_id:
            inventory_list = self.get_active_inventory()
            orig_qty = inventory_list[index_of_product_id][2]
            txn_id, orig_qty, qty_to_add, new_qty, price_bought, total_value, timestamp \
                = self.helper_funcs.prompt_add_qty_to_product_input(orig_qty)
            history_record = [
                txn_id, "buy", orig_qty, qty_to_add, "", new_qty, price_bought, total_value, timestamp
            ]
            # set new qty in product inventory
            inventory_list[index_of_product_id][2] = new_qty
            self.helper_funcs.write_to_file(inventory_list, self.constants.INVENTORY_FILE_NAME)
            self.helper_funcs.append_to_file(
                history_record,
                f"inventory/{product_id}.csv"
            )
            print("Updated:")
            print(inventory_list[index_of_product_id])
        else:
            self.helper_funcs.clrscr()
            print("Product does not exist!")
        self.helper_funcs.click_to_continue()

    def remove_product_qty_txn(self):
        product_id, index_of_product_id = self.update_product_id_input()
        if product_id:
            inventory_list = self.get_active_inventory()
            orig_qty = inventory_list[index_of_product_id][2]
            txn_id, orig_qty, qty_to_remove, new_qty, price_sold, total_value, timestamp \
                = self.helper_funcs.prompt_remove_qty_from_product_input(orig_qty)
            history_record = [
                txn_id, "sell", orig_qty, "", qty_to_remove, new_qty, price_sold, total_value, timestamp
            ]
            # set new qty in product inventory
            inventory_list[index_of_product_id][2] = new_qty
            self.helper_funcs.write_to_file(inventory_list, self.constants.INVENTORY_FILE_NAME)
            self.helper_funcs.append_to_file(
                history_record,
                f"inventory/{product_id}.csv"
            )
            print("Updated:")
            print(inventory_list[index_of_product_id])
        else:
            self.helper_funcs.clrscr()
            print("Product does not exist!")
        self.helper_funcs.click_to_continue()

    def update_product_id_input(self):
        self.helper_funcs.clrscr()
        inv_list = [item[0] for item in self.get_active_inventory()]
        input_product_id = input("Input Product ID: ")
        if input_product_id in inv_list:
            # for getting the index of product_id in the list
            for idx, x in enumerate(inv_list):
                if x == input_product_id:
                    index = idx
                    return input_product_id, index
        else:
            return None, None

    def update_product_menu(self):
        self.helper_funcs.clrscr()
        while True:
            print(self.constants.UPDATE_PRODUCT_CHOICES)
            input_choice = input("What to do: ")
            choice_method = self.update_product_switcher.get(input_choice)
            if choice_method:
                choice_method()
                break
            self.helper_funcs.clrscr()

    def remove_product_menu(self):
        self.helper_funcs.clrscr()
        inv_list = [item[0] for item in self.get_active_inventory()]
        input_product_id = input("Input Product ID: ")
        if input_product_id in inv_list:
            self.helper_funcs.clrscr()
            deleted_product = self.helper_funcs.purge_line_of_file_and_add_to_another(
                input_product_id,
                self.constants.INVENTORY_FILE_NAME,
                self.constants.REMOVED_INVENTORY_FILE_NAME,
            )
            print("Deleted:")
            print(deleted_product)
        else:
            self.helper_funcs.clrscr()
            print("Product does not exist!")
        self.helper_funcs.click_to_continue()

    def display_inventory_history_menu(self):
        self.helper_funcs.clrscr()
        while True:
            print(self.constants.INVENTORY_HISTORY_CHOICES)
            input_choice = input("What to view: ")
            choice_method = self.inventory_and_history_switcher.get(input_choice)
            if choice_method:
                choice_method()
                break
            self.helper_funcs.clrscr()

    def display_active_inventory(self):
        self.helper_funcs.clrscr()
        print("ACTIVE INVENTORY:")
        self.helper_funcs.list_display_printer2(
            self.get_active_inventory(),
            self.constants.INVENTORY_HEADERS
        )
        self.helper_funcs.click_to_continue()

    def display_inactive_inventory(self):
        self.helper_funcs.clrscr()
        print("INACTIVE INVENTORY:")
        self.helper_funcs.list_display_printer2(
            self.get_inactive_inventory(),
            self.constants.INVENTORY_HEADERS
        )
        self.helper_funcs.click_to_continue()

    def display_history(self):
        self.helper_funcs.clrscr()
        inv_list = [item[0] for item in self.get_active_inventory()]
        input_product_id = input("Input Product ID: ")
        if input_product_id in inv_list:
            history_list = self.helper_funcs.read_from_file(f"inventory/{input_product_id}.csv")
            history_list.reverse()
            self.helper_funcs.clrscr()
            self.helper_funcs.list_display_printer2(
                history_list,
                self.constants.HISTORY_HEADERS
            )
        else:
            self.helper_funcs.clrscr()
            print("Product does not exist!")
        self.helper_funcs.click_to_continue()

    def recover_deleted_product(self):
        self.helper_funcs.clrscr()
        inv_list = [item[0] for item in self.get_inactive_inventory()]
        input_product_id = input("Input Product ID: ")
        if input_product_id in inv_list:
            self.helper_funcs.clrscr()
            deleted_product = self.helper_funcs.purge_line_of_file_and_add_to_another(
                input_product_id,
                self.constants.REMOVED_INVENTORY_FILE_NAME,
                self.constants.INVENTORY_FILE_NAME,
            )
            print("Recovered:")
            print(deleted_product)
        else:
            self.helper_funcs.clrscr()
            print("Product does not exist!")
        self.helper_funcs.click_to_continue()

    def restock_level_alert(self):
        self.helper_funcs.clrscr()
        inv_list = [item[0] for item in self.get_active_inventory()]
        input_product_id = input("Input Product ID: ")
        product_index = None
        if input_product_id in inv_list:
            for idx, x in enumerate(inv_list):
                if x == input_product_id:
                    product_index = idx
            product = self.get_active_inventory()[product_index]
            qty = int(product[2])
            threshold_1 = int(product[3])
            threshold_2 = int(product[4])

            # Checks
            if qty < threshold_1:
                print(f"Restock Needed!")
                print(f"Current Qty:{qty} is less than threshold 1 - {threshold_1}")
                if qty < threshold_2:
                    print(f"Current Qty:{qty} is less than threshold 2 - {threshold_2}")
            else:
                print(f"No Restock Needed! Current Qty: {qty} above Threshold 1 and 2 ({threshold_1},{threshold_2})")
        else:
            self.helper_funcs.clrscr()
            print("Product does not exist!")
        self.helper_funcs.click_to_continue()

    def show_total_revenue(self, input_product_id):
        history_list = self.helper_funcs.read_from_file(f"inventory/{input_product_id}.csv")
        buys = [item for item in history_list if item[1] == 'buy']
        buys_values = [float(txn[-2]) for txn in buys]
        total_buys_value = math.fsum(buys_values)
        sells = [item for item in history_list if item[1] == 'sell']
        sells_values = [float(txn[-2]) for txn in sells]
        total_sells_value = math.fsum(sells_values)
        total_revenue = math.fsum([total_sells_value, -total_buys_value])
        print(f"Total Revenue is {total_revenue}")

    def show_total_value_bought(self, input_product_id):
        history_list = self.helper_funcs.read_from_file(f"inventory/{input_product_id}.csv")
        buys = [item for item in history_list if item[1] == 'buy']
        buys_values = [float(txn[-2]) for txn in buys]
        total_buys_value = math.fsum(buys_values)
        print(f"Total Value Bought is {total_buys_value}")

    def show_total_value_sold(self, input_product_id):
        history_list = self.helper_funcs.read_from_file(f"inventory/{input_product_id}.csv")
        sells = [item for item in history_list if item[1] == 'sell']
        sells_values = [float(txn[-2]) for txn in sells]
        total_sells_value = math.fsum(sells_values)
        print(f"Total Value Sold is {total_sells_value}")

    def show_max_min_buy_price(self, input_product_id):
        history_list = self.helper_funcs.read_from_file(f"inventory/{input_product_id}.csv")
        buys = [item for item in history_list if item[1] == 'buy']
        buys_values = [float(txn[-3]) for txn in buys]
        if buys_values:
            max_buy_price = max(buys_values)
            min_buy_price = min(buys_values)
        else:
            max_buy_price = 0
            min_buy_price = 0
        print(f"Min buy price is {min_buy_price}, Max buy price is {max_buy_price}")

    def show_max_min_sell_price(self, input_product_id):
        history_list = self.helper_funcs.read_from_file(f"inventory/{input_product_id}.csv")
        sells = [item for item in history_list if item[1] == 'sell']
        sells_values = [float(txn[-3]) for txn in sells]
        if sells_values:
            max_sell_price = max(sells_values)
            min_sell_price = min(sells_values)
        else:
            max_sell_price = 0
            min_sell_price = 0
        print(f"Min sell price is {min_sell_price}, Max sell price is {max_sell_price}")

    def show_ave_price_bought(self, input_product_id):
        history_list = self.helper_funcs.read_from_file(f"inventory/{input_product_id}.csv")
        buys = [item for item in history_list if item[1] == 'buy']
        buys_values = [float(txn[-3]) for txn in buys]
        if buys_values:
            ave_buy_value = round(numpy.average(buys_values), 2)
        else:
            ave_buy_value = 0
        print(f"Ave Buy Price is {ave_buy_value}")

    def show_ave_price_sold(self, input_product_id):
        history_list = self.helper_funcs.read_from_file(f"inventory/{input_product_id}.csv")
        sells = [item for item in history_list if item[1] == 'sell']
        sells_values = [float(txn[-3]) for txn in sells]
        if sells_values:
            ave_sell_value = round(numpy.average(sells_values), 2)
        else:
            ave_sell_value = 0
        print(f"Ave Sell Price is {ave_sell_value}")

    def show_txn_count(self, input_product_id):
        history_list = self.helper_funcs.read_from_file(f"inventory/{input_product_id}.csv")
        txn_count = len(history_list)
        print(f"Number of transactions occured is {txn_count}")

    def show_all_stats(self):
        inv_list = [item[0] for item in self.get_active_inventory()]
        input_product_id = input("Input Product ID: ")
        if input_product_id in inv_list:
            self.show_total_revenue(input_product_id)
            self.show_total_value_bought(input_product_id)
            self.show_total_value_sold(input_product_id)
            self.show_ave_price_bought(input_product_id)
            self.show_max_min_buy_price(input_product_id)
            self.show_ave_price_sold(input_product_id)
            self.show_max_min_sell_price(input_product_id)
            self.show_txn_count(input_product_id)
        else:
            self.helper_funcs.clrscr()
            print("Product does not exist!")
        self.helper_funcs.click_to_continue()

    def show_techmart_insights(self):
        self.helper_funcs.clrscr()
        self.show_all_stats()

    def exit_tech_mart(self):
        self.trigger_exit = False

    def other_choice(self):
        self.helper_funcs.clrscr()
        print(self.constants.INVALID_SELECTION_MESSAGE)
        self.helper_funcs.click_to_continue()

    def todo(self):
        pass

    def main(self):
        self.helper_funcs.clrscr()
        print(self.constants.WELCOME_MESSAGE)
        while self.trigger_exit:
            print(self.constants.MAIN_CHOICES)
            input_choice = input("What do you want to do: ")
            choice_method = self.main_menu_switcher.get(input_choice, self.other_choice)

            if choice_method:
                try:
                    choice_method()

                except Exception as e:
                    if e.args:
                        # For Asserts
                        print(e.args[0])
                    else:
                        print(e)
                    print(self.constants.EXCEPTION_OCCURRED)
                    self.helper_funcs.click_to_continue()
                self.helper_funcs.clrscr()


tm = TechMart()
tm.main()
