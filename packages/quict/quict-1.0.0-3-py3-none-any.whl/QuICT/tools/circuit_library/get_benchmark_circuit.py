import random
import numpy as np

from QuICT.core import Circuit
from QuICT.core.gate import *


class BenchmarkCircuitBuilder:
    """
    A class fetch QuICT benchmark circuits.

    Args:
        width(int): number of qubits
        size(int): number of gates
        random_params (bool, optional): whether random parameter or use default parameter. Defaults to True.
    """
    @staticmethod
    def parallelized_circuit_build(width: int, size: int):
        typelist = [GateType.rz, GateType.cx]
        prob = [0.8, 0.2]

        gate_indexes = list(range(2))
        qubits_indexes = list(range(width))
        shuffle_qindexes = qubits_indexes[:]
        random.shuffle(shuffle_qindexes)

        random_para = [0.4, 0.6, 0.8, 1]
        cirs_list = []

        for i in range(len(random_para)):
            cir = Circuit(width)
            H | cir(0)
            while cir.size() < size:
                rand_type = np.random.choice(gate_indexes, p=prob)
                gate_type = typelist[rand_type]
                gate = GATE_TYPE_TO_CLASS[gate_type]()

                if gate.params:
                    gate.pargs = list(np.random.uniform(0, 2 * np.pi, gate.params))

                gsize = gate.controls + gate.targets
                if gsize > len(shuffle_qindexes):
                    continue

                gate & shuffle_qindexes[:gsize] | cir
                if gsize == len(shuffle_qindexes) or random.random() > random_para[i]:
                    shuffle_qindexes = qubits_indexes[:]
                    random.shuffle(shuffle_qindexes)
                else:
                    shuffle_qindexes = shuffle_qindexes[gsize:]

            depth = cir.depth()
            cir.name = "+".join(["benchmark", "highly_parallelized", f"w{width}_s{size}_d{depth}_v1"])
            cirs_list.append(cir)
        return cirs_list

    @staticmethod
    def serialized_circuit_build(width: int, size: int):
        cirs_list = []
        random_para = [0.4, 0.6, 0.8, 1]

        for i in range(len(random_para)):
            void_gates = 0
            cir = Circuit(width)
            H | cir(0)
            qubit_indexes = list(range(width))
            qubit = random.choice(qubit_indexes)
            qubit_indexes.remove(qubit)
            while cir.size() < size:
                qubit_new = random.choice(qubit_indexes)
                qubits_list = [qubit, qubit_new]
                random.shuffle(qubits_list)
                CX & (qubits_list) | cir
                if random.random() > random_para[i]:
                    CX & (random.sample(list(range(width)), 2)) | cir
                    void_gates += 1

            depth = cir.depth()
            cir.name = "+".join(["benchmark", "highly_serialized", f"w{width}_s{size}_d{depth}_v{void_gates}"])
            cirs_list.append(cir)

        return cirs_list

    @staticmethod
    def entangled_circuit_build(width: int, size: int):
        def _pattern1():
            cgate = CompositeGate()
            qubit_indexes = list(range(width))
            qubit_extra = []
            for _ in range(width):
                if len(qubit_indexes) > 1:
                    qubit_index = random.sample(qubit_indexes, 2)
                    CX & (qubit_index) | cgate
                    qubit_extra.append(qubit_index)
                    qubit_indexes = list(set(qubit_indexes) - set(qubit_index))
                elif len(qubit_indexes) == 1:
                    for i in range(len(qubit_extra)):
                        q_collect = random.choice(qubit_extra[i])
                        CX & ([qubit_indexes[0], q_collect]) | cgate
                    break
                else:
                    break
            return cgate

        def _pattern2():
            cgate = CompositeGate()
            qubit_indexes = list(range(width))
            result = [qubit_indexes[i:i + 2] for i in range(0, len(qubit_indexes), 2)]
            for i in range(len(result)):
                if len(result[i]) == 2:
                    CX & (result[i]) | cgate

            result = [qubit_indexes[i + 1:i + 3] for i in range(0, len(qubit_indexes), 2)]
            for i in range(len(result)):
                if len(result[i]) == 2:
                    CX & (result[i]) | cgate
                else:
                    break

            return cgate

        random_para = [0.4, 0.6, 0.8, 1]
        cirs_list = []
        for i in range(len(random_para)):
            void_gates = 0
            cir = Circuit(width)
            H | cir(0)
            while cir.size() < size:
                if size - cir.size() < width or random.random() > random_para[i]:
                    cir.random_append(1, [GateType.cx])
                    void_gates += 1
                else:
                    cgate = random.choice([_pattern1(), _pattern2()])
                    cgate | cir

            size = cir.size()
            depth = cir.depth()
            cir.name = "+".join(["benchmark", "highly_entangled", f"w{width}_s{size}_d{depth}_v{void_gates}"])
            cirs_list.append(cir)

        return cirs_list

    @staticmethod
    def mediate_measure_circuit_build(width: int, size: int):
        typelist = [GateType.rz, GateType.cx]
        prob = [0.8, 0.2]

        def flat_build():
            cgate = CompositeGate()
            qubits_indexes = list(range(width))
            random.shuffle(qubits_indexes)
            while len(qubits_indexes) > 0:
                if len(qubits_indexes) == 1:
                    Rz & qubits_indexes.pop() | cgate
                else:
                    gate_type = np.random.choice(typelist, p=prob)
                    gate = GATE_TYPE_TO_CLASS[gate_type]()
                    gate_size = gate.controls + gate.targets
                    gate & qubits_indexes[:gate_size] | cgate
                    qubits_indexes = qubits_indexes[gate_size:]

            return cgate

        cir_list = []
        random_para = [0.4, 0.6, 0.8, 1]
        for i in range(len(random_para)):
            void_gates = 0
            cir = Circuit(width)
            for _ in range(size - width, size, width):
                flat_build() | cir
            Measure | cir
            while cir.size() < size:
                if size - cir.size() < width or random.random() > random_para[i]:
                    cir.random_append(1, [random.choice(typelist)])
                    void_gates += 1
                else:
                    flat_build() | cir
            size = cir.size()
            depth = cir.depth()
            cir.name = "+".join(["benchmark", "mediate_measure", f"w{width}_s{size}_d{depth}_v{void_gates}"])
            cir_list.append(cir)

        return cir_list
