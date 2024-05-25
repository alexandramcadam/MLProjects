import sys
import copy

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())


    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """

        variables = list(self.crossword.variables)

        for v in variables: #for each variable
            values = self.domains[v].copy() #set of values
            for x in values:
                if len(x) != v.length:
                    self.domains[v].remove(x)



    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """


        #for crossword a conflict is square where variables have different letters

        valuesX = self.domains[x].copy() #set of values of x
        valuesY = self.domains[y].copy() #set of values of y

        overlap = self.crossword.overlaps[x, y] #overlap (i,j)
        mod = False
        ok = False

        if overlap is not None:
            i, j = overlap
            for vX in valuesX:
                for vY in valuesY:
                    if vX[i] == vY[j]: #value satisfies constraint
                        ok = True
                if ok is not True:
                    #if no y value satisfies constraint
                    self.domains[x].discard(vX) #could already be removed, use discard
                    mod = True


        return mod



    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """


        if arcs == None:
            queue = set()

            #set queue to all initial arcs
            for x in self.crossword.variables:
                ns = self.crossword.neighbors(x) #variables with overlap
                for n in ns:
                    if ((x, n) or (n, x)) not in queue:
                        queue.add((x, n)) #add arcs to queue

        else:
            queue = set(arcs)


        while queue != set():
            (x, y) = queue.pop() #remove random arc from queue, tuple

            if self.revise(x, y) == True: #been modified
                if len(self.domains[x]) == 0:
                    return False
                else:
                    for z in self.crossword.neighbors(x):
                        if z != y: # - y
                            queue.add((z,x))


        return True






    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.

        """

        variables = self.crossword.variables
        keys = list(assignment.keys())

        if len(variables) == len(keys):
            return True
        else:
            return False




    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        #consistent with what's already assigned

        keys = list(assignment.keys())
        for k in keys:

            #check words fit
            ns = self.crossword.neighbors(k)
            for n in ns:
                if n in keys:
                    overlap = self.crossword.overlaps[k, n] #overlap (i,j)
                    i, j = overlap
                    if assignment[k][i] != assignment[n][j]: #not consistent
                        return False

            #check length
            if k.length != len(assignment[k]):
                return False


        #check values distinct
        words = list(assignment.values())
        checkWords = list(dict.fromkeys(words)) #remove duplicates if any
        if len(words) != len(checkWords):
            return False


        return True



#complied




    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        values = list(self.domains[var])
        return values



    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        variables = self.crossword.variables
        keys = list(assignment.keys())

        for x in variables:
            if x not in keys:
                return x



    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """


        if self.assignment_complete(assignment) == True:
            return assignment

        else:
            x = self.select_unassigned_variable(assignment)
            for v in self.order_domain_values(x, assignment):
                assignment[x] = v
                if self.consistent(assignment) == True:
                    result = self.backtrack(assignment)
                    if result != None:
                        return result
                    assignment.popitem() #deletes last key

        return None




def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
