from random import randint, sample, choice
from typing import List
from random import choices
from itertools import accumulate



class Product:
    """
    Represents a product on a pallet.
    This class is a will hold more data in the future for things like product weight, frequency etc.

    Attributes:
        type (int): A number representing product type (cheese, meat ect).
    """

    def __init__(self):
        self.type = 0


class Pallet:
    """
    Represents a pallet with layers of different products

    Attributes:
        layers(List[Product]): The products that are on the pallet.
    """
    layers: List[Product]

    def __init__(self, max_prod_type):
        """

        Args:
            max_prod_type (int): The maximum number of unique product types possible
        """
        self.layers = []
        self.frequencies = []
        self.product_types = list(range(1, max_prod_type + 1))

        self.frequencies = [.10 / 51] * 51
        self.frequencies.append(.9)

        # self.rand_fill()
        self.rand_fill_by_one()

    def rand_fill(self) -> None:
        """
        Fills the pallets 9 layers high with random types of products
        and random number of layers for each type.
        """

        types = self.product_types[:]

        while len(self.layers) < 9:
            product = Product()
            product.type = sample(types, 1)[0]
            # don't pick the same type again
            del types[types.index(product.type)]

            layers_left = 9 - len(self.layers)

            quantity = 0
            # if pallet is not empty
            if len(self.layers) > 0:
                quantity = randint(1, layers_left)
            # if pallet is empty don't fill it completely
            elif len(self.layers) == 0:
                quantity = randint(1, 8)

            self.layers.extend([product] * quantity)

    def rand_fill_by_one(self) -> None:
        """
        Fills the pallet with random non-repeating products
        """
        random_layers = sample(range(1, len(self.product_types) + 1), 9)
        for random_type in random_layers:
            random_product = Product()
            random_product.type = random_type
            self.layers.append(random_product)

    def dist_fill_by_one(self) -> None:
        """
        Fills the pallet with non-repeating products according
        to the product frequency
        """
        # convert frequencies to a cumulative list to speed up the choices function
        cum_freq = list(accumulate(self.frequencies))
        types = self.product_types[:]

        for layer in range(9):
            new_product = Product()
            new_type = choices(types, cum_weights=cum_freq)[0]
            new_product.type = new_type
            self.layers.append(new_product)
            type_index = types.index(new_type)

            # delete the product and its frequency to not pick it again
            del types[type_index]
            del cum_freq[type_index]

    def __str__(self) -> str:
        """
        Returns:
            str: A string representing the pallet's layers
        """
        return ', '.join(str(layer.type) for layer in self.layers)
