#!/usr/bin/env python3
"""
Copyright (c) 2020 Mykola Dvornik

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

# Based on the "Traveling Santa Problem" tutorial by Stephen Jordan / Microsoft Quantum
# http://quantumalgorithmzoo.org/traveling_santa/

from dwave.system import DWaveSampler, EmbeddingComposite
from collections import defaultdict

# Segments' costs
C = [4.70,
     9.09,
     9.03,
     5.70,
     8.02,
     1.71]

# Total number of segments
N_tot = len(C)

# Required number of segments in the trip
N_req = 4

# Lagrangian multipliers for Constrain I and Constrain II, respectively
l_I = 9
l_II = 30


def QUBO_sum(Q1, Q2):
    return {k: Q1.get(k, 0) + Q2.get(k, 0) for k in set(Q1) | set(Q2)}

def QUBO_guess_chain_strength(Q):
    # contrary to D-Wave recommendations
    # quarter of the absolute maximum of the QUBO coefficients
    # works best here
    return 0.25*abs(max(Q.values(), key=abs))


def QUBO_print(Qn, Q, N):
    print("{}:".format(Qn))
    print(end="\t")
    for i in range(N):
        print("{}".format(i), end="\t")
    print()

    print(end="\t")
    for i in range(N):
        print("―", end="\t")
    print()

    for i in range(N):
        print("{}|".format(i), end="\t")
        for j in range(N):
            print("{}".format(Q.get((i, j), 0)), end="\t")
        print()
    print()


if __name__ == "__main__":
    
    # Set Q for the problem QUBO

    # Goal: minimize trip cost
    Q_goal = defaultdict(int)
    for i in range(N_tot):
        Q_goal[(i, i)] = C[i]

    # Constrain I: there should be N segments in the trip
    Q_cI = defaultdict(int)
    for i in range(N_tot):
        Q_cI[(i, i)] = l_I * (1 - 2 * N_req)
        for j in range(i+1, N_tot):
            Q_cI[(i, j)] = l_I * 2

    # Constrain II: the trip should start and finish at the North Pole
    Q_cII = defaultdict(int)
    for i in range(N_tot):
        Q_cII[(i, i)] = l_II
    Q_cII[(0, 2)] = -l_II * 2
    Q_cII[(1, 3)] = -l_II * 2
    Q_cII[(4, 5)] = -l_II * 2

    QUBO_print("Q_goal", Q_goal, N_tot)
    QUBO_print("Q_cI", Q_cI, N_tot)
    QUBO_print("Q_cII", Q_cII, N_tot)

    Q = QUBO_sum(Q_cI, Q_cII);
    Q = QUBO_sum(Q, Q_goal);

    chain_strength = QUBO_guess_chain_strength(Q)

    print("Chain Strength: {}".format(chain_strength), end="\n\n")

    sampleset = EmbeddingComposite(DWaveSampler()).sample_qubo(
        Q, num_reads=10, chain_strength=chain_strength)
    print(sampleset)
