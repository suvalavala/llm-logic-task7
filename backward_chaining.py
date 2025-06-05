from typing import List, Tuple, Dict, Optional, Set
import re

# --- Extended  Facts and Rules ---
facts = [
    "parent(john, mary)",
    "parent(mary, alice)",
    "parent(alice, bob)",
    "parent(bob, charlie)",
    "parent(susan, tom)",
    "parent(tom, jerry)",
    "male(john)",
    "male(bob)", 
    "male(charlie)",
    "male(tom)",
    "male(jerry)",
    "female(mary)",
    "female(alice)",
    "female(susan)"
]

rules = [
    ("parent(X, Y)", "ancestor(X, Y)"),
    ("ancestor(X, Y) and parent(Y, Z)", "ancestor(X, Z)"),
    ("parent(X, Y) and male(X)", "father(X, Y)"),
    ("parent(X, Y) and female(X)", "mother(X, Y)"),
    ("parent(X, Y) and parent(X, Z) and Y != Z", "sibling(Y, Z)"),
    ("ancestor(X, Y) and ancestor(X, Z) and Y != Z", "related(Y, Z)")
]

# ---  Helpers ---

def parse_predicate(pred: str) -> Tuple[str, List[str]]:
    """Parse predicate into name and arguments."""
    name, args = pred.split("(", 1)
    args = args.rstrip(")").split(",")
    return name.strip(), [a.strip() for a in args]

def is_variable(term: str) -> bool:
    """Check if term is a variable (starts with uppercase or is single lowercase in some contexts)."""
    return term[0].isupper() or len(term) == 1

def unify(term1: str, term2: str, subst: Dict[str, str] = None) -> Optional[Dict[str, str]]:
    """Unify two terms with existing substitution."""
    if subst is None:
        subst = {}
    
    # Apply existing substitutions
    term1 = subst.get(term1, term1)
    term2 = subst.get(term2, term2)
    
    if term1 == term2:
        return subst
    elif is_variable(term1):
        new_subst = subst.copy()
        new_subst[term1] = term2
        return new_subst
    elif is_variable(term2):
        new_subst = subst.copy()
        new_subst[term2] = term1
        return new_subst
    else:
        return None

def unify_predicates(pred1: str, pred2: str) -> Optional[Dict[str, str]]:
    """Unify two predicates."""
    try:
        name1, args1 = parse_predicate(pred1)
        name2, args2 = parse_predicate(pred2)
        
        if name1 != name2 or len(args1) != len(args2):
            return None
        
        subst = {}
        for arg1, arg2 in zip(args1, args2):
            subst = unify(arg1, arg2, subst)
            if subst is None:
                return None
        
        return subst
    except:
        return None

def apply_substitution(pred: str, subst: Dict[str, str]) -> str:
    """Apply substitution to predicate."""
    name, args = parse_predicate(pred)
    new_args = [subst.get(arg, arg) for arg in args]
    return f"{name}({', '.join(new_args)})"

def get_variables(pred: str) -> Set[str]:
    """Get all variables in a predicate."""
    _, args = parse_predicate(pred)
    return {arg for arg in args if is_variable(arg)}

# --- BCL---

def bc_ask(query: str, facts: List[str], rules: List[Tuple[str, str]], 
           subst: Dict[str, str] = None, visited: Set[str] = None) -> bool:
    """
    Backward chaining ask with proper variable handling.
    """
    if subst is None:
        subst = {}
    if visited is None:
        visited = set()
    
    # Apply current substitution to query
    ground_query = apply_substitution(query, subst)
    
    # Prevent infinite recursion
    if ground_query in visited:
        return False
    visited.add(ground_query)
    
    # Check if query matches any fact
    for fact in facts:
        if unify_predicates(ground_query, fact) is not None:
            return True
    
    # Try to prove using rules
    for rule_body, rule_head in rules:
        # Try to unify query with rule head
        head_unification = unify_predicates(ground_query, rule_head)
        if head_unification is None:
            continue
        
        # Parse rule body (handle conjunctions)
        if " and " in rule_body:
            subgoals = [goal.strip() for goal in rule_body.split(" and ")]
        else:
            subgoals = [rule_body.strip()]
        
        # Apply head unification to all subgoals
        instantiated_subgoals = []
        for subgoal in subgoals:
            # Skip inequality constraints for now (simplified)
            if "!=" in subgoal:
                continue
            instantiated_subgoals.append(apply_substitution(subgoal, head_unification))
        
        # Try to prove all subgoals
        if all(bc_ask(subgoal, facts, rules, head_unification, visited.copy()) 
               for subgoal in instantiated_subgoals):
            return True
    
    return False

# --- Few Tests ---

def run_tests():
    """Run comprehensive tests."""
    test_queries = [
        "ancestor(john, alice)",      # True
        "ancestor(john, bob)",        # True  
        "ancestor(john, charlie)",    # True
        "ancestor(alice, john)",      # False
        "ancestor(susan, jerry)",     # True
        "father(john, mary)",         # True
        "mother(mary, alice)",        # True
        "father(mary, alice)",        # False
        "related(alice, bob)",        # Should be True (both descended from john)
        "father(john, alice)"         # False
    ]
    
    print("=== Backward Chaining Test Results ===\n")
    
    for query in test_queries:
        result = bc_ask(query, facts, rules)
        print(f"Query: {query}")
        print(f"Result: {result}")
        print()

if __name__ == "__main__":
    run_tests()



"""
exp output
=== Backward Chaining Test Results ===

Query: ancestor(john, alice)
Result: True

Query: ancestor(john, bob)
Result: True

Query: ancestor(john, charlie)
Result: True

Query: ancestor(alice, john)
Result: False

Query: ancestor(susan, jerry)
Result: True

Query: father(john, mary)
Result: True

Query: mother(mary, alice)
Result: True

Query: father(mary, alice)
Result: False

Query: related(alice, bob)
Result: True

Query: father(john, alice)
Result: False
"""
