### CFGCYK 0.1

##### A CFG library for python.

Use the PhraseStructure class to store grammar rules (CNF) and generate lists of symbols.

CFGCYK allows the symbols in the grammar rules to be any type. As a result, many possibilities arise.

You can even put different instances of PhraseStructure grammar classes inside a PhraseStructure grammar class!

Right now, only grammatical list generation works (this version is a get-it-out-there kinda affair), but some planned features include:

1. CYK algorithm
2. Identifying paths in a grammar that efficiently terminalize a generated symbol list
3. Generating graphs of a grammar
4. A grammar specifying file-type ".grmr", with the ability to take multiple grammar styles and convert them to CNF form before inputting them into the PhraseStructure class.

### Usage

To get us up and running, lets try making (semi-) arbitrary length lists of the character 'a':

    from cfgcyk import PhraseStructure
    
    #Initialize the class
    ps = PhraseStructure()
    
    #Add our intermediate symbol "A".
    ps.add_symbol("A", is_terminal=False)
    
    #Add intermediate rules.
    #Intermediate rules are those which take an intermediate symbol (one that has children)
    ps.add_intermediate_rule(parent_symbol=None, daughter_symbol1="A", daughter_symbol2="A")
    ps.add_intermediate_rule("A", "A", "A")
    
    #Add our terminal symbol
    #Terminal symbols are those which have no children, and essentially act as our desired
    #   output symbols.
    ps.add_symbol("a", is_terminal=True)
    
    #Add our terminal rule
    ps.add_terminal_rule("A", "a")
    
    #Generate a list of terminal symbols
    symbol_list = ps.generate_symbol_string(depth=10, bruteforce=10)
    
    #View our list!
    print(symbol_list)

More information to come with next release.
