"""
BNF

Stores a BNF grammar in the BNF class.

Used by the grmr file reader to read a file and then convert it
to CNF, for use in the PhraseStructure class.
"""
from .phrase_structure import PhraseStructure

class BNF_Symbol:
    """
    BNF_Symbol.

    Stores the data for a symbol in a BNF grammar.

    Different from PhraseStructureSymbol by having
    rules which produce an arbitrary amount of
    output symbols.

    Functions:
    - __init__(self, symbol, is_terminal)
    - add_rule(self, *produces)
    - add_parent(self, parent_symbol)
    - get_parents(self)
    - get_rules(self)

    Variables:
    - symbol(any): The symbol with which this class is referred to in the handler
    - rules(set(tuple(any)))
    - parents(set(any))
    - is_terminal(bool): Determines whether the symbol can produce other
                         symbols (whether it can have rules)
    """
    def __init__(self, symbol, is_terminal):
        """
        __init__

        Initializes BNF_Symbol class.

        Parameters:
        - symbol(any): The data used to reference this class in BNF
        - is_termianl(bool): Whether or not this symbol takes rules;
                             whether the symbol is terminal.

        Returns:
            None
        """
        self.symbol = symbol
        self.rules = set()
        self.parents = set()
        self.is_terminal = is_terminal


    def add_rule(self, *produces):
        """
        add_rule

        Adds a production rule generated by this symbol.

        Parameters:
        - *produces(any): The symbol references which are produced
                          under this rule.

        Returns:
            int: -1 if the symbol is terminal(doesn't accept rules)
                  0 if the symbol is not terminal, and thus the rule is added.
        """
        if self.is_terminal:
            return -1
        self.rules.add(produces)
        return 0


    def remove_rule(self, *produces):
        """
        remove_rule

        Takes a rule out of the list of rules for this symbol.
        Used in converting to CNF.

        Parameters:
        - *produces(any): the symbols references of the rule
                          being removed.

        Returns:
            int: -1 if the rule specified is not cataloged
                    under this symbol
                  0 otherwise
        """
        if tuple(produces) not in self.rules:
            return -1
        self.rules.remove(tuple(produces))
        return 0


    def remove_parent(self, parent):
        """
        remove_parent

        Removes a parent reference from the symbol.
        Used in converting to CNF.

        Parameters:
        - parent(any): The symbol reference which indicates
                       the parent to be removed.

        Returns:
            int: -1 if parent is not found in list of parents
                  0 otherwise.
        """
        if parent not in self.parents:
            return -1
        self.parents.remove(parent)
        return 0


    def add_parent(self, parent_symbol):
        """
        add_parent

        Adds a parent to the list of parents which can
        produce this symbol.

        Parameters:
        - parent_symbol(any): The symbol reference which
                              refers to the parent added.

        Returns:
            int: 0
        """
        self.parents.add(parent_symbol)
        return 0


    def get_parents(self):
        """
        get_parents

        Returns:
            self.parents(set)
        """
        return self.parents


    def get_rules(self):
        """
        get_rules

        Returns:
            self.rules(set)
        """
        return self.rules


class BNF:
    """
    BNF class.

    Stores a grammar in Backus-Naur form
    and converts it into Chomsky normal form.

    Should be used to assign strings to symbols.
    Do not use integers as symbols... If you need
    a grammar that outputs anything but strings,
    convert to CNF first using the convert_to_cnf
    method after adding tags with the data required.

    Functions:
    - add_symbol(self, symbol, is_terminal)
    - add_terminal_symbol(self, symbol)
    - add_intermediate_symbol(self, symbol)
    - add_rule(self, input_symbol, output_symbols)
    - conversion_start(self)
    - conversion_term(self)
    - conversion_bin(self)
    - conversion_del(self)
    - conversion_unit(self)
    - check_if_cnf(self)
    - convert_to_cnf(self)

    Variables:
        - symbols(dict): Stores symbols mapped to their respective
                         BNF_Symbol class
    """
    def __init__(self):
        """
        __init__

        Initializes the BNF class.

        Creates variables:
        - start_symbol(int): The current start symbol for the class
        - symbols(dict): Mapping of symbol references to BNF_Symbol instances
        - current_term_replacement(int): The term being used in
                                         convert_to_cnf that implements
                                         bin and term intermediate
                                         symbol replacement
        - tags(dict): Assigns symbol references in this class
                      to the symbol references to be outputted
                      in the PhraseStructure instance
                      created by the convert_to_cnf method.
        """
        self.start_symbol = 0
        self.symbols = {0: BNF_Symbol(0, is_terminal=False)}
        self.current_term_replacement = -1
        self.tags = {}


    def add_rule_to_root(self, *rule):
        """
        add_rule_to_root

        Adds a rule to the current start symbol.

        Parameters:
        - *rule(any): The rule to be added.

        Returns:
            None
        """
        self.symbols[self.start_symbol].add_rule(*rule)
        for item in rule:
            self.symbols[item].add_parent(self.start_symbol)


    def add_symbol(self, symbol, is_terminal):
        """
        add_symbol

        Creates a new symbol (instance of BNF_Symbol) to
        store rule and parent relations.

        Parameters:
        - symbol(any): The symbol to be created. Ideally is a
                       string or (internally) an int.
        - is_terminal(bool): indicates whether the symbol is
                             terminal in the grammar. This
                             determines whether the symbol can
                             store rules and produce other symbols.

        Returns:
            int: -1 if symbol already exists
                  0 otherwise
        """
        if symbol in self.symbols:
            return -1
        self.symbols[symbol] = BNF_Symbol(symbol, is_terminal)
        return 0

    def add_terminal_symbol(self, symbol):
        """
        add_terminal_symbol

        Creates a terminal symbol by calling add_symbol with
        is_terminal=False as a parameter.

        Parameters:
        - symbol(any): The symbol to be added. Generally a string
                       or (internal to the class) an int.

        Returns:
            int: return value from add_symbol.
        """
        return self.add_symbol(symbol, is_terminal=True)


    def add_intermediate_symbol(self, symbol):
        """
        add_intermediate_symbol

        Adds an intermediate symbol to the set of symbols.
        (A symbol which can produce other symbols and stores rules)

        Parameters:
        - symbol(any): Generally a string or (internal to this class)
                       an int. The symbol reference used by the BNF
                       class to access the data (rules and parents)
                       under a given symbol.

        Returns:
            int: return value from add_symbol
        """
        return self.add_symbol(symbol, is_terminal=False)


    def add_rule(self, input_symbol, output_symbols_tuple):
        """
        add_rule

        Adds a rule under the BNF_Symbol referenced by input_symbol,
        with the output_symbols_tuple argument describing the production.
        Also adds a parent reference to the products listed under the rule.

        Parameters:
        - input_symbol: The symbol reference which is used to access the BNF_Symbol
                        instance in which the rule is to be stored.
        - output_symbols_tuple:
        """
        if input_symbol not in self.symbols:
            return -3
        if self.symbols[input_symbol].is_terminal:
            return -1
        for symbol in output_symbols_tuple:
            if symbol not in self.symbols:
                return -2
        self.symbols[input_symbol].add_rule(*output_symbols_tuple)
        for symbol in output_symbols_tuple:
            self.symbols[symbol].add_parent(input_symbol)
        return 0


    def does_start_occur_on_right(self):
        for symbol in self.symbols:
            for rule in self.symbols[symbol].get_rules():
                if self.start_symbol in rule:
                    return True
        return False


    def conversion_start(self):
        """
        conversion_start

        Used internally to convert a BNF grammar to a CNF grammar.
        Replaces start terms in rules with new start symbol that
        doesn't occur on the right-hand side.

        Parameters:
            None

        Returns:
            None
        """
        if self.does_start_occur_on_right():
            self.start_symbol = self.start_symbol+1
            self.add_intermediate_symbol(self.start_symbol)
            self.add_rule(self.start_symbol, (self.start_symbol-1,))


    def conversion_term_replacer(self, terminal_product):
        """
        conversion_term_replacer

        Helper method to conversion_term.
        Replaces terminal_product with new element which
        is intermediate, so that a rule does not lead
        to more than one product including terminals,
        which would violate CNF.

        Parameters:
        - terminal_product(any): The symbol reference to be
                                 replaced with an intermediate
                                 symbol.

        Returns:
            int: replacement_id of new intermediate which directs
                 to the terminal being removed.
        """
        replacement_id = self.current_term_replacement
        self.current_term_replacement -= 1
        self.symbols[replacement_id] = BNF_Symbol(replacement_id, is_terminal=False)
        self.symbols[replacement_id].add_rule(terminal_product)
        self.symbols[terminal_product].add_parent(replacement_id)
        return replacement_id


    def check_if_conversion_term_necessary(self, rule):
        has_nonterminals = False
        has_terminals = False
        for item in rule:
            if self.symbols[item].is_terminal:
                has_terminals = True
            else:
                has_nonterminals = True
        return has_nonterminals and has_terminals


    def conversion_term_product_determinalizer(self, parent_symbol, rule):
        """
        conversion_term_product_determinalizer

        conversion_term helper method.
        Calls conversion_term_replacer to replace terminals in rules
        with intermediate rule.

        Parameters:
        - parent_symbol(any): The parent symbol of the rule being determinalized.
        - rule(tuple(any)): The rule under the parent symbol beign determinalized.

        Returns:
            None
        """
        replaced = False
        for item in rule:
            if self.symbols[item].is_terminal:
                replaced = True
                self.conversion_term_replacer(item)
        if replaced:
            self.symbols[parent_symbol].remove_rule(rule)


    def conversion_term(self):
        """
        conversion_term

        Implements the TERM replacement step of the BNF->CNF conversion
        algorithm.

        Parameters:
            None

        Returns:
            None
        """
        old_symbols = set(self.symbols.keys()).copy()
        for symbol in old_symbols:
            old_rules = set(self.symbols[symbol].get_rules()).copy()
            for rule in old_rules:
                if self.check_if_conversion_term_necessary(rule):
                    self.conversion_term_product_determinalizer(symbol, rule)


    def conversion_bin_splitter(self, parent_symbol, rule):
        """
        conversion_bin_splitter

        Helper method to conversion_bin.
        Splits long rules into 2-item rules.

        Parameters:
        - parent_symbol(any): The parent symbol reference of the rule being
                              evaluated.
        - rule(tuple(any)): The given rule being evaluated by this function for
                            splitting.

        Returns:
            set(tuple(any)): The set of 2-tuples of new rules for the given
                             rule argument.
        """
        replacements = set()
        previous_replacement_id = parent_symbol
        replacement_id = self.current_term_replacement
        self.current_term_replacement -= 1
        # self.add_symbol(replacement_id, is_terminal=False)
        for item in rule[:-2]:
            self.add_symbol(replacement_id, is_terminal = False)
            replacements.add((previous_replacement_id, item, replacement_id))
            previous_replacement_id = replacement_id
            replacement_id = self.current_term_replacement
            self.current_term_replacement -= 1
        replacements.add((previous_replacement_id, rule[-2], rule[-1]))
        return replacements


    def is_bin_applicable(self, rule):
        """
        is_bin_applicable

        Helper method to conversion_bin.
        Checks if BIN method in CNF conversion is applicable.
        Counts number of nonterminals to see if nonterminal count
        exceeds 2.

        Parameters:
        - rule(tuple(any)): The rule to be checked for BIN applicability

        Returns:
            bool: whether BIN is applicable (True) or not (False).
        """
        #nonterminals = 0
        #for item in rule:
            #if self.symbols[item].is_terminal is False:
                #nonterminals += 1
        return len(rule)>2#nonterminals > 2


    def conversion_bin(self):
        """
        converison_bin

        Replaces rules of greater than two nonterminals
        with rules of solely two nonterminals.

        Parameters:
            None

        Returns:
            None
        """
        oldsymbols = set(self.symbols.keys()).copy()
        for symbol in oldsymbols:
            oldrules = self.symbols[symbol].get_rules().copy()
            for rule in oldrules:
                if self.is_bin_applicable(rule):
                    replacements = self.conversion_bin_splitter(symbol, rule)
                    for parent, symbol1, symbol2 in replacements:
                        self.symbols[parent].add_rule(symbol1, symbol2)
                        self.symbols[symbol1].add_parent(parent)
                        self.symbols[symbol2].add_parent(parent)
                    self.symbols[symbol].remove_rule(*rule)
                    for item in rule:
                        if self.is_only_subrule_with_daughter(symbol, item):
                            self.symbols[item].remove_parent(symbol)

    def conversion_del(self):
        #We don't accept epsilon-rules in this current scheme,
        # making this function irrelevant for the time being...
        pass

    def is_only_subrule_with_daughter(self, parent_symbol, daughter_symbol):
        """
        is_only_subrule_with_daughter

        Helper method to conversion_unit.
        Checks if a given daughter symbol only occurs once within ruleset
        of parent symbol.

        Parameters:
        - parent_symbol(any): The parent symbol under which the daughter
                              symbol would occur
        - daughter_symbol(any): The daughter symbol whose occurences
                                are being measured by this function.

        Returns:
            bool: Whether rules contain daughter only once.
        """
        is_only_subrule_with_daughter = True
        for rule in self.symbols[parent_symbol].get_rules():
            if daughter_symbol in rule and len(rule) > 1:
                is_only_subrule_with_daughter = False
        return is_only_subrule_with_daughter


    def conversion_unit(self):
        """
        conversion_unit

        Removes unit rules(ones in which a nonterminal is directed to
        another nonterminal).

        Parameters:
            None

        Returns:
            None
        """
        unit_rule_products = set()
        old_symbols = set(self.symbols.keys()).copy()
        for symbol in old_symbols:
            old_rules = set(self.symbols[symbol].get_rules()).copy()
            for rule in old_rules:
                if len(rule) == 1 and self.symbols[rule[0]].is_terminal is False:
                    unit_rule_products.add((symbol, rule[0]))
                    for subrule in self.symbols[rule[0]].get_rules():
                        self.symbols[symbol].add_rule(*subrule)
        for parent, product in unit_rule_products:
            self.symbols[parent].remove_rule(product)
            if self.is_only_subrule_with_daughter(parent, product):
                self.symbols[product].remove_parent(parent)


    def check_if_cnf(self):
        """
        check_if_cnf

        Checks if grammar stored in BNF class instance has been
        converted into CNF yet. Used in convert_to_cnf method
        to determine if CNF has been reached yet by optimal order
        of grammar transformations (START, TERM, BIN, DEL, UNIT)

        Parameters:
            None

        Returns:
            bool: True if CNF, False if not CNF.
        """
        for symbol in self.symbols:
            for rule in self.symbols[symbol].get_rules():
                if len(rule) > 2:
                    return False
                elif len(rule) == 2:
                    if self.symbols[rule[0]].is_terminal:
                        return False
                    if self.symbols[rule[1]].is_terminal:
                        return False
                elif len(rule) == 1:
                    if not self.symbols[rule[0]].is_terminal:
                        return False
        return True


    def add_tag(self, symbol, tag):
        """
        add_tag

        Adds a 'tag' to be outputted for a given symbol.
        Used in converting to CNF PhraseStructure instance
        when PhraseStructure needs to output things other than
        the strings specified in, say, a grammar file (for instance).
        """
        self.tags[symbol] = tag


    def reset_start_symbol_for_cnf(self):
        """
        reset_start_symbol_for_cnf

        Adds tag for start symbol that routes start_symbol
        to None so that start_symbol can be the root value
        for the grammar being generated in CNF.
        (See PhraseStructure class for reference).

        Parameters:
            None

        Returns:
            None
        """
        self.tags[self.start_symbol] = None


    def set_unset_tags(self):
        """
        set_unset_tags

        Gives values to symbols which don't have tags yet
        so that they can be mapped to in resulting PhraseStructure
        instance when using convert_to_cnf method.

        Parameters:
            None

        Returns:
            None
        """
        tag = 0
        for symbol in self.symbols:
            if symbol not in self.tags:
                while tag in self.tags.values():
                    tag += 1
                self.tags[symbol] = tag
        self.reset_start_symbol_for_cnf()


    def create_phrase_structure(self):
        """
        create_phrase_structure

        Creates a PhraseStructure instance using the CNF
        grammar which is converted to with convert_to_cnf
        and subsequently returned by convert_to_cnf.
        Called by convert_to_cnf to get return value.

        Parameters:
            None

        Returns:
            PhraseStructure: PhraseStructure instance of
                             CNF grammar expressed to this
                             BNF instance.
        """
        self.set_unset_tags()
        phrase_structure = PhraseStructure()
        for symbol in self.symbols:
            symbol_tag = self.tags[symbol]
            phrase_structure.add_symbol(symbol_tag, self.symbols[symbol].is_terminal)
        for symbol in self.symbols:
            symbol_tag = self.tags[symbol]
            for rule in self.symbols[symbol].get_rules():
                if len(rule) == 2:
                    phrase_structure.add_intermediate_rule(symbol_tag, self.tags[rule[0]], self.tags[rule[1]])
                elif len(rule) == 1:
                    phrase_structure.add_terminal_rule(symbol_tag, self.tags[rule[0]])
        return phrase_structure


    def convert_to_cnf(self):
        """
        convert_to_cnf

        Converts this BNF instance to a CNF compatible form and
        returns a PhraseStructure instance of this grammar to
        be used for sentence generation and CYK tree identification.

        Parameters:
            None

        Returns:
            None
        """
        while not self.check_if_cnf():
            self.conversion_start()
            self.conversion_term()
            self.conversion_bin()
            self.conversion_del()
            self.conversion_unit()
        return self.create_phrase_structure()
