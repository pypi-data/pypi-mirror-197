# Verify potential solution to cnf with true of false.
def verify(cnf, solution):

    # See if solution is None.
    if solution==None: return None

    # Check every clause.
    for clause in cnf:

        # Check if the solution satesfies the clause.
        if set(clause).isdisjoint(solution): return False

    # Return true if succesful.
    return True

# Verify which clauses are not satisfied yet and return them.
def verify_partial(cnf, solution):

    # See if solution is None.
    if solution==None: return None

    # Define new cnf.
    cnf_new = []

    # Check every clause.
    for clause in cnf:

        # Check if the solution satesfies the clause.
        if set(clause).isdisjoint(solution): cnf_new.append(clause)

    # Return new cnf.
    return cnf_new

# Returns new literal not yet found in the input or cnf.
def new_literal(input, cnf, avoid=None):

    # Initialize avoid.
    if avoid == None: avoid = []

    # Get literals from input.
    literals = list(set([abs(i) for i in input]))

    # Append literals from avoid.
    literals = list(set(literals) | set(avoid))

    # Add literals from cnf.
    for j in range(len(cnf)):
        literals = list(set(literals) | set([abs(i) for i in cnf[j]]))

    # Generate literal not yet found in input or cnf.
    if literals == []: return 1
    return literals[-1]+1

# Get literals.
def get_literals(cnf):

    # Define literals and solution literals.
    literals = []

    # Get literals.
    [[literals.append(abs(literal)) for literal in clause] for clause in cnf]

    return list(set(literals))

# Get literal assignments that do not have a negation within the cnf.
def get_solution_singular(cnf):

    # Define literals and solution literals.
    literals = []

    # Define solution.
    solution = []

    # Get literals.
    [[literals.append(literal) for literal in clause] for clause in cnf]
    literals = list(set(literals))

    # Get solution.
    [solution.append(literal) for literal in literals if -literal not in literals]

    return list(set(solution))

# Perform unit propagation on cnf and give partial solution.
def propagate(cnf, solution_part):

    while True:

        # Get literals that do not have a opposite negation.
        solution_app = get_solution_singular(cnf)

        # Quit if there are no new literals to be added.
        if len(solution_app) == 0: break

        # Append new literals.
        solution_part = list(set(solution_part+solution_app))

        # Remove clauses that are satisfied by solution, while the rest remians.
        cnf = verify_partial(cnf, solution_part)

    return cnf, solution_part

# Adjust cnf by removing literals set to False.
def set_false_literals(cnf, solution):

    # Get inverted solution.
    solution_inv = [-literal for literal in solution]

    # Check every clause.
    for clause in cnf:
        [clause.remove(literal) for literal in solution_inv if literal in clause]

    return cnf

# Adjust cnf to solution and vice versa.
def adjust_cnf_solution(cnf, solution):

    # Remove clauses that are satisfied.
    cnf = verify_partial(cnf, solution)

    # Remove literals set to False.
    cnf = set_false_literals(cnf, solution)

    # Perform unit propagation on cnf.
    cnf, solution = propagate(cnf, solution)

    return cnf, solution
