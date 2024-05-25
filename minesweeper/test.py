class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """

        knownMines = set()
        #how to check if cell is a mine?
        if self.count == len(self.cells):
            for cell in self.cells:
                knownMines.add(cell)

        return knownMines



    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """

        knownSafes = set()
        for cell in self.cells:
            #how to check if cell is safe?
            if self.count == 0:
                knownSafes.add(cell)

        return knownSafes

s = Sentence({(1,1),(1,2)}, 0)
print(s.known_safes())
