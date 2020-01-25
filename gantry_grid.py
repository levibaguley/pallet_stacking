from random import sample
from typing import List, Tuple, Set

from numpy import zeros, int32, nditer, where, ndarray

from order import Order
from segment import Segment



class Gantry:
    """
    Represents a gantry configuration with products from an order in the grid.
    Attributes:
        row_num (int): The number of rows for the gantry grid. Changing the
            number of rows will make new grid filled with zeros
        col_num (int): The number of columns for the gantry grid.
        grid (ndarray): The grid holding the locations of the products,
            pallet building locations and empty locations represented as integers.
            Zeros are in places where there are no pallets.
        empty_rows(Tuple[Segment, ...]): Sections of rows in the grid where no pallets
            should be placed.
        empty_cols(Tuple[Segment, ...]): Sections of columns in the grid where no pallets
            should be placed.
        order(Order): The Order that the gantry needs to fill.
        build_indices(Tuple[Tuple[int, int], ...]): The indices of where the gantry fills
            pallets according to the order

    """
    empty_rows: Tuple[Segment, ...]
    empty_cols: Tuple[Segment, ...]
    build_indices: Tuple[Tuple[int, int], ...]

    def __init__(self):
        self._grid = None
        self.row_num = 1
        self.col_num = 1
        self.empty_rows = ()
        self.empty_cols = ()
        self.build_indices = ()

        self.order = None

    def set_order(self, length, max_prod_type=None) -> None:
        """
        Sets the length of the order and number of unique product types.
        If max_prod_type is not given, it defaults to the number of locations
        where a product pallet can be placed.

        Args:
            length (int): The number of pallets to be put in the order.
            max_prod_type (int): The maximum number of unique product types in the order
        """
        if max_prod_type is None:
            self.order = Order(length, self.spots())
        else:
            self.order = Order(length, max_prod_type)

    @property
    def row_num(self) -> int:
        """
        Provides access to the number of rows in the grid. If changed, updates
        the dimensions (shape) of the grid and fills it with zeros.
        """
        return self._row_num

    @row_num.setter
    def row_num(self, row_num):
        self._row_num = row_num

        # this avoids setting the grid shape with col_num undefined (if in __init__)
        if hasattr(self, "col_num"):
            self._grid = zeros((self._row_num, self.col_num), int32)
        else:
            self._grid = zeros((self._row_num, 1), int32)

    @property
    def col_num(self) -> int:
        """
        Provides access to the number of columns in the grid. If changed, updates
        the dimensions (shape) of the grid and fills it with zeros.
        """
        return self._col_num

    @col_num.setter
    def col_num(self, col_num):
        self._col_num = col_num

        # this avoids setting the grid shape with row_num undefined (if in __init__)
        if hasattr(self, "row_num"):
            self._grid = zeros((self.row_num, self._col_num), int32)
        else:
            self._grid = zeros((1, self._col_num), int32)

    @property
    def grid(self) -> ndarray:
        """
        Provides access to the grid but restricts setting the grid as a whole.

        Notes:
            Grid indices can still be set using: grid[row_index, col_index] = value. \n
            Change the size using col_num and row_num.
        """
        return self._grid

    def set_build_indices(self, option) -> None:
        """
        Sets the locations of where new pallets will be built in the grid.

        Args:
            option(int): If 1, will set to the centers of the edges. If 2, will
                set the spots according to the base case configuration
        """
        # center edges
        if option == 1:
            self.build_indices = ((0, self.col_num // 2),
                                  (self.row_num - 1, self.col_num // 2),
                                  (self.row_num // 2, 0),
                                  (self.row_num // 2, self.col_num - 1))
        # base case configuration
        if option == 2:
            self.build_indices = ((3, 4), (3, 6))

    def set_base_case(self) -> None:
        """
        Sets all the attributes to create the base case configuration.
        """
        self.row_num = 7
        self.col_num = 11
        self.empty_rows = (Segment((2, 0), (2, 10)),)
        self.empty_cols = (Segment((2, 2), (6, 2)),
                           Segment((2, 5), (6, 5)),
                           Segment((2, 8), (6, 8)))
        self.set_build_indices(2)

    def empty_locations(self) -> Set[Tuple[int, int]]:
        """
        Returns:
                empty_locations (Set[Tuple[int, int]]): The locations where absolutely no
                    pallets should be placed. Used for filling functions.
        """
        empty_locations = set()

        if len(self.empty_rows) == 0:
            print("Warning: gantry has zero empty_rows")
        if len(self.empty_cols) == 0:
            print("Warning: gantry has zero empty columns")

        for segment in self.empty_cols:
            empty_locations = empty_locations.union(segment.indices())

        for segment in self.empty_rows:
            empty_locations = empty_locations.union(segment.indices())

        return empty_locations

    def spots(self) -> int:
        """
        Returns:
            object (int): The number of locations where a product pallet can be placed.
        """
        if len(self.build_indices) == 0:
            print("Warning: gantry has zero build indices")

        return (self.grid.size
                - len(self.build_indices)
                - len(self.empty_locations()))

    def fill_by_order(self) -> None:
        """
        Fills the grid randomly using the unique products in the order.
        """
        shuffled_products = sample(self.order.unique_products(),
                                   len(self.order.unique_products()))
        it = nditer(self.grid, flags=['multi_index'], op_flags=['readwrite'])
        index = 0
        while not it.finished:
            if (it.multi_index not in self.build_indices
                    and it.multi_index not in self.empty_locations()):
                it[0] = shuffled_products[index]
                index += 1
            it.iternext()

    def fill_by_product(self) -> None:
        """
        Fills the grid randomly using the maximum number of products.
        """
        shuffled_products = sample(list(range(1, self.spots() + 1)),
                                   self.spots())

        it = nditer(self.grid, flags=['multi_index'], op_flags=['readwrite'])
        index = 0
        while not it.finished:
            if (it.multi_index not in self.build_indices
                    and it.multi_index not in self.empty_locations()):
                it[0] = shuffled_products[index]
                index += 1
            it.iternext()

    def picking_locations(self, pallet_num) -> List[Tuple[int, int]]:
        """
        Args:
            pallet_num (int): The index of a pallet in the order.

        Returns:
            locations: The list of all the locations of the
                products that are needed for the given pallet
        """
        locations: List[Tuple[int, int]] = []
        build_pallet = self.order.order_list[pallet_num]

        for layer in build_pallet.layers:
            location = where(self.grid == layer.type)
            locations += list(zip(location[0], location[1]))

        return locations

    def build_spot_cost(self, pallet_num: int, build_index: Tuple[int, int]) -> int:
        """
        Calculates the number of grid spaces the gantry has to travel in order to
        build a pallet in the order using the max norm of each movement.

        Args:
            pallet_num: The index of a pallet in the order.
            build_index: The 2D index of the spot where the new pallet will be built.

        Returns:
            spot_cost (int):  The distance in units of the number of grid spaces
        """
        spot_cost = 0
        for picking_location in self.picking_locations(pallet_num):
            y_cost = abs(picking_location[0] - build_index[0])
            x_cost = abs(picking_location[1] - build_index[1])
            spot_cost += max(x_cost, y_cost)

        return spot_cost

    def best_build_spot(self, pallet_num) -> Tuple[int, int]:
        """
        Args:
            pallet_num (int): The index of a pallet in the order.

        Returns:
            best_build_spot: The index of the pallet building location that will
                minimize the distance that the gantry has to travel to build the given pallet.
        """
        best_build_spot = None
        # initialize min cost to be larger than it could be
        min_cost = max(self.row_num, self.col_num) * 10

        for build_index in self.build_indices:
            if self.build_spot_cost(pallet_num, build_index) < min_cost:
                best_build_spot = build_index

        return best_build_spot

    def __str__(self):
        """
        Returns:
            str: A string representing the gantry and where products are.
        """
        string = ""

        it = nditer(self.grid, flags=['multi_index'], op_flags=['readwrite'])
        while not it.finished:
            if (it.multi_index not in self.build_indices
                     and it.multi_index not in self.empty_locations()):
                string += str(it[0]).rjust(3)

            elif it.multi_index in self.empty_locations():
                string += ".".rjust(3)
            else:
                string += '\033[01m' + "X".rjust(3) + '\033[01m'

            if it.multi_index[1] == self.col_num-1:
                string += "\n"

            it.iternext()

        return string























