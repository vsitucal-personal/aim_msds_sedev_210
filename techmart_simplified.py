"""
Authors:
Vincent Itucal
Rhodora Cleofe
Leonard Rizada
Jamil Hadji Alawi
"""

import os
import uuid
from datetime import datetime
from typing import List, Union


class TechMartConstants:
    """
    A class that defines constants used in the Tech Mart Management System.

    Attributes:
        WELCOME_MESSAGE (str): A welcome message displayed at the start of the program.
        MAIN_CHOICES (str): A list of main choices available in the Tech Mart Management System menu.
        INVENTORY_HISTORY_CHOICES (str): A list of choices available in the inventory history submenu.
        UPDATE_PRODUCT_CHOICES (str): A list of choices available in the update product submenu.
        INVALID_SELECTION_MESSAGE (str): A message displayed when an invalid selection is made.
        EXCEPTION_OCCURRED (str): A message displayed when an exception occurs due to bad input.
        INVENTORY_HEADERS (list): A list of tuples representing inventory headers and their corresponding padding.
        HISTORY_HEADERS (list): A list of tuples representing history headers and their corresponding padding.
        INVENTORY_FILE_NAME (str): The name of the CSV file containing active product inventory data.
        REMOVED_INVENTORY_FILE_NAME (str): The name of the CSV file containing inactive product inventory data.
    """

    WELCOME_MESSAGE = "Welcome to Tech Mart Management System!!!"
    MAIN_CHOICES = "1 - Add Product Inventory\n" \
                   "2 - Update Product Quantity\n" \
                   "3 - Remove a product from inventory\n" \
                   "4 - Display Inventory\n" \
                   "5 - Recover Deleted Product\n" \
                   "6 - Product Restock Level Alert\n" \
                   "7 - Show TechMart Insights\n" \
                   "8 - Exit "
    INVENTORY_HISTORY_CHOICES = "1 - Display Active Product Inventory\n" \
                                "2 - Display Inactive Product Inventory\n" \
                                "3 - Display Product Transaction History\n" \
                                "4 - Return to home"
    UPDATE_PRODUCT_CHOICES = "1 - Add Product Quantity Transaction\n" \
                             "2 - Remove Product Quantity Transaction\n" \
                             "3 - Return to home"
    INVALID_SELECTION_MESSAGE = "NOT IN CHOICES PICK AGAIN"
    EXCEPTION_OCCURRED = "EXCEPTION OCCURRED BAD INPUT"
    INVENTORY_HEADERS = [
        ("Product ID", 36), ("Product Name", 16), ("Quantity", 8), ("Threshold1", 10), ("Threshold2", 10),
        ("Last Updated", 26),
    ]
    HISTORY_HEADERS = [
        ("Transaction ID", 36), ("Transaction Type", 16), ("Start Qty", 9), ("Add", 9), ("Remove", 9), ("End Qty", 9),
        ("Unit Price", 11), ("Total Value", 11), ("Timestamp", 26)
    ]
    INVENTORY_FILE_NAME = "tech_mart_inventory.csv"
    REMOVED_INVENTORY_FILE_NAME = "inactive_tech_mart_inventory.csv"


class HelperFunctions:
    """
       A class containing various static and instance methods for utility functions in the Tech Mart Management System.
    """

    @staticmethod
    def timestamp_now():
        """
        Get the current timestamp as a string.

        This method returns the current timestamp as a string representation. The timestamp is generated using the
        `datetime.now()` function, which retrieves the current date and time.

        Returns:
            str: A string representation of the current timestamp.
        """
        return str(datetime.now())

    @staticmethod
    def clrscr():
        """
        Clears the console screen based on the operating system. Doesn't clear in Jupyter Notebooks though.

        Example:
            clrscr()  # Clears the console screen.
        """
        if os.name == 'nt':  # Check if the operating system is Windows
            os.system('cls')
        else:  # Assume Unix-based system (Linux, macOS, etc.)
            os.system('clear')

    @staticmethod
    def click_to_continue():
        """
        Pauses the program and prompts the user to click any button to continue.

        Note:
            The prompt will be displayed until the user provides any input,
            which can be any character or key pressed on the keyboard. Need to input in textbox provided in Jupyter

        Example:
            click_to_continue()  # Pauses the program until the user clicks any button to continue.
        """
        input("Click any button to continue...")

    @staticmethod
    def read_from_file(inp_filename: str) -> list:
        """
        Reads data from a CSV file and returns it as a list of lists.

        This static method reads data from the specified CSV file and converts it into a list of lists.
        Each line in the CSV file is considered a separate list within the returned list.
        The elements within each line are split using commas (',') as the delimiter.

        Parameters:
            inp_filename (str): The name of the CSV file to read from.

        Returns:
            list: A list of lists containing the data read from the CSV file.
             Each sublist represents a line of data from the file, with its elements as individual data points.

        Note:
            If the specified file does not exist or cannot be accessed (IOError), an empty list will be returned.

        Example:
            data_list = read_from_file("data.csv")
            print(data_list)  # Output: [['John', 'Doe', '30'], ['Jane', 'Smith', '25'], ['Michael', 'Johnson', '42']]
        """
        try:
            with open(inp_filename, "r") as file:
                lines = file.read().splitlines()
                data = []
                for line in lines:
                    list_data = line.split(",")
                    data.append(list_data)
        except IOError:
            # probably no inp file
            data = []
        return data

    @staticmethod
    def touch_file(out_filename: str):
        """
        Creates a new file if it doesn't exist, along with any necessary directories.

        This static method checks if the specified 'out_filename' file exists. If not, it creates
        the necessary directories (if any) and the file itself. If the file already exists, this method has no effect.

        Parameters:
            out_filename (str): The name of the file to be created or checked.

        Note:
            The 'out_filename' can include a relative or absolute path to the file.

        Example:
            touch_file("data/output.txt")
            # If 'output.txt' file does not exist, it will be created in the 'data' directory.
        """
        if not os.path.exists(out_filename.split("/")[0]):
            os.mkdir(out_filename.split("/")[0])
        open(out_filename, "a").close()

    @staticmethod
    def write_to_file(inp_list: list, out_filename: str) -> None:
        """
        Writes data from a list of lists to a CSV file.

        This static method takes a list of lists 'inp_list' and writes its data to a CSV file specified by
        'out_filename'. Each sublist within 'inp_list' represents a line in the CSV file.
        The elements in each sublist are joined together with commas (',') as the delimiter before
        being written to the file.

        Parameters:
            inp_list (list): The list of lists containing the data to be written to the CSV file.
            out_filename (str): The name of the CSV file to which the data will be written.

        Note:
            The 'out_filename' can include a relative or absolute path to the file.
            The contents of the existing file (if any) will be overwritten.

        Example:
            data_list = [['John', 'Doe', '30'], ['Jane', 'Smith', '25'], ['Michael', 'Johnson', '42']]
            write_to_file(data_list, "output.csv")
            # The 'output.csv' file will be created (or overwritten if it already exists) with the data
            # from 'data_list'.
        """
        with open(out_filename, "w") as file:
            for element in inp_list:
                to_write = ",".join(element)
                file.write(f"{to_write}\n")

    @staticmethod
    def append_to_file(inp_list: list, out_filename: str) -> None:
        """
        Appends data from a list to an existing CSV file.

        This static method takes a list 'inp_list' and appends its data to an existing CSV file specified by
        'out_filename'. The elements of 'inp_list' are joined together with commas (',') as the delimiter and
        then written as a new line at the end of the file.

        Parameters:
            inp_list (list): The list containing the data to be appended to the CSV file.
            out_filename (str): The name of the CSV file to which the data will be appended.

        Note:
            The 'out_filename' can include a relative or absolute path to the file.
            The method will create the file if it does not exist.

        Example:
            data_list = ['John', 'Doe', '30']
            append_to_file(data_list, "output.csv")
            # The data_list will be appended as a new line to the 'output.csv' file.
        """
        with open(out_filename, "a") as file:
            to_append = ",".join([str(i) for i in inp_list])
            file.write(f"{to_append}\n")

    def purge_line_of_file_and_add_to_another(
      self, id_to_purge: str, out_filename_orig: str, out_filename_del: str
    ):
        """
        Purges a line with a given ID from one CSV file and adds it to another, along with a timestamp.

        This method takes a 'id_to_purge' string and searches for its occurrence in the CSV file specified by
        'out_filename_orig'. If the ID is found, the corresponding line is removed from 'out_filename_orig' and
        appended to the file specified by 'out_filename_del'. A timestamp is added to the removed line before
        appending it to the 'out_filename_del'.

        Parameters:
            id_to_purge (str): The ID to be searched and purged from the original CSV file.
            out_filename_orig (str): The name of the CSV file from which the ID will be purged.
            out_filename_del (str): The name of the CSV file to which the purged line will be added with a timestamp.

        Returns:
            list: The line that was purged from the original file and added to the destination file with a timestamp.

        Note:
            Both 'out_filename_orig' and 'out_filename_del' can include a relative or absolute path to the file.

        Example:
            id_to_remove = "ABC123"
            original_file = "data/inventory.csv"
            deleted_file = "data/deleted_inventory.csv"
            purged_line = purge_line_of_file_and_add_to_another(id_to_remove, original_file, deleted_file)
            print(purged_line)  # Output: ['ABC123', 'Product A', '15', '20', '5', '2023-08-03 10:30:00']
        """
        rows_to_keep = []
        rows_to_delete = []
        reader = self.read_from_file(out_filename_orig)
        for row in reader:
            if id_to_purge in row:
                rows_to_delete.append(row)
            else:
                rows_to_keep.append(row)

        self.write_to_file(rows_to_keep, out_filename_orig)
        row_to_write = rows_to_delete[0]
        row_to_write[-1] = self.timestamp_now()
        self.append_to_file(row_to_write, out_filename_del)

        return row_to_write

    @staticmethod
    def format_display(inp_string, padding_int):
        """
        Formats and prints a string with the specified padding.

        This static method takes an 'inp_string' and a 'padding_int' as input and prints the 'inp_string' with
        left-justified padding. The padding is achieved by adding spaces to the right of the string until it reaches
        the specified length given by 'padding_int'.

        Parameters:
            inp_string (str): The string to be formatted and printed.
            padding_int (int): The desired length of the formatted string, determined by the number of characters.

        Returns:
            None

        Example:
            product_name = "Widget A"
            quantity = 25
            format_display(product_name, 15)
            format_display(quantity, 10)
            # Output:
            # Widget A      | 25        |
        """
        print(str(inp_string).ljust(padding_int, " "), end=" | ")

    def list_display_printer(self, list_to_print: list, header_tuple):
        """
        Formats and prints a list of lists with aligned headers.

        This method takes a list of lists 'list_to_print' and a 'header_tuple', which contains header information in
        the form of (header_name, padding_length) pairs. It formats and prints the list data along with the headers
        aligned using the specified padding lengths.

        Parameters:
            list_to_print (list): The list of lists containing data to be displayed.
            header_tuple (list(tuple)): A tuple of (header_name, padding_length) pairs for each column header.

        Returns:
            None

        Example:
            inventory_data = [
                ["001", "Widget A", 25, 20, 5],
                ["002", "Widget B", 50, 40, 10],
                ["003", "Widget C", 30, 25, 5]
            ]
            headers = [("Product ID", 5), ("Product Name", 15), ("Quantity", 10), ("Threshold1", 10),
            ("Threshold2", 10)]
            list_display_printer(inventory_data, headers)
            # Output:
            # Product ID | Product Name   | Quantity   | Threshold1 | Threshold2 |
            # 001        | Widget A       | 25         | 20         | 5          |
            # 002        | Widget B       | 50         | 40         | 10         |
            # 003        | Widget C       | 30         | 25         | 5          |
        """
        headers = list(zip(*header_tuple))[0]
        padding = list(zip(*header_tuple))[1]
        for i, j in zip(headers, padding):
            self.format_display(i, j)
        print("")
        for line in list_to_print:
            for i, j in zip(line, padding):
                self.format_display(i, j)
            print("")

    def prompt_add_product_input(self):
        """
        Prompts the user to input data for adding a new product.

        This static method guides the user to input necessary details to add a new product to the inventory.
        It prompts the user to enter the product name, threshold values, and generates a unique product ID using UUID.
        The quantity of the product is set to 0, and the 'last_updated' timestamp is recorded as the current date and
        time.

        Returns:
            list: A list containing the input data for the new product in the following order:
            [product_id, product_name, quantity, threshold_1, threshold_2, last_updated]

        Note:
            The product name must have a length greater than 0.
            The thresholds should be integers, and threshold_1 should be greater than threshold_2.

        Example:
            new_product_data = prompt_add_product_input()
            # User enters the following inputs:
            # Enter Product Name: Widget X
            # Enter Threshold 1: 100
            # Enter Threshold 2: 80
            # Output: ['b4cf85b5-987f-465b-90a6-1fbd9e00f7ce', 'Widget X', 0, 100, 80, '2023-08-03 11:45:00']
        """
        product_name = input("Enter Product Name: ")
        # Product name string should at least have len > 0
        assert len(product_name) > 0, "Product name string should at least have len > 0"
        # Thresholds should be integers
        threshold_1 = int(input("Enter Threshold 1: "))
        threshold_2 = int(input("Enter Threshold 2: "))
        assert threshold_1 > threshold_2, "Threshold 1 must be greater than threshold 2"
        product_id = str(uuid.uuid4())
        qty = 0
        last_updated = self.timestamp_now()

        return [product_id, product_name, qty, threshold_1, threshold_2, last_updated]

    def prompt_add_qty_to_product_input(self, orig_qty: int):
        """
        Prompts the user to input data for adding quantity to a product.

        This static method guides the user to input the necessary details when adding quantity to an existing product
        in the inventory. It prompts the user to enter the quantity to be added, the price at which the items were
        bought, and automatically generates a unique transaction ID using UUID. The method calculates the new quantity,
        the total value of the transaction, and records the timestamp when the transaction occurred.

        Parameters:
            orig_qty (int): The current quantity of the product before adding.

        Returns:
            tuple: A tuple containing the input data for the transaction in the following order:
            (txn_id, orig_qty, qty_to_add, new_qty, price_bought, total_value, timestamp)

        Example:
            current_qty = 50
            transaction_data = prompt_add_qty_to_product_input(current_qty)
            # User enters the following inputs:
            # Enter Quantity to Add: 20
            # Enter Price Bought: 10.5
            # Output: ('bb93a2dd-1f12-4d6c-91a3-c70b192c7be6', 50, 20, 70, 10.5, 210.0, '2023-08-03 12:00:00')
        """
        qty_to_add = int(input("Enter Quantity to Add: "))
        new_qty = str(int(orig_qty) + qty_to_add)
        price_bought = float(input("Enter Price Bought: "))
        total_value = round(price_bought * qty_to_add, 2)
        txn_id = str(uuid.uuid4())
        timestamp = self.timestamp_now()
        return txn_id, orig_qty, qty_to_add, new_qty, price_bought, total_value, timestamp

    def prompt_remove_qty_from_product_input(self, orig_qty: int):
        """
        Prompts the user to input data for removing quantity from a product.

        This static method guides the user to input the necessary details when removing quantity from an existing
        product in the inventory. It prompts the user to enter the quantity to be removed, the price at which the
        items were sold, and automatically generates a unique transaction ID using UUID. The method verifies that
        the quantity to remove does not exceed the current quantity in stock. It calculates the new quantity,
        the total value of the transaction, and records the timestamp when the transaction occurred.

        Parameters:
            orig_qty (int): The current quantity of the product before removal.

        Returns:
            tuple: A tuple containing the input data for the transaction in the following order:
            (txn_id, orig_qty, qty_to_remove, new_qty, price_sold, total_value, timestamp)

        Raises:
            AssertionError: If the 'qty_to_remove' is greater than the 'orig_qty', an AssertionError is raised with an
            error message.

        Example:
            current_qty = 100
            transaction_data = prompt_remove_qty_from_product_input(current_qty)
            # User enters the following inputs:
            # Enter Quantity to Remove: 20
            # Enter Price Sold: 15.5
            # Output: ('86f00e3b-ba51-4d2c-9895-06b1aef1b96b', 100, 20, 80, 15.5, 310.0, '2023-08-03 12:15:00')
        """
        qty_to_remove = int(input("Enter Quantity to Remove: "))
        assert int(orig_qty) >= qty_to_remove, \
            f"Remove quantity ({qty_to_remove}) is greater than current quantity " \
            f"({orig_qty})! "
        new_qty = str(int(orig_qty) - qty_to_remove)
        price_sold = float(input("Enter Price Sold: "))
        total_value = round(price_sold * qty_to_remove, 2)
        txn_id = str(uuid.uuid4())
        timestamp = self.timestamp_now()
        return txn_id, orig_qty, qty_to_remove, new_qty, price_sold, total_value, timestamp

    def list_averager(self, inp_list: List[Union[int, float]]):
        """
        Computes the average of elements in a numeric list.

        This method takes a numeric list 'inp_list' containing integers or floating-point numbers and calculates the
        average (mean) of all its elements.

        Parameters:
            inp_list (List[Union[int, float]]): The numeric list whose elements will be averaged.

        Returns:
            float: The average of all the elements in the input list, rounded to two decimal places.

        Example:
            numbers = [10, 5, 7, 3, 2]
            avg = list_averager(numbers)
            print(avg)  # Output: 5.4 (average of elements in 'numbers' list)
        """
        return round((self.list_summer(inp_list) / len(inp_list)), 2)

    @staticmethod
    def list_summer(inp_list: List[Union[int, float]]):
        """
        Computes the sum of elements in a numeric list.

        This static method takes a numeric list 'inp_list' containing integers or floating-point numbers and
        calculates the sum of all its elements.

        Parameters:
            inp_list (List[Union[int, float]]): The numeric list whose elements will be summed.

        Returns:
            int or float: The sum of all the elements in the input list.

        Example:
            numbers = [10, 5, 7, 3, 2]
            total_sum = list_summer(numbers)
            print(total_sum)  # Output: 27 (sum of elements in 'numbers' list)
        """
        list_sum = 0
        for element in inp_list:
            list_sum += element
        return list_sum

    @staticmethod
    def find_product_id_index_in_list(input_product_id: str, inv_list: list):
        """
        Searches for a given product ID in a list and returns its index.

        This static method takes a 'input_product_id' string and searches for its occurrence in the provided 'inv_list'
        list. If the product ID is found in the list, the method returns the index of the first occurrence.
         If the product ID is not found, the method returns None.

        Parameters:
            input_product_id (str): The product ID to be searched in the list.
            inv_list (list): The list in which the product ID will be searched.

        Returns:
            int or None: The index of the first occurrence of the product ID in the list, or None if the product ID
             is not found.

        Example:
            product_id = "ABC123"
            inventory = ["XYZ987", "DEF456", "GHI789", "ABC123", "JKL321"]
            index = find_product_id_index_in_list(product_id, inventory)
            print(index)  # Output: 3 (index of "ABC123" in the list)
        """
        for idx, x in enumerate(inv_list):
            if x == input_product_id:
                index = idx
                return index


class TechMart:
    """
    TechMart class represents a management system for a tech store.

    This class manages the inventory of products and provides various functionalities like adding products,
    updating product quantities, removing products, displaying inventory history, recovering deleted products,
    restock level alerts, showing TechMart insights, and exiting the system.
    """

    def __init__(self):
        """
        Initializes the TechMart class.

        This constructor sets up the TechMart instance by initializing attributes and creating dictionaries
        for menu choices. It also initializes HelperFunctions and TechMartConstants instances.
        """
        self.helper_funcs = HelperFunctions()
        self.constants = TechMartConstants()
        self.trigger_exit = True
        self.main_menu_switcher = {
            # Dorie
            "1": self.add_product_menu,
            # Jamil
            "2": self.update_product_menu,
            # Leonard
            "3": self.remove_product_menu,
            # Vincent
            "4": self.display_inventory_history_menu,
            # Leonard
            "5": self.recover_deleted_product,
            # Vincent
            "6": self.restock_level_alert,
            # Vincent
            "7": self.show_all_stats,
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
        """
        Get the active inventory from the inventory file.

        This method reads the active inventory data from the inventory file and returns it as a list.

        Returns:
            list: A list containing the active inventory data. Each element in the list represents a product
                  with its attributes, such as Product ID, Product Name, Quantity, Threshold1, Threshold2,
                  and Last Updated.
        """
        return self.helper_funcs.read_from_file(self.constants.INVENTORY_FILE_NAME)

    def get_inactive_inventory(self):
        """
        Get the inactive inventory from the removed inventory file.

        This method reads the inactive inventory data from the removed inventory file and returns it as a list.

        Returns:
            list: A list containing the inactive inventory data. Each element in the list represents a product
                  with its attributes, such as Product ID, Product Name, Quantity, Threshold1, Threshold2,
                  and Last Updated.
        """
        return self.helper_funcs.read_from_file(self.constants.REMOVED_INVENTORY_FILE_NAME)

    def add_product_menu(self):
        """
        Author: Rhodora Cleofe

        Display the add product menu and process the input.

        This method displays the add product menu, prompts the user to input product details, and adds the product
        to the inventory file. It also creates a new CSV file for the product in the 'inventory' directory if it does
        not already exist. After successful addition, it prints the added product details.

        Returns:
            None
        """
        self.helper_funcs.clrscr()
        input_product = self.helper_funcs.prompt_add_product_input()
        self.helper_funcs.append_to_file(input_product, self.constants.INVENTORY_FILE_NAME)
        self.helper_funcs.touch_file(f"inventory/{input_product[0]}.csv")
        print("Added Product:")
        print(f"{input_product}")
        self.helper_funcs.click_to_continue()

    def add_product_qty_txn(self):
        """
        Display the add product menu and add a new product to the inventory.

        This method presents the add product menu to the user, where they can input the details of a new product,
        including the Product Name, Threshold1, and Threshold2. After receiving the input, the method adds the new
        product to the inventory by appending its details to the inventory file. Additionally, it creates a new file
        for the product in the 'inventory' directory with its Product ID as the filename.

        Note:
            - The Product ID is generated using the `uuid.uuid4()` function to ensure uniqueness.
            - The Quantity is initialized to 0 when a new product is added.
            - The Last Updated attribute is set to the current timestamp.

        Returns:
            None
        """
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
        """
        Remove quantity from an existing product and record the transaction in the history.

        This method allows the user to remove a specific quantity of an existing product from the inventory.
        It first prompts the user to input the Product ID of the product they want to update. If the Product ID
        is found in the active inventory, the user is prompted to enter the quantity to remove and the price
        at which the product was sold. The method then records the transaction in the product's history file
        with a unique transaction ID, the original quantity, the quantity removed, the new quantity after removal,
        the price at which the product was sold, the total value of the transaction, and the current timestamp.

        Returns:
            None

        Notes:
            - The transaction ID is generated using `uuid.uuid4()` for uniqueness.
            - The user cannot remove a quantity greater than the current quantity of the product.
            - If the product does not exist, the method displays an appropriate message.
        """
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
        """
        Prompt the user to input the Product ID and find its index in the active inventory list.

        This method clears the screen and then prompts the user to input the Product ID of the product they
        want to update. It retrieves the list of Product IDs from the active inventory and checks if the input
        Product ID exists in the list. If found, the method returns a tuple containing the input Product ID
        and its corresponding index in the active inventory list. If the Product ID does not exist in the list,
        the method returns a tuple with two None values.

        Returns:
            tuple: A tuple containing two elements - the input Product ID (str) and its index (int) in the
                active inventory list. If the Product ID does not exist in the list, it returns a tuple
                with two None values.
        """
        self.helper_funcs.clrscr()
        inv_list = [item[0] for item in self.get_active_inventory()]
        input_product_id = input("Input Product ID: ")
        if input_product_id in inv_list:
            # for getting the index of product_id in the list
            return input_product_id, self.helper_funcs.find_product_id_index_in_list(input_product_id, inv_list)
        else:
            return None, None

    def update_product_menu(self):
        """
        Author: Jamil Hadji Alawi

        Display the update product menu and execute the chosen action.

        This method clears the screen and displays the update product menu with various choices.
        It prompts the user to input their choice and then uses the update_product_switcher dictionary
        to find the corresponding method to execute based on the user's choice. If a valid choice is found,
        the associated method is executed, and the loop is broken to return to the main menu. If the user
        enters an invalid choice, the screen is cleared, and the menu is displayed again for the user to
        choose a valid option.

        Returns:
            None
        """
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
        """
        Author: Leonard Rizada

        Display the remove product menu and execute the chosen action.

        This method clears the screen and prompts the user to input the Product ID of the product
        they want to remove from the active inventory. It checks if the entered Product ID exists in
        the active inventory list. If the product exists, it will move the product from the active
        inventory file to the removed inventory file and print the details of the deleted product.
        If the entered Product ID does not exist in the active inventory list, it will display a message
        indicating that the product does not exist.

        Returns:
            None
        """
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
        """
        Author: Vincent Itucal

        Display the inventory and history menu and execute the chosen action.

        This method clears the screen and presents a menu of options to the user related to viewing
        inventory and transaction history. The user is prompted to select an option by entering the
        corresponding number. The selected option is then executed using the switcher dictionary,
        which maps the user's input to specific methods.

        Returns:
            None
        """
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
        """
        Display the active inventory items to the user.

        This method clears the screen, prints a header indicating that the displayed items are from the
        active inventory, and then prints the active inventory items in a tabular format. The inventory
        items are fetched using the `get_active_inventory` method, and the headers for the tabular format
        are taken from the `INVENTORY_HEADERS` constant. After displaying the items, the user is prompted
        to continue by pressing any button.

        Returns:
            None
        """
        self.helper_funcs.clrscr()
        print("ACTIVE INVENTORY:")
        self.helper_funcs.list_display_printer(
            self.get_active_inventory(),
            self.constants.INVENTORY_HEADERS
        )
        self.helper_funcs.click_to_continue()

    def display_inactive_inventory(self):
        """
        Display the inactive inventory items to the user.

        This method clears the screen, prints a header indicating that the displayed items are from the
        inactive inventory, and then prints the inactive inventory items in a tabular format. The inventory
        items are fetched using the `get_inactive_inventory` method, and the headers for the tabular format
        are taken from the `INVENTORY_HEADERS` constant. After displaying the items, the user is prompted
        to continue by pressing any button.

        Returns:
            None
        """
        self.helper_funcs.clrscr()
        print("INACTIVE INVENTORY:")
        self.helper_funcs.list_display_printer(
            self.get_inactive_inventory(),
            self.constants.INVENTORY_HEADERS
        )
        self.helper_funcs.click_to_continue()

    def display_history(self):
        """
        Display the transaction history of a specific product.

        This method clears the screen, prompts the user to input a product ID, and checks if the product ID
        exists in the active inventory list. If the product ID exists, the method reads the transaction
        history from the corresponding file in the "inventory" directory and displays it in reverse order.
        The transaction history is printed in a tabular format using the `HISTORY_HEADERS` constant for
        column headers. If the product ID does not exist, a message indicating that the product does not
        exist is printed. After displaying the history or the error message, the user is prompted to
        continue by pressing any button.

        Returns:
            None
        """
        self.helper_funcs.clrscr()
        inv_list = [item[0] for item in self.get_active_inventory()]
        input_product_id = input("Input Product ID: ")
        if input_product_id in inv_list:
            history_list = self.helper_funcs.read_from_file(f"inventory/{input_product_id}.csv")
            history_list.reverse()
            self.helper_funcs.clrscr()
            self.helper_funcs.list_display_printer(
                history_list,
                self.constants.HISTORY_HEADERS
            )
        else:
            self.helper_funcs.clrscr()
            print("Product does not exist!")
        self.helper_funcs.click_to_continue()

    def recover_deleted_product(self):
        """
        Author: Leonard Rizada

        Recover a deleted product from the inactive inventory.

        This method clears the screen, prompts the user to input a product ID, and checks if the product ID
        exists in the inactive inventory list. If the product ID exists, the method removes the product from
        the inactive inventory file and adds it back to the active inventory file. The recovered product is
        printed to the console. If the product ID does not exist in the inactive inventory, a message indicating
        that the product does not exist is printed. After recovering the product or displaying the error message,
        the user is prompted to continue by pressing any button.

        Returns:
            None
        """
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
        """
        Author: Vincent Itucal

        Check if a product needs restocking based on its current quantity and threshold levels.

        This method clears the screen, prompts the user to input a product ID, and checks if the product ID
        exists in the active inventory list. If the product ID exists, the method retrieves the product's
        information, including its current quantity, threshold 1, and threshold 2. It then compares the
        current quantity with the threshold levels and prints a restocking alert if the quantity is below
        any of the thresholds. If the quantity is above both thresholds, it indicates that no restocking
        is needed. If the product ID does not exist in the active inventory, a message indicating that
        the product does not exist is printed. After displaying the restocking alert or the error message,
        the user is prompted to continue by pressing any button.

        Returns:
            None
        """
        self.helper_funcs.clrscr()
        inv_list = [item[0] for item in self.get_active_inventory()]
        input_product_id = input("Input Product ID: ")
        if input_product_id in inv_list:
            product_index = self.helper_funcs.find_product_id_index_in_list(input_product_id, inv_list)
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

    def show_total_revenue(self, history_list):
        """
        Calculate and display the total revenue for a product based on its transaction history.

        This method calculates the total revenue for a product by summing up the values of its 'buy' transactions and
        subtracting the values of its 'sell' transactions from it. It then prints the calculated total revenue.

        Parameters:
            history_list (list): A list containing the transaction history of a product.

        Returns:
            None
        """
        buys = [item for item in history_list if item[1] == 'buy']
        buys_values = [float(txn[-2]) for txn in buys]
        total_buys_value = self.helper_funcs.list_summer(buys_values)
        sells = [item for item in history_list if item[1] == 'sell']
        sells_values = [float(txn[-2]) for txn in sells]
        total_sells_value = self.helper_funcs.list_summer(sells_values)
        total_revenue = self.helper_funcs.list_summer([total_sells_value, -total_buys_value])
        print(f"Total Revenue is {total_revenue}")

    def show_total_value_bought(self, history_list):
        """
        Calculate and display the total value of products bought based on the 'buy' transactions in the history.

        This method calculates the total value of products bought for a specific product based on its 'buy' transactions
        in the given history_list. It then prints the calculated total value.

        Parameters:
            history_list (list): A list containing the transaction history of a product.

        Returns:
            None
        """
        buys = [item for item in history_list if item[1] == 'buy']
        buys_values = [float(txn[-2]) for txn in buys]
        total_buys_value = self.helper_funcs.list_summer(buys_values)
        print(f"Total Value Bought is {total_buys_value}")

    def show_total_value_sold(self, history_list):
        """
        Calculate and display the total value of products sold based on the 'sell' transactions in the history.

        This method calculates the total value of products sold for a specific product based on its 'sell' transactions
        in the given history_list. It then prints the calculated total value.

        Parameters:
            history_list (list): A list containing the transaction history of a product.

        Returns:
            None
        """
        sells = [item for item in history_list if item[1] == 'sell']
        sells_values = [float(txn[-2]) for txn in sells]
        total_sells_value = self.helper_funcs.list_summer(sells_values)
        print(f"Total Value Sold is {total_sells_value}")

    @staticmethod
    def show_max_min_buy_price(history_list):
        """
        Calculate and display the minimum and maximum buy prices for a specific product based on its 'buy' transactions.

        This static method calculates the minimum and maximum buy prices for a specific product based on its 'buy'
        transactions in the given history_list. It then prints the calculated minimum and maximum buy prices.

        Parameters:
            history_list (list): A list containing the transaction history of a product.

        Returns:
            None
        """
        buys = [item for item in history_list if item[1] == 'buy']
        buys_values = [float(txn[-3]) for txn in buys]
        if buys_values:
            max_buy_price = max(buys_values)
            min_buy_price = min(buys_values)
        else:
            max_buy_price = 0
            min_buy_price = 0
        print(f"Min buy price is {min_buy_price}, Max buy price is {max_buy_price}")

    @staticmethod
    def show_max_min_sell_price(history_list):
        """
        Calculate and display the minimum and maximum sell prices of a specific product.

        This static method calculates the minimum and maximum sell prices of a specific product based on
        the given history_list, which contains the transaction history of the product. It filters the
        transactions for 'sell' events, extracts the sell prices, and then determines the minimum and
        maximum sell prices. If no sell transactions are found, it sets both the minimum and maximum
        sell prices to 0.

        Parameters:
            history_list (list): A list containing the transaction history of a product.

        Returns:
            None
        """
        sells = [item for item in history_list if item[1] == 'sell']
        sells_values = [float(txn[-3]) for txn in sells]
        if sells_values:
            max_sell_price = max(sells_values)
            min_sell_price = min(sells_values)
        else:
            max_sell_price = 0
            min_sell_price = 0
        print(f"Min sell price is {min_sell_price}, Max sell price is {max_sell_price}")

    def show_ave_price_bought(self, history_list):
        """
        Calculate and display the average buy price of a specific product.

        This function calculates the average buy price of a specific product based on the given
        history_list, which contains the transaction history of the product. It filters the transactions
        for 'buy' events, extracts the buy prices, and then calculates the average buy price. If no
        buy transactions are found, it sets the average buy price to 0.

        Parameters:
            history_list (list): A list containing the transaction history of a product.

        Returns:
            None
        """
        buys = [item for item in history_list if item[1] == 'buy']
        buys_values = [float(txn[-3]) for txn in buys]
        if buys_values:
            ave_buy_value = self.helper_funcs.list_averager(buys_values)
        else:
            ave_buy_value = 0
        print(f"Ave Buy Price is {ave_buy_value}")

    def show_ave_price_sold(self, history_list: list):
        """
        Calculate and display the average sell price of a specific product.

        This function calculates the average sell price of a specific product based on the given
        history_list, which contains the transaction history of the product. It filters the transactions
        for 'sell' events, extracts the sell prices, and then calculates the average sell price. If no
        sell transactions are found, it sets the average sell price to 0.

        Parameters:
            history_list (list): A list containing the transaction history of a product.

        Returns:
            None
        """
        sells = [item for item in history_list if item[1] == 'sell']
        sells_values = [float(txn[-3]) for txn in sells]
        if sells_values:
            ave_sell_value = self.helper_funcs.list_averager(sells_values)
        else:
            ave_sell_value = 0
        print(f"Ave Sell Price is {ave_sell_value}")

    @staticmethod
    def show_txn_count(history_list: list):
        """
        Calculate and display the total, buy and sell number of transactions occurred for a specific product.

        This function calculates the total number of transactions occurred for a specific product
        based on the given history_list, which contains the transaction history of the product. It then
        prints the total number of transactions.

        Parameters:
            history_list (list): A list containing the transaction history of a product.

        Returns:
            None
        """
        txn_count = len(history_list)
        sells = [item for item in history_list if item[1] == 'sell']
        buys = [item for item in history_list if item[1] == 'buy']
        sell_count = len(sells)
        buy_count = len(buys)
        print(f"Number of transactions: {txn_count}")
        print(f"Number of buy transactions: {buy_count}")
        print(f"Number of sell transactions: {sell_count}")

    def show_all_stats(self):
        """
        Author: Vincent Itucal

        Display various statistics for a specific product based on its transaction history.

        This method displays various statistics for a specific product based on its transaction history.
        It first prompts the user to input the Product ID and then checks if the product exists in the
        active inventory. If the product is found, it reads the transaction history of the product and
        calculates and displays the following statistics:
            1. Total Revenue
            2. Total Value Bought
            3. Total Value Sold
            4. Average Buy Price
            5. Minimum and Maximum Buy Prices
            6. Average Sell Price
            7. Minimum and Maximum Sell Prices
            8. Number of Transactions

        Returns:
            None
        """
        self.helper_funcs.clrscr()
        inv_list = [item[0] for item in self.get_active_inventory()]
        input_product_id = input("Input Product ID: ")
        print(f"As of {self.helper_funcs.timestamp_now()} :")
        if input_product_id in inv_list:
            history_list = self.helper_funcs.read_from_file(f"inventory/{input_product_id}.csv")
            self.show_total_revenue(history_list)
            self.show_total_value_bought(history_list)
            self.show_total_value_sold(history_list)
            self.show_ave_price_bought(history_list)
            self.show_max_min_buy_price(history_list)
            self.show_ave_price_sold(history_list)
            self.show_max_min_sell_price(history_list)
            self.show_txn_count(history_list)
        else:
            self.helper_funcs.clrscr()
            print("Product does not exist!")
        self.helper_funcs.click_to_continue()

    def exit_tech_mart(self):
        """
        Exit the Tech Mart application.

        This method sets the 'trigger_exit' attribute to False, indicating that the Tech Mart application
        should exit and terminate.

        Returns:
            None
        """
        self.trigger_exit = False

    def other_choice(self):
        """
        Display the invalid selection message and wait for user input to continue.

        This method is called when the user selects an invalid option from the main menu. It clears the screen,
        displays the "INVALID_SELECTION_MESSAGE" from the constants, and waits for the user to press any key to
        continue.

        Returns:
            None
        """
        self.helper_funcs.clrscr()
        print(self.constants.INVALID_SELECTION_MESSAGE)
        self.helper_funcs.click_to_continue()

    def main(self):
        """
        The main function that represents the TechMart application's main loop.

        This method displays the welcome message and the main menu options. It then waits for the user to input a choice
        and calls the corresponding method based on the user's selection. If the user chooses an invalid option,
        the "other_choice" method is called to display an error message.

        The main loop continues until the "trigger_exit" attribute is set to False, which can be done by selecting
        the "exit_tech_mart" option from the main menu.

        Returns:
            None
        """
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
