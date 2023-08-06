import typing
from time import perf_counter

import numpy as np
from dimod import Sampler, SampleSet, Vartype

from omnisolver.bruteforce.ext.gpu import gpu_search


def _convert_int_to_sample(val, num_variables):
    sample = {}
    for i in range(num_variables):
        sample[i] = val % 2
        val //= 2
    return sample


class BruteforceGPUSampler(Sampler):
    def sample(self, bqm, num_states, suffix_size, grid_size, block_size, dtype=np.float32):
        """Solve Binary Quadratic Model using exhaustive (bruteforce) search on the GPU.

        :param bqm: Binary Quadratic Model instance to solve.
        :param num_states: number of lowest energy states to compute.
        :param suffix_size: exponent l such that 2 ** l is the number of temporarily stored
        :param grid_size: number of blocks for the custom kernels. Note that this parameter
            does not affect the grid on which the Thrust kernels are launched.
        :param block_size: number of threads per block for custom kerneles. Note that this
            parameter does not affect the grid on which the Thrust kernels are launched.
        :param dtype: datatype to use, either np.float32 or np.float64. The default is
            np.flaot32 which on most GPU is significantly faster then 64-bit floating point
            numbers.
        :returns: sample set containing num_states samples.
        """
        if bqm.vartype == Vartype.SPIN:
            return self.sample(
                bqm.change_vartype("BINARY", inplace=False),
                num_states,
                suffix_size,
                grid_size,
                block_size,
            ).change_vartype("SPIN", inplace=False)

        bqm, mapping = bqm.relabel_variables_as_integers()

        qubo_mat = np.zeros((bqm.num_variables, bqm.num_variables), dtype=dtype)

        for (i, j), coef in bqm.quadratic.items():
            qubo_mat[i, j] += coef
            qubo_mat[j, i] += coef

        for i, coef in bqm.linear.items():
            qubo_mat[i, i] = coef

        states_out = np.zeros(num_states, dtype=np.uint64)
        energies_out = np.zeros(num_states, dtype=dtype)

        start_counter = perf_counter()

        gpu_search(
            qubo_mat,
            num_states,
            states_out,
            energies_out,
            grid_size,
            block_size,
            suffix_size,
        )

        solve_time_in_seconds = perf_counter() - start_counter

        samples = [_convert_int_to_sample(state, bqm.num_variables) for state in states_out]

        result = SampleSet.from_samples(
            samples,
            bqm.vartype,
            energies_out + bqm.offset,
            info={"solve_time_in_seconds": solve_time_in_seconds},
        )

        return result.relabel_variables(mapping, inplace=False)

    @property
    def parameters(self) -> typing.Dict[str, typing.Any]:
        return {
            "num_states": [],
            "suffix_size": [],
            "grid_size": [],
            "block_size": [],
            "dtype": [],
        }

    @property
    def properties(self) -> typing.Dict[str, typing.Any]:
        return {}
