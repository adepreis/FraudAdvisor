\ >> PATH_TO_CPLEX\cplex\bin\x64_win64\cplex.exe
\ >> read test.lp
\ >> opt
\ >> display solution variables *


\problem name
        maximize
                obj: x1 + x2 + x3
        subject to
                c1: x1-x3 <= 3
                c2: x1+x2 >= 1.5
        bounds
                0 <= x1 <= 1
                0 <= x2 <= 5
                1 <= x3 <= 2
end
