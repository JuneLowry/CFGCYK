"""
CYK

Contains the CYK class, which determines whether a given
list of symbols is within a given PhraseStructure class's grammar.
"""
from .phrase_structure import PhraseStructure


class CYK:
    """
    CYK:

    A class for determining if a list of symbols is grammatical.

    Functions:
    - __init__(self, phrase_structure): Initializes cyk by linking it
                                        to a pre-existing grammar.
    - fits_grammar(self, symbol_list): Checks whether a symbol list
                                       follows the grammar specified
                                       in the phrase structure class
                                       provided.
    - get_previous_tree(self): Returns the possible trees for the
                               previous call to fits_grammar.
                               Returns a list of length zero when
                               the previous fits_grammar call was
                               False.

    Variables:
    - cyk_table(list(list(set))): Stores information used in the CYK algorithm.
    - phrase_structure(PhraseStructure): Stores the grammar to be evaluated.
    """
    def generate_cyk_table(self, size):
        """
        generate_cyk_table

        Generates the cyk table when called by fits_grammar,
        stored in self.cyk_table

        Parameters:
            size(int): The length of the symbol list being evaluated

        Returns:
            None
        """
        self.cyk_table = []
        for i in range(size):
            self.cyk_table.append([])
            for j in range(size-i):
                self.cyk_table[i].append(set())


    def __init__(self, phrase_structure):
        """
        __init__

        Initializes class instance with specified CNF grammar
        stored in PhraseStructure instance provided as an argument.

        Parameters:
        - phrase_structure(PhraseStructure): The CNF grammar used for
                                             evaluating inputted symbol lists
        """
        self.cyk_table = None
        self.phrase_structure = phrase_structure


    def get_cyk_pairs(self, row, column):
        """
        get_cyk_pairs

        For a given row and column entry, finds the relevant pairs
        to be compared to find a parent rule.

        Parameters:
        - row(int): The row of the entry being evaluated
        - column(int): The column of the entry being evaluated

        Returns:
            set: Pairs (2-tuples) of symbols to be checked for common parent rule
        """
        pairs = set()
        for left_i in range(row):
            left_j = column
            right_j = column+left_i+1
            right_i = row-left_i-1
            for item1 in self.cyk_table[left_i][left_j]:
                for item2 in self.cyk_table[right_i][right_j]:
                    pairs.add((item1, item2))
        return pairs


    def get_common_parents(self, item1, item2):
        """
        get_common_parents

        Finds the intersection of parents between symbols item1 and item2.

        Parameters:
        - item1(any): symbol of first item to find parents for.
        - item2(any): symbol of second item to find parents for.

        Returns:
            set: parent symbols in common between item1 and item2
        """
        parents1 = self.phrase_structure.symbols[item1].get_parents()
        parents2 = self.phrase_structure.symbols[item2].get_parents()
        return parents1.intersection(parents2)


    def fill_cyk_row(self, row):
        """
        fill_cyk_row

        Fills a row of the CYK table following CYK algorithm.

        Parameters:
            row(int): the row index to be filled

        Returns:
            None
        """
        width = len(self.cyk_table[row])
        for column in range(width):
            pairs = self.get_cyk_pairs(row, column)
            for item1, item2 in pairs:
                for parent in self.get_common_parents(item1, item2):
                    if (item1, item2) in self.phrase_structure.symbols[parent].get_rules():
                        self.cyk_table[row][column].add(parent)


    def fits_grammar(self, symbol_list):
        """
        fits_grammar

        Determines whether a list of symbols (symbol_list argument) fits the
        given PhraseStructure instance's grammar.

        Parameters:
        - symbol_list(list(any)): The list of symbols to be evaluated.

        Returns:
            bool: Whether symbol_list fits PhraseStructure instance's grammar
        """
        size = len(symbol_list)
        self.generate_cyk_table(size)
        for column in range(size):
            for parent in self.phrase_structure.symbols[symbol_list[column]].get_parents():
                self.cyk_table[0][column].add(parent)
        for row in range(1, size):
            self.fill_cyk_row(row)
        head = self.cyk_table[-1][0]
        return None in head


    def get_tree(self, symbol_list):
        size = len(symbol_list)
        self.generate_cyk_table(size)
        for column in range(size):
            for parent in self.phrase_structure.symbols[symbol_list[column]].get_parents():
                self.cyk_table[0][column].add(parent)
        for row in range(1, size):
            
