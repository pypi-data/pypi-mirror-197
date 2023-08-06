import torch
import time
import threading as th
import enigma.sat as sat
from tqdm import tqdm
from queue import Queue

# Initialize.
dtype     = torch.bool
device    = torch.device("cpu")
n_threads = 5000
unsat     = False

# Set device.
def set_device(device_name):
    global device
    device = torch.device(device_name)

# set values in clause tensor.
def set_clause_tensor(clause, cnf, cnf_tensor, literals):

    # Get index.
    clause_index = cnf.index(clause)

    # Loop through literals.
    for literal in clause:

        # Get index.
        literal_index = literals.index(abs(literal))

        # Set to true based on negation.
        if literal > 0: cnf_tensor[clause_index, literal_index, 0] = True
        if literal < 0: cnf_tensor[clause_index, literal_index, 1] = True

# Get cnf tensor.
def get_cnf_tensor(cnf):

    # Get literals.
    literals = sat.get_literals(cnf)

    # Construct tensor.
    cnf_tensor = torch.zeros([len(cnf), len(literals), 2], dtype=dtype, device=device)

    # Loop through clauses.
    for clause in cnf:
        set_clause_tensor(clause, cnf, cnf_tensor, literals)

    return cnf_tensor

# Get cnf from cnf tensor.
def get_cnf(cnf_tensor, literals):

    # Define cnf.
    cnf = []

    # Loop through clauses.
    for clause_index in range(cnf_tensor.size(dim=0)):

        # Get literal tensor.
        literals_tensor = torch.tensor(literals, device=device)

        # Get non negated literals.
        clause_tensor_idy = literals_tensor[cnf_tensor[clause_index,:,0]]

        # Get negated literals.
        clause_tensor_neg = -literals_tensor[cnf_tensor[clause_index,:,1]]

        # Combine clause tensors.
        clause_tensor = torch.cat((clause_tensor_idy, clause_tensor_neg), dim=0)

        # Append clause to cnf.
        cnf.append(clause_tensor.tolist())

    return cnf

# Check satisfiability.
def check_unsat(cnf_tensor):

    # Set access to UNSAT flag.
    global unsat

    # Decide what clauses to keep for unsatisfiability check.
    keep = cnf_tensor.sum(dim=1).sum(dim=1) == 1

    # Only keep relevant clauses for unsatisfiability check.
    cnf_tensor = cnf_tensor[keep]

    # Check if unsatisfiable.
    if torch.any(cnf_tensor, dim=0).all(dim=1).any().item(): unsat = True

# Simplify cnf tensor.
def simplify(cnf_tensor):

    # Set access to UNSAT flag.
    global unsat

    # Check if UNSAT flag is set. If so return.
    if unsat: return cnf_tensor

    # Remove clauses that are always true.
    cnf_tensor = cnf_tensor[torch.logical_not(torch.any(torch.logical_and(cnf_tensor[:,:,0], cnf_tensor[:,:,1]), dim=1)),:,:]

    # Remove duplicate clauses.
    cnf_tensor = torch.unique(cnf_tensor, dim=0)

    return cnf_tensor

# Verify solution tensor.
def verify_tensor(cnf_tensor, solution_tensor):

    # Check if solution tensor is None.
    if solution_tensor == None: return None

    # Get overlap tensor.
    overlap_tensor = torch.logical_and(cnf_tensor, solution_tensor)

    # Evaluate solution.
    result = torch.all(torch.logical_or(torch.any(overlap_tensor[:,:,0], dim=1),torch.any(overlap_tensor[:,:,1], dim=1))).item()

    return result

# Set literal index row to False.
def set_row_to_false(cnf_tensor, literal_index):

    # Set literal index row to False.
    cnf_tensor[:,literal_index,:] = torch.zeros((cnf_tensor.size(dim=0),2), dtype=dtype, device=device)

    return cnf_tensor

# Subroutine to make the pairing function multithreaded.
def pairing_sub(cnf_tensor_idy, cnf_tensor_neg, clause_index, q):

    # Set access to UNSAT flag.
    global unsat

    # Keep trying until memory becomes available.
    while True:
        try:
            # Check if UNSAT flag is set.
            if unsat: break

            # Perform pairing and move to cpu memory.
            q.put(simplify(torch.logical_or(cnf_tensor_idy[clause_index,:,:],cnf_tensor_neg)).cpu())
            break
        except:
            time.sleep(0.1)

# Pairing clauses.
def pairing(cnf_tensor, literal_index):

    # Return None for empty cnf tensor.
    if 0 in cnf_tensor.size(): return None

    # Get clauses that contain literal_index, negated literal_index and the remaining ones. And transfer the remainder to cpu menory.
    cnf_tensor_idy = cnf_tensor[cnf_tensor[:,literal_index,0]]
    cnf_tensor_neg = cnf_tensor[cnf_tensor[:,literal_index,1]]
    cnf_tensor_rem = cnf_tensor[torch.logical_not(torch.logical_or(cnf_tensor[:,literal_index, 0],cnf_tensor[:,literal_index, 1]))].cpu()

    # Return if one tensor is empty.
    if len(cnf_tensor_idy) == 0 or len(cnf_tensor_neg) == 0: return None

    # Set literal index row to False.
    cnf_tensor_idy = set_row_to_false(cnf_tensor_idy, literal_index)
    cnf_tensor_neg = set_row_to_false(cnf_tensor_neg, literal_index)

    # Define thread array and queue.
    threads = []
    q = Queue()

    # Pairing all clause combinations.
    for clause_index in range(0,len(cnf_tensor_idy)):
        t = th.Thread(target=pairing_sub, args=[cnf_tensor_idy, cnf_tensor_neg, clause_index, q])
        t.start()
        threads.append(t)

        # Limit threads.
        if th.active_count() > n_threads:
            time.sleep(1)

    # Wait for threads to finish.
    for t in threads:
        cnf_tensor_rem = torch.cat((cnf_tensor_rem.to(device), q.get().to(device)), dim=0)
        t.join()

    # Simplify cnf tensor in terms of uniqueness of clauses.
    cnf_tensor_rem = torch.unique(cnf_tensor_rem, dim=0)

    # Check if the cnf tensor is unsatisfiable.
    check_unsat(cnf_tensor_rem)

    return cnf_tensor_rem

# Check if clause is essentail or redundant.
def essentail(clause, cnf_tensor, keep):

    # Keep trying until memory becomes available.
    while True:
        try:
            # Determine what clauses are kept for this clause. And update keep tensor.
            keep_clauses = torch.logical_xor(torch.logical_and(cnf_tensor, clause), clause).any(dim=1).any(dim=1)
            keep[keep_clauses.logical_not()] = False
            break
        except:
            time.sleep(0.1)

# Remove redundant clauses from cnf.
def removing(cnf_tensor_up):

    # Define cnf tensor.
    cnf_tensor = None

    # Define necessary tensors.
    counts = torch.add(torch.count_nonzero(cnf_tensor_up[:,:,0], dim=1),torch.count_nonzero(cnf_tensor_up[:,:,1], dim=1))
    keep = torch.ones(cnf_tensor_up.size(dim=0), dtype=dtype, device=device)

    # Get all counts.
    counts_uniq = counts.unique()

    # Loop over counts.
    for count in counts_uniq:

        # Skip counts that dont apply.
        if count == counts_uniq[-1]: continue

        # Get necessary tensors.
        counts = torch.add(torch.count_nonzero(cnf_tensor_up[:,:,0], dim=1),torch.count_nonzero(cnf_tensor_up[:,:,1], dim=1))

        # Get cnf tensors.
        cnf_tensor_eq = cnf_tensor_up[counts == count]
        cnf_tensor_up = cnf_tensor_up[counts > count]

        # Get necessary tensors.
        counts = torch.add(torch.count_nonzero(cnf_tensor_up[:,:,0], dim=1),torch.count_nonzero(cnf_tensor_up[:,:,1], dim=1))
        keep = torch.ones(cnf_tensor_up.size(dim=0), dtype=dtype, device=device)

        # Define thread array.
        threads = []

        # Loop through clauses and decide which clauses to keep.
        for clause_index in range(cnf_tensor_eq.size(dim=0)):
            t = th.Thread(target=essentail, args=[cnf_tensor_eq[clause_index], cnf_tensor_up, keep])
            t.start()
            threads.append(t)

            # Limit threads.
            if th.active_count() > n_threads:
                time.sleep(1)

        # Wait for threads to finish.
        for t in threads:
            t.join()

        # Remove redundant clauses.
        cnf_tensor_up = cnf_tensor_up[keep]

        # Append clauses.
        if cnf_tensor == None: cnf_tensor = cnf_tensor_eq
        else: cnf_tensor = torch.cat((cnf_tensor, cnf_tensor_eq), dim=0)

    # Append clauses.
    if cnf_tensor == None: cnf_tensor = cnf_tensor_up
    else: cnf_tensor = torch.cat((cnf_tensor, cnf_tensor_up), dim=0)

    return cnf_tensor

# Solve cnf tensor.
def tensor_solver(cnf_tensor, literals):

    # Define solution.
    solution = []

    # Define cnf list.
    cnf_list = []

    # Define literals list.
    literals_list = []

    # Set access to UNSAT flag.
    global unsat

    # Set UNSAT flag to false.
    unsat = False

    # Simplify tensor.
    cnf_tensor = simplify(cnf_tensor)

    # Check if the cnf tensor is unsatisfiable.
    check_unsat(cnf_tensor)

    # Append cnf tensor in cnf form.
    cnf_list.append(get_cnf(cnf_tensor, literals))

    # Set literal index.
    pairing_index = 0

    # Print message.
    print('Construct tensors...')

    # Go through all literals.
    for row in tqdm(range(cnf_tensor.size(dim=1))):

        # Check if UNSAT flag is set.
        if unsat: continue

        # Force pairing to happen for one row.
        while pairing_index < cnf_tensor.size(dim=1):

            # Pair clauses.
            cnf_tensor_new = pairing(cnf_tensor, pairing_index)

            # Check if pairing occured.
            if cnf_tensor_new == None:
                pairing_index += 1
            else:

                # Get literal rows that only contain False.
                literal_existing_row = cnf_tensor_new.any(dim=0).any(dim=1)

                # Remove literal rows that only contain False.
                cnf_tensor_new = cnf_tensor_new[:,literal_existing_row,:]

                # Remove literals that are not present in cnf anymore.
                literals_new = []
                literals_remv = []

                # Get remaining and removed literals.
                for literal_index in range(len(literals)):
                    if literal_existing_row[literal_index] == True:
                        literals_new.append(literals[literal_index])
                    else: literals_remv.append(literals[literal_index])

                # Update literals.
                literals = literals_new

                # Append removed literals to list.
                literals_list.append(literals_remv)

                # Remove redundant clauses if activated.
                cnf_tensor_new = removing(cnf_tensor_new)

                # Append cnf tensor in cnf form.
                cnf_list.append(get_cnf(cnf_tensor_new, literals))

                # Set cnf tensor to new cnf tensor.
                cnf_tensor = cnf_tensor_new

                # Adjust pairing index to removed rows.
                pairing_index = 0
                break

    # Check if UNSAT flag is set.
    if unsat: return None

    # Reverse order of cnf list.
    cnf_list.reverse()
    literals_list.reverse()

    # Solve.
    for cnf_index, cnf in enumerate(cnf_list):

        # Adjust cnf to solution and vice versa.
        cnf, solution = sat.adjust_cnf_solution(cnf, solution)

        # Add missing literals to solution.
        for literal in literals_list[cnf_index-1]:

            # Skip for index 0 and literals that are already in solution.
            if cnf_index == 0 or literal in [abs(literal) for literal in solution]: continue
            solution.append(literal)                                # Append literal.
            cnf, solution = sat.adjust_cnf_solution(cnf, solution)  # Adjust cnf to solution and vice versa.

    return solution

# Solve cnf.
def solver(cnf):

    # Define solution for literals that have a opposite negation and a solution for literals that don't.
    solution_neg = []
    solution_sing = []

    # Perform unit propagation on cnf.
    cnf, solution_sing = sat.propagate(cnf, solution_sing)

    # See if there is anything left to solve, otherwise return solution.
    if len(cnf) == 0: return solution_sing

    # Get literals that have opposite negation.
    literals_neg = sat.get_literals(cnf)

    # Get solution for literals that have opposite negation.
    solution_neg = tensor_solver(get_cnf_tensor(cnf), literals_neg)

    # If solution is unsatisfiable return None.
    if solution_neg == None: return None

    # Adjust cnf to solution and vice versa.
    cnf, solution_neg = sat.adjust_cnf_solution(cnf, solution_neg)

    # Combine solutions.
    solution = list(set(solution_sing + solution_neg))

    return solution
