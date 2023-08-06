import dimod
import numpy as np

from omnisolver.bruteforce.ext.gpu import gpu_search

NUM_STATES = 1000

def main():
    with open("../instances/instance_36_1.txt") as f:
        instance = dimod.BQM.from_coo(f, vartype="SPIN")
    print(instance)
    instance.scale(-1)
    instance.relabel_variables({i: i - 1 for i in instance.variables})

    mat = instance.to_numpy_matrix()

    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            mat[j, i] = mat[i, j]
    qubo = instance.change_vartype("BINARY", inplace=False)
    states_out = np.empty(NUM_STATES, dtype=np.uint64)
    energies_out = np.empty(NUM_STATES, dtype=np.float32)

    inpt = mat.astype(np.float32)

    from time import time
    gpu_search(inpt, NUM_STATES, states_out, energies_out, 2 ** 15, 256, suffix_size=25)

    start = time()
    gpu_search(inpt, NUM_STATES, states_out, energies_out, 2 ** 15, 256, suffix_size=25)
    stop = time()
    print(f"Elapsed: {stop - start}")

    idx = np.argmin(energies_out)

    energy = energies_out[idx]
    state = states_out[idx]
    print(list(energies_out + qubo.offset)[:10])
    actual_energies = []
    for state in states_out[:10]:
        state_dict = {}
        for i in range(qubo.num_variables):
            state_dict[i] = 2 * (int(state) & 1) - 1
            state //= 2
        actual_energies.append(instance.energy(state_dict))

    print(states_out)
    print(actual_energies)
    print(instance.offset)
    print(len(set(states_out)))


if __name__ == '__main__':
    main()
