# Task 7 – Backward Chaining System (LLM Logic)

This project implements a basic backward chaining system for First Order Logic (FOL) in Python.  
It was developed from scratch as part of Task 7 in the LLM+Logic project.

---

## Features

- Supports rule-based inference with unification
- Evaluates conjunctive goals recursively
- Minimal input format using strings for facts, rules, and queries
- Easy to extend for additional logic functionality

---

## Repository Structure

```
llm-logic-task7/
├── backward_chaining.py         # Main logic engine
├── test_cases.txt               # Sample facts, rules, and queries
├── tutorial/
│   └── task7_writeup.md         # One-page write-up for Task 7
└── README.md
```

---

## How to Run

Run the inference engine using:

```bash
python3 backward_chaining.py
```

The script includes a sample knowledge base and a test query.

---

Query: ancestor(john, alice)
Result: True
```


