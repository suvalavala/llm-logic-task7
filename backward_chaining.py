from typing import List, Tuple, Dict, Optional


facts = [
    "parent(john, mary)",
    "parent(mary, alice)"
]

rules = [
    ("parent(x, y)", "ancestor(x, y)"),
    ("ancestor(x, y) and parent(y, z)", "ancestor(x, z)")
]


def parse_predicate(pred: str) -> Tuple[str, List[str]]:
    name, args = pred.split("(")
    args = args.strip(")").split(",")
    return name.strip(), [a.strip() for a in args]

def unify(goal: str, fact: str) -> Optional[Dict[str, str]]:
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

def apply_subst(pred: str, subst: Dict[str, str]) -> str:
    name, args = parse_predicate(pred)
    new_args = [subst.get(a, a) for a in args]
    return f"{name}({', '.join(new_args)})"

def merge_subst(s1: Dict[str, str], s2: Dict[str, str]) -> Optional[Dict[str, str]]:
    result = s1.copy()
    for k, v in s2.items():
        if k in result and result[k] != v:
            return None
        result[k] = v
    return result

# Backward Chaining Logic 

def bc_ask(query: str, facts: List[str], rules: List[Tuple[str, str]], visited=None) -> bool:
    if visited is None:
        visited = set()
    if query in visited:
        return False
    visited.add(query)

    # Check if query directly matches any fact
    for fact in facts:
        if unify(query, fact):
            return True

    for body, head in rules:
        head_subst = unify(query, head)
        if head_subst is None:
            continue
        sub_goals = [s.strip() for s in body.split("and")]
        if all(bc_ask(apply_subst(sub_goal, head_subst), facts, rules, visited.copy()) for sub_goal in sub_goals):
            return True

    return False


if __name__ == "__main__":
    query = "ancestor(john, alice)"
    result = bc_ask(query, facts, rules)
    print(f"Query: {query}")
    print("Result:", result)

# exp output
# Query: ancestor(john, alice)
# Result: True
