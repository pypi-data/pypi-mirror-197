import numpy as np
from dimod import BQM

from omnisolver.bruteforce.gpu import BruteforceGPUSampler


def random_bqm(num_variables, vartype, offset, rng):
    linear = {i: rng.uniform(-2, 2) for i in range(num_variables)}
    quadratic = {
        (i, j): rng.uniform(-1, 1)
        for i in range(num_variables)
        for j in range(i + 1, num_variables)
    }
    return BQM(linear, quadratic, offset, vartype=vartype)

N = 40
bqm = random_bqm(N, "BINARY", 0, np.random.default_rng(1234))
sampler = BruteforceGPUSampler()
result = sampler.sample(bqm, 100, 24, 2**11, 256, np.float32)

print(result)
