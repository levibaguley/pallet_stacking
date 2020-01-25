from typing import List

from pallet import Pallet


class Order:
    """
    Represents a list of pallets that need to be created by the gantry.

    Attributes:
        order_list: The list of all the pallets in the order.
    """
    order_list: List[Pallet]

    def __init__(self, length, max_prod_type):
        """
        Create an order of pallets with the number of pallets given.
        
        Args:
            length (int): The number of pallets to be put in the order.
            max_prod_type (int): The maximum number of unique product types in the order
        """
        self.order_list = [Pallet(max_prod_type) for _ in range(length)]

    def __str__(self) -> str:
        """
        Returns:
            str: A string representing the pallets in the order with each line
                representing one pallet.
        """
        return "\n".join(pallet.__str__() for pallet in self.order_list)

    def unique_products(self) -> List[int]:
        """
        Returns:
            List[int]: All the unique product types in the order.
        """
        unique_products = []
        for pallet in self.order_list:
            for layer in pallet.layers:
                if layer.type not in unique_products:
                    unique_products.append(layer.type)
        return unique_products
