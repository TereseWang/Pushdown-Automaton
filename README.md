# Pushdown Automaton 
Implemented a pda running machine 

## PDA Data Representation:
  - A State is a String
  - A Function is a tuple of three strings, with first string represent the
    returning state, second to be the pop and third will be the push to the stack
  - A Transition is a dictionary with key to be the input alpha, value to be
    a List of Function

  A PDA is a python class with fields below:
  - states: a list of States
  - alpha: a list of Chars
  - stack_alpha: a list of Chars
  - stack: a list of Chars
  - transitions: A Dictionary with key to be current state, value to be a
    Transition, for example {q1 : {0 : [(q2, empty, 0)], 1: [(q3, 0, 1)]}}
  - start: A State of states
  - accept: A List of States from states

- Time Spent: 12 hour
- References: TextBook
