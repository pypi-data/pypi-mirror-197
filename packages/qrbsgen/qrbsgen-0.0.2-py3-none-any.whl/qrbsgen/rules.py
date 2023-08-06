import re

regex_clause_with_parentheses = re.compile(r"^\(\w*\s*IS\s*\w*\)$")
regex_clause_without_term= re.compile(r"[a-zA-Z]")
regex_clause = re.compile(r"^\w*\s*IS\s*\w*$")


# Operator definitions
def OR(x,y): return max(x, y)
def AND(x,y): return min(x, y)
def NOT(x): return 1.-x

# Clause class
class Clause(object):
    def __init__(self, variable, term=-1):
        self._variable = variable
        self._term = term
    def __repr__(self):
        if self._term == -1: return "c.(%s)" % (self._variable)
        else: return "c.(%s IS %s)" % (self._variable, self._term)

# Functional class
class Functional(object):
    def __init__(self, fun, A, B, operators=None):
        self._A = A
        self._B = B
        if fun=="NOT":
            if B == "": raise Exception("Second operand missing")
        elif A == "": raise Exception("First operand missing")
        if operators is None:
            self._fun = fun
        else:
            self._fun = fun
    def __repr__(self):
        return "f.(" + str(self._A) + " " + self._fun + " " + str(self._B) + ")"

# Parse rule function - extract antecedent and consequent
def parse_rule(rule):
    if rule.find("THEN") == -1:
        raise Exception("ERROR: badly formatted rule, please check syntax.\n"
                        + rule)
    antecedent = rule[rule.find("IF")+2:rule.find(" THEN")].strip()
    consequent = rule[rule.find(" THEN")+5:].strip(" ")
    return antecedent, consequent

# Find index of operator function - returns index position of operator
def find_index_operator(string):
    pos = 0
    par = 1
    while(par>0):
        pos+=1
        if string[pos]==")": par-=1
        if string[pos]=="(": par+=1
    pos2 = pos
    while(string[pos2]!="("):
        pos2+=1
    return pos+1, pos2

# Recursive parse function - recursively processes rule clauses
def recursive_parse(text, self, operators=None): 
    text = text.strip()
    if text=="" or text=="()": 
        raise Exception("ERROR: emtpy clauses not allowed") 
    if regex_clause.match(text):
        variable = text[:text.find(" IS")].strip()
        term     = text[text.find(" IS")+3:].strip()
        self._clauses.append( variable )
        clause = Clause(variable, term)
        return clause
    if regex_clause_without_term.match(text):
        variable = text
        self._clauses.append( variable )
        clause = Clause(variable)
        return clause
    elif regex_clause_with_parentheses.match(text):
        variable = text[1:text.find(" IS")].strip()
        term     = text[text.find(" IS")+3:-1].strip()
        self._clauses.append( variable )
        clause = Clause(variable, term)
        return clause
    else:
        if text[:3]=="NOT":
            beginindop = 0
            endindop = 3
        elif text[:4]=="(NOT":
            text = text[1:-1]
            beginindop = 0
            endindop = 3
        else:
            try:
                beginindop, endindop = find_index_operator(text)
            except IndexError:
                try: 
                    if text[0] == "(" and text[-1] == ")": 
                        text = text[1:-1]
                        return recursive_parse(text, self, operators=operators)
                    else: 
                        raise Exception("ERROR: badly formatted rule, please check capitalization and syntax.\n"
                        + " ---- PROBLEMATIC RULE:\n"
                        + text)
                except: 
                    raise Exception("ERROR: badly formatted rule, please check capitalization and syntax.\n"
                        + " ---- PROBLEMATIC RULE:\n"
                        + text)
        firsthalf = text[:beginindop].strip()
        secondhalf = text[endindop:].strip()
        operator = text[beginindop:endindop].strip()
        if operator.find(" ")>-1: 
            raise Exception("ERROR: operator %s invalid: cannot use spaces in operators" % operator)
        self._rule_terms.append( [firsthalf, secondhalf, operator] )
        try:
            novel_fun = Functional(operator, 
            recursive_parse(firsthalf, self, operators=operators), 
            recursive_parse(secondhalf, self, operators=operators), 
        operators=operators)
        except:
            raise Exception("ERROR: badly formatted rule, please check capitalization and syntax.\n"
                    + " ---- PROBLEMATIC RULE:\n"
                    + text)
        return novel_fun