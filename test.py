import cplex
import sys

def run_lp_file(filename):
    """A simple function that execute a .lp file thanks to cplex

    Only argument is the file to run.
    """
    c = cplex.Cplex()

    out = c.set_results_stream(None)
    out = c.set_log_stream(None)

    c.read(filename)
    c.solve()

    status = c.solution.get_status()

    if status == 1:
        print(c.variables.get_names())
        print(c.solution.get_values())

    return (c.variables.get_names(), c.solution.get_values())

    c.end() # is this statement reached ? (but impossible to return results if located before)

if __name__ == '__main__':
    run_lp_file("test.lp")