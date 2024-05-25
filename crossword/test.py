values = {'SATISFACTION', 'OPTIMIZATION', 'INTELLIGENCE', 'DISTRIBUTION'}

values.remove('SATISFACTION')
print(values)


"""


        variables = self.crossword.variables
        print(assignment)

        for v in variables:
            if assignment[v] == None: #key error
                return False

        return True


                variables = self.crossword.variables
                keys = list(assignment.keys())

                if len(keys) == len(variables):
                    for k in keys:
                        if assignment[k] == None: #key error
                            return False
                else:
                    return False #not added all variables

                return True
"""

        #variables = self.crossword.variables
        #for x in variables:

            #check words fit
            #ns = self.crossword.neighbors(x)
            #for n in ns:
            #    overlap = self.crossword.overlaps[x, n] #overlap (i,j)
            #    i, j = overlap
            #    if assignment[x][i] != assignment[n][j]: #not consistent #ERROR
            #        return False

            #check length
            #if x.length != len(assignment[x]):
            #    return False
