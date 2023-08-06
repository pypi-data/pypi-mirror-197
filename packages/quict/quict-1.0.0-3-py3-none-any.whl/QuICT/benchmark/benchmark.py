import os
import random
import re
import pandas as pd
import prettytable as pt
import numpy as np
from collections import defaultdict
from matplotlib import pyplot as plt

from QuICT.core.layout.layout import Layout
from QuICT.qcda.qcda import QCDA
from QuICT.simulation.state_vector import StateVectorSimulator
from QuICT.tools.circuit_library.circuitlib import CircuitLib
from QuICT.qcda.synthesis.gate_transform.instruction_set import InstructionSet


class QuICTBenchmark:
    """ The QuICT Benchmarking. """
    def __init__(
        self,
        device: str = "CPU",
        output_path: str = "./benchmark",
        output_file_type: str = "txt"
    ):
        """
        Initial circuit library

        Args:
            output_path (str, optional): The path of the Analysis of the results.
            show_type (str, optional): Analysis of the Graph exists by default,
                and other analysis selects "txt" or "excel".
            simulator (Union, optional): The simulator for simulating quantum circuit.
        """
        self._output_path = os.path.abspath(output_path)
        self._output_file_type = output_file_type
        self._device = device
        self.simulator = StateVectorSimulator(device=self._device)

    def _circuit_selection(self, qubit_num, level):
        based_circuits_list = []
        based_fields_list = ["highly_entangled", "highly_parallelized", "highly_serialized", "mediate_measure"]
        for field in based_fields_list:
            circuits = CircuitLib().get_benchmark_circuit(str(field), qubits_interval=qubit_num)
            based_circuits_list.extend(circuits)
        alg_fields_list = [
            "ctrl_unitary", "diag", "single_bit", "ctrl_diag", "google", "ibmq", "ionq", "ustc", "nam", "origin"
        ]
        random_fields_list = random.sample(alg_fields_list, 5)
        for field in random_fields_list:
            circuits = CircuitLib().get_random_circuit(str(field), qubits_interval=qubit_num)
            based_circuits_list.extend(circuits)

        if level >= 2:
            alg_fields_list = ["adder", "clifford", "qft"]
            for field in alg_fields_list:
                circuits = CircuitLib().get_algorithm_circuit(str(field), qubits_interval=qubit_num)
                based_circuits_list.extend(circuits)

        if level == 3:
            alg_fields_list = ["grover", "cnf", "maxcut", "qnn", "quantum_walk", "vqe"]
            for field in alg_fields_list:
                circuits = CircuitLib().get_algorithm_circuit(str(field), qubits_interval=qubit_num)
                based_circuits_list.extend(circuits)

        return based_circuits_list

    def _validate_quantum_machine_info(self, quantum_machine_info):
        assert isinstance(quantum_machine_info["qubits_number"], int)
        if "layout_file" in quantum_machine_info.keys():
            assert isinstance(quantum_machine_info["layout_file"], Layout)
        if "Instruction_Set" in quantum_machine_info.keys():
            assert isinstance(quantum_machine_info["Instruction_Set"], InstructionSet)

    def get_circuits(
        self,
        quantum_machine_info: dict,
        level: int = 1,
        mapping: bool = False,
        gate_transform: bool = False
    ):
        """
        Get circuit from CircuitLib and Get the circuit after qcda.

        Args:
            quantum_machine_info(dict[str]): Gives the sub-physical machine properties to be measured, include:
                {"qubits_number": str, the number of physical machine bits, "layout_file": layout, the physical machine
                topology, "Instruction_Set": InstructionSet, Physical machine instruction set type,only one double-bit
                gate can be included}.
                for example:

                layout_file = Layout.load_file(f"grid_3x3.json")
                Instruction_Set = InstructionSet(GateType.cx, [GateType.h])

            level (int): Get the type of benchmark circuit group, include different circuits, one of [1, 2, 3],
                default 1.
            mapping(bool): Mapping according to the physical machine topology or not, default False.
            gate_transform(bool): Gate transform according to the physical machine Instruction Set or not,
                default False.

        Returns:
            (List[Circuit]): Return the list of output circuit order by output_type.
        """
        # whether quantum_machine_info is valid or not
        self._validate_quantum_machine_info(quantum_machine_info)

        # Step 1: get circuits from circuitlib
        circuits_list = self._circuit_selection(quantum_machine_info["qubits_number"], level)
        if mapping is False and gate_transform is False:
            return circuits_list

        # Step 2: Whether it goes through QCDA or not
        cir_qcda_list, layout_width_mapping = [], {}
        if mapping:
            for i in range(2, quantum_machine_info["qubits_number"] + 1):
                layout_file = quantum_machine_info["layout_file"].sub_layout(i)
                layout_width_mapping[i] = layout_file

        for circuit in circuits_list:
            cir_width = int(re.findall(r"\d+", circuit.name)[0])
            qcda = QCDA()
            if mapping is True and cir_width > 1:
                qcda.add_mapping(layout_width_mapping[cir_width])

            if gate_transform is True and circuit.name.split("+")[-2] != "mediate_measure":
                qcda.add_gate_transform(quantum_machine_info["Instruction_Set"])
            cir_qcda = qcda.compile(circuit)

            type, classify = circuit.name.split("+")[:-1][0], circuit.name.split("+")[:-1][1]
            if type != "benchmark":
                cir_qcda.name = "+".join(
                    [type, classify, f"w{cir_qcda.width()}_s{cir_qcda.size()}_d{cir_qcda.depth()}"]
                )
            else:
                void_value = int(re.findall(r"\d+", circuit.name)[3])
                cir_qcda.name = "+".join(
                    [type, classify, f"w{cir_qcda.width()}_s{cir_qcda.size()}_d{cir_qcda.depth()}_v{void_value}"]
                )
            cir_qcda_list.append(cir_qcda)

        return cir_qcda_list

    def run(
        self,
        simulator_interface,
        quantum_machine_info: dict,
        level: int = 1,
        mapping: bool = False,
        gate_transform: bool = False
    ):
        """
        Connect real-time benchmarking to the sub-physical machine to be measured.

        Args:
            simulator_interface(optional): Interface for the sub-physical machine to be measured, that is a function for
                realize the output quantum physics machine amplitude of the input circuit, saving circuit and amplitude
                input and output.for example:

                def sim_interface(circuit):
                    simulation(circuit)
                    return amplitude

            quantum_machine_info(dict[str]): Gives the sub-physical machine properties to be measured,for example:
                {"qubits_number": the number of physical machine bits, "layout_file": the physical machine topology,
                "Instruction_Set": Physical machine instruction set type, only one double-bit gate can be included}.
            level (int): Get the type of benchmark circuit group, include different circuits, one of [1, 2, 3],
                default 1.
            mapping(bool): Mapping according to the physical machine topology or not, default False.
            gate_transform(bool): Gate transform according to the physical machine Instruction Set or not,
                default False.

        Returns:
            Return the analysis of benchmarking.
        """
        # Step1 : get circuits from circuitlib
        circuits_list = self.get_circuits(quantum_machine_info, level, mapping, gate_transform)
        # Step 2: physical machine simulation
        amp_results_list = []
        for circuit in circuits_list:
            sim_result = simulator_interface(circuit)
            amp_results_list.append(sim_result)

        # Step 3: evaluate all circuits
        self.evaluate(circuits_list, amp_results_list)

    def evaluate(self, circuits_list: list, amp_results_list: list):
        """
        Evaluate all circuits in circuit list group by fields

        Args:
            circuit_list (List): The list of circuits.
            mac_results_list (List[ndarray]): Physical machine simulation amplitude results.

        Returns:
            Return the analysis of benchmarking.
        """
        # Step 1: Entropy measures the difference between the physical machine
        entropy_QV_score = self._entropy_QV_score(circuits_list, amp_results_list)

        # Step 2: Filter according to certain conditions to obtain valid circuits.
        valid_circuits_list = self._filter_system(entropy_QV_score)
        if valid_circuits_list == []:
            print("There is no valid circuit, please select again !")

        # Step 3: It is a score for the special benchmark circuit index value and the quantum volume of all circuits.
        eigenvalue_QV_score = self._eigenvalue_QV_score(valid_circuits_list)

        # Step 4: Data analysis
        self.show_result(entropy_QV_score, eigenvalue_QV_score, valid_circuits_list)

    def _entropy_QV_score(self, circuit_list, amp_results_list):
        def normalization(data):
            data = np.array(data)
            data = data / np.sum(data)
            return data
        # Step 1: simulate circuit by QuICT simulator
        entropy_QV_score = []
        for index in range(len(circuit_list)):
            if self._device == "CPU":
                sim_result = self.simulator.run(circuit_list[index])
            else:
                sim_result = self.simulator.run(circuit_list[index]).get()

            quict_result = normalization(abs(sim_result))
            machine_result = normalization(abs(amp_results_list[index]))

            # Step 2: calculate Cross entropy loss, Relative entropy loss, Regression loss
            wasserstein = self._wasserstein_cal(quict_result, machine_result)
            huber = self._huber_cal(quict_result, machine_result)
            entropy_value = round((wasserstein + huber) / 2, 4)
            entropy_score = self._entropy_cal(entropy_value)

            circuit_info = re.findall(r"\d+", circuit_list[index].name)
            QV_value = min(int(circuit_info[0]), int(circuit_info[2]))
            # print(entropy_QV_score)
            # Step 3: return entropy values and quantum volumn values
            entropy_QV_score.append([circuit_list[index].name, entropy_value, entropy_score, QV_value])
            entropy_QV_score.sort(key=lambda x: int(re.findall(r"\d+", x[0])[0]), reverse=False)

        return entropy_QV_score

    def _eigenvalue_QV_score(self, valid_circuits_list):
        eigenvalue_QV_score = []
        for i in range(len(valid_circuits_list)):
            field = valid_circuits_list[i].split("+")[-2]
            cir_attribute = re.findall(r"\d+", valid_circuits_list[i])
            QV = min(int(cir_attribute[0]), int(cir_attribute[2]))
            if field == "highly_parallelized":
                P = abs((int(cir_attribute[1]) / int(cir_attribute[2]) - 1) / (int(cir_attribute[0]) - 1) * QV)
                eigenvalue_QV_score.append([valid_circuits_list[i], P])
            elif field == "mediate_measure":
                M = (int(cir_attribute[3]) / int(cir_attribute[2])) * QV
                eigenvalue_QV_score.append([valid_circuits_list[i], M])
            elif field == "highly_entangled":
                E = (1 - int(cir_attribute[3]) / int(cir_attribute[1])) * QV
                eigenvalue_QV_score.append([valid_circuits_list[i], E])
            elif field == "highly_serialized":
                S = (1 - int(cir_attribute[3]) / int(cir_attribute[1])) * QV
                eigenvalue_QV_score.append([valid_circuits_list[i], S])

        return eigenvalue_QV_score

    def _wasserstein_cal(self, p, q):
        # calculate wasserstein distance
        wasserstein_distance = 0
        for i in range(len(p)):
            wasserstein_distance += abs(p[i] - q[i])
        return wasserstein_distance

    def _huber_cal(self, p, q):
        # calculate huber loss
        delta = 1
        huber_loss = 0
        for i_x, i_y in zip(p, q):
            tmp = abs(i_y - i_x)
            if tmp <= delta:
                huber_loss += 0.5 * (tmp ** 2)
            else:
                huber_loss += tmp * delta - 0.5 * delta ** 2
        return huber_loss

    def _entropy_cal(self, entropy_value):
        counts = round((1 - entropy_value) * 100, 2)
        return counts

    def _filter_system(self, entropy_QV_score):
        valid_circuits_list = []
        for i in range(len(entropy_QV_score)):
            if entropy_QV_score[i][2] >= round(2 / 3 * 100, 3):
                valid_circuits_list.append(entropy_QV_score[i][0])
        return valid_circuits_list

    def show_result(self, entropy_QV_score, eigenvalue_QV_score, valid_circuits_list):
        """ show benchmark result. """
        if not os.path.exists(self._output_path):
            os.makedirs(self._output_path)

        if len(eigenvalue_QV_score) > 0:
            self._graph_show(entropy_QV_score, eigenvalue_QV_score, valid_circuits_list)

        if self._output_file_type == "txt":
            self._txt_show(entropy_QV_score)
        else:
            self._excel_show(entropy_QV_score)

    def _graph_show(self, entropy_QV_score, eigenvalue_QV_score, valid_circuits_list):
        plt.rcParams['axes.unicode_minus'] = False
        plt.style.use('ggplot')
        ################################ based circuits benchmark #####################################
        # Construct the data
        feature_name = ['parallelized', 'entangled', 'serialized', 'measure', 'QV']

        P, E, S, M, QV, values, feature = [], [], [], [], [], [], []
        for i in range(len(eigenvalue_QV_score)):
            field = eigenvalue_QV_score[i][0].split("+")[-2]
            if field == "highly_parallelized":
                P.append(eigenvalue_QV_score[i][1])
            elif field == "highly_serialized":
                S.append(eigenvalue_QV_score[i][1])
            elif field == "highly_entangled":
                E.append(eigenvalue_QV_score[i][1])
            elif field == "mediate_measure":
                M.append(eigenvalue_QV_score[i][1])

        for j in range(len(entropy_QV_score)):
            field_random = entropy_QV_score[j][0].split("+")[-3]
            if field_random == "random":
                QV.append(float(entropy_QV_score[j][3]))

        for x in [P, E, S, M, QV]:
            if len(x) > 0:
                values.append(max(x))
                feature.append(feature_name[[P, E, S, M, QV].index(x)])
        N = len(values)

        # Sets the angle of the radar chart to bisect a plane
        angles = np.linspace(0, 2 * np.pi, N, endpoint=False)
        feature = np.concatenate((feature, [feature[0]]))
        values = np.concatenate((values, [values[0]]))
        angles = np.concatenate((angles, [angles[0]]))

        # Draw the first diagram
        plt.figure(figsize=(13, 5), dpi=100)
        plt.figure(1.8)
        ax1 = plt.subplot(121, polar=True)
        ax1.plot(angles, values, 'y-', linewidth=2)
        ax1.fill(angles, values, 'r', alpha=0.5)

        ax1.set_thetagrids(angles * 180 / np.pi, feature)
        ax1.set_ylim(0, np.floor(values.max()) + 0.5)

        plt.tick_params(labelsize=12)
        plt.title('based circuits benchmark radar chart show')
        ax1.grid(True)

        ################################### algorithmic circuits benchmark ##############################
        # Construct the data
        value_list, feature, values_2 = [], [], []
        field_list = ["adder", "clifford", "cnf", "grover", "maxcut", "qft", "qnn", "quantum_walk", "vqe"]
        for i in range(len(valid_circuits_list)):
            field = valid_circuits_list[i].split("+")[-2]
            if field in field_list:
                cir_attribute = re.findall(r"\d+", valid_circuits_list[i])
                QV = min(int(cir_attribute[0]), int(cir_attribute[2]))
                value_list.append([field, QV])
        if len(value_list) > 0:
            field_QV_map = defaultdict(list)
            for field, QV in value_list:
                field_QV_map[field].append(QV)
                feature.append(field)
            feature_1 = list(set(feature))
            feature_1.sort(key=feature.index)
            for value in feature_1:
                values_2.append(max(field_QV_map[value]))
            # Sets the angle of the radar chart to bisect a plane
            N = len(values_2)
            angles = np.linspace(0, 2 * np.pi, N, endpoint=False)
            feature_1 = np.concatenate((feature_1, [feature_1[0]]))
            values_2 = np.concatenate((values_2, [values_2[0]]))
            angles = np.concatenate((angles, [angles[0]]))
            # Draw the second diagram
            ax2 = plt.subplot(122, polar=True)
            ax2.plot(angles, values_2, 'c-', linewidth=2)
            ax2.fill(angles, values_2, 'b', alpha=0.5)
            ax2.set_thetagrids(angles * 180 / np.pi, feature_1)
            ax2.set_ylim(0, np.floor(values_2.max()) + 0.5)

            plt.tick_params(labelsize=12)
            plt.title('algorithmic circuits benchmark radar chart show')
            ax2.grid(True)

        plt.savefig(self._output_path + "/benchmark_radar_chart_show.jpg")
        plt.show()

    def _txt_show(self, entropy_QV_score):
        result_file = open(self._output_path + '/benchmark_txt_show.txt', mode='w+', encoding='utf-8')
        tb = pt.PrettyTable()
        tb.field_names = [
            'field', 'circuit width', 'circuit size', 'circuit depth', 'entropy value', 'entropy score', 'QV value'
        ]
        for i in range(len(entropy_QV_score)):
            field = entropy_QV_score[i][0].split("+")[-2]
            cir_attribute = re.findall(r"\d+", entropy_QV_score[i][0])
            tb.add_row([
                field, cir_attribute[0], cir_attribute[1], cir_attribute[2], entropy_QV_score[i][1],
                entropy_QV_score[i][2], (2 ** entropy_QV_score[i][3])
            ])
        result_file.write(str(tb))
        result_file.close()

    def _excel_show(self, entropy_QV_score):
        dfData_list = []
        for i in range(len(entropy_QV_score)):
            field = entropy_QV_score[i][0].split("+")[-2]
            cir_attribute = re.findall(r"\d+", entropy_QV_score[i][0])
            dfData = {
                'field': field,
                'circuit width': cir_attribute[0],
                'circuit size': cir_attribute[1],
                'circuit depth': cir_attribute[2],
                'entropy value': entropy_QV_score[i][1],
                'entropy score': entropy_QV_score[i][2],
                'QV value': 2 ** entropy_QV_score[i][3]
            }
            dfData_list.append(dfData)

        df = pd.DataFrame(dfData_list)
        df.to_excel(self._output_path + "/benchmark_excel_show.xlsx")
