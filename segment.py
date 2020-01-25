from typing import Tuple, Set


class Segment:
    """
    Represents a section in a 2D grid. Indices are tuples taken as: (row_index, column_index)
    with indices starting at 0.

    Attributes:
        start_index (Tuple[int, int]): The starting point of the segment, inclusive.

        end_index (Tuple[int, int]): The ending point of the segment, inclusive.
    """
    start_index: Tuple[int, int]
    end_index: Tuple[int, int]

    def __init__(self, start_index, end_index):
        self.start_index = start_index
        self.end_index = end_index

        self.check_start_end()

    def indices(self) -> Set[Tuple[int, int]]:
        """
        Returns:
            indices: All the indices along the segment including the ends.
        """
        indices = set()
        if self.start_index == self.end_index:
            indices.add(self.start_index)

        # column segment
        elif self.start_index[0] == self.end_index[0]:
            for col_index in range(self.start_index[1], self.end_index[1] + 1):
                empty_location = (self.start_index[0], col_index)
                indices.add(empty_location)

        # row segment
        elif self.start_index[1] == self.end_index[1]:
            for row_index in range(self.start_index[0], self.end_index[0] + 1):
                empty_location = (row_index, self.start_index[1])
                indices.add(empty_location)

        return indices

    def check_start_end(self) -> None:
        """
        Raises:
            IndexError: If indices are not in the same column or row, or if they are not
                given as top index first or left-hand index first.

        """
        if (self.start_index[0] != self.end_index[0] and
                self.start_index[1] != self.end_index[1]):
            raise IndexError("Starting and ending indices must be in the same column or row")

        elif (self.start_index[0] == self.end_index[0] and
              self.start_index[1] > self.end_index[1]):
            raise IndexError("Starting column index is greater than ending column index.")

        elif (self.start_index[1] == self.end_index[1] and
              self.start_index[0] > self.end_index[0]):
            raise IndexError("Starting row index is greater than ending row index.")
