from .rules import recursive_parse, parse_rule
from qiskit import QuantumCircuit, execute, Aer
import re

class QuantumRuleBasedSystem(object):
    """
        Creates a new quantum rule-based system.
    """

    def __init__(self, operators=None):

        self._rules = []
        self._clauses = []
        self._rule_terms = []
        self._circuit_terms = []
        self._constants = []
        self._operators = operators

    def add_rules(self, rules):
        """
        Adds new rules to the quantum rule-based system.
        Args:
            rules: list of rules to be added to QRBS. Rules must be specified as strings, with defined syntax.
        """
        for rule in rules:
            antecedent, consequent = parse_rule(rule)
            recursive_parse(antecedent, self)
            self._rules.append([antecedent, consequent])
        clauses = self._clauses
        rule_terms = self._rule_terms
        qubits = (len(clauses) + len(rule_terms))
        print("* Added rule IF", antecedent,
                  "THEN", consequent)
        return rule_terms, qubits
    
    def evaluate_rules(self, rule_terms, qubits):
        """
        Evaluates rules using quantum rule-based system.
        Args:
            rule_terms: terms that make up the rules to be translated to the quantum circuit.
            qubits: nummber of qubits to add to quantum register in the quantum circuit.
        """
        circuit = QuantumCircuit(qubits, 1)
        for term in rule_terms[::-1]:
            lhs = re.sub(r'[()]', '', term[0])
            rhs = re.sub(r'[()]', '', term[1])
            sides = [lhs, rhs]
            operator = term[2]
            for side in sides:
                if side not in self._circuit_terms: 
                    self._circuit_terms.append( side )
                    circuit.h(self._circuit_terms.index( side ))
            if operator == 'AND': 
                self._circuit_terms.append( '%s %s %s' % (lhs, operator, rhs) )
                circuit.ccx(self._circuit_terms.index( lhs ), self._circuit_terms.index( rhs ), self._circuit_terms.index( '%s %s %s' % (lhs, operator, rhs) )) 
            elif operator == 'OR':
                self._circuit_terms.append( '%s %s %s' % (lhs, operator, rhs) )
                circuit.ccx(self._circuit_terms.index( lhs ), self._circuit_terms.index( rhs ), self._circuit_terms.index( '%s %s %s' % (lhs, operator, rhs) )) 
                circuit.cx(self._circuit_terms.index( lhs ), self._circuit_terms.index( '%s %s %s' % (lhs, operator, rhs) )) 
                circuit.cx(self._circuit_terms.index( rhs ), self._circuit_terms.index( '%s %s %s' % (lhs, operator, rhs) )) 
        circuit.measure((qubits - 1), 0)
        simulator = Aer.get_backend('qasm_simulator')
        job = execute(circuit, simulator, shots=1000)
        result = job.result()
        counts = result.get_counts(circuit)['1']
        probability = counts / 1000
        print("* Probability of outcome: ", probability)
        return probability
