# backward_chaining.py

from typing import List, Tuple

# --- Sample Facts and Rules ---
facts = [
    "parent(john, mary)",
    "parent(mary, alice)"
]

rules = [
    ("parent(x, y)", "ancestor(x, y)"),
    ("ancestor(x, y) and parent(y, z)", "ancestor(x, z)")
]

# --- Helpers ---

def parse_predicate(pred: str) -> Tuple[str, List[str]]:
    name, args = pred.split("(")
    args = args.strip(")").split(",")
    return name.strip(), [a.strip() for a in args]

def unify(goal: str, fact: str) -> dict | None:
    g_name, g_args = parse_predicate(goal)
    f_name, f_args = parse_predicate(fact)
    if g_name != f_name or len(g_args) != len(f_args):
        return None
    subst = {}
    for g, f in zip(g_args, f_args):
        if g.islower():  # variable
            subst[g] = f
        elif g != f:
            return None
    return subst

def apply_subst(pred: str, subst: dict) -> str:
    name, args = parse_predicate(pred)
    new_args = [subst.get(a, a) for a in args]
    return f"{name}({', '.join(new_args)})"

# --- Backward Chaining Logic ---

def bc_ask(query: str, facts: List[str], rules: List[Tuple[str, str]]) -> bool:
    if query in facts:
        return True
    for body, head in rules:
        subst = unify(query, head)
        if subst is None:
            continue
        sub_goals = [p.strip() for p in body.split("and")]
        if all(bc_ask(apply_subst(g, subst), facts, rules) for g in sub_goals):
            return True
    return False

# --- Example Usage ---

if __name__ == "__main__":
    query = "ancestor(john, alice)"
    result = bc_ask(query, facts, rules)
    print(f"Query: {query}")
    print("Result:", result)
