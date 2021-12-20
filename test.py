import cplex
import sys

c = cplex.Cplex()

out = c.set_results_stream(None)
out = c.set_log_stream(None)

c.read("test.lp")
c.solve()

status = c.solution.get_status()

if status == 1:
    print(c.variables.get_names())
    print(c.solution.get_values())

c.end()
