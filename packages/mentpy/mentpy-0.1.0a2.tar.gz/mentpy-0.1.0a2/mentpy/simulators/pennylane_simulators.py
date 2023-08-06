from typing import Union, List, Tuple, Optional

import numpy as np

from mentpy.simulators.base_simulator import BaseSimulator
from mentpy.states.mbqcstate import MBQCState

import pennylane as qml
import networkx as nx

__all__ = ["PennylaneSimulator"]


class PennylaneSimulator(BaseSimulator):
    """Simulator for measuring patterns of MBQC states.

    Args
    ----
    mbqcstate: mp.MBQCState
        The MBQC state used for the simulation.
    input_state: np.ndarray
        The input state of the simulator.

    See Also
    --------
    :class:`mp.PatternSimulator`, :class:`mp.CirqSimulator`

    Group
    -----
    simulators
    """

    def __init__(
        self, mbqcstate: MBQCState, input_state: np.ndarray, *args, **kwargs
    ) -> None:
        self.circuit = graphstate_to_circuit(mbqcstate)
        super().__init__(mbqcstate, input_state)

    def measure(self, angle: float, plane: str = "XY"):
        raise NotImplementedError

    def measure_pattern(
        self, angles: List[float], planes: Union[List[str], str] = "XY", **kwargs
    ) -> Tuple[List[int], np.ndarray]:

        # TODO: Implement this
        if planes != "XY":
            raise NotImplementedError

        return self.circuit(angles, st=self.input_state, **kwargs)

    def reset(self, input_state=None):
        if input_state is None:
            input_state = self.input_state
        self.input_state = input_state


def graphstate_to_circuit(gsc):
    """Converts a MBQCState to a PennyLane circuit."""
    gr = gsc.graph
    N = gr.number_of_nodes()
    dev = qml.device("default.qubit", wires=N)

    @qml.qnode(dev)
    def circuit(param, output="density", st=None):
        if output != "density":
            assert (
                len(param) == N
            ), f"Length of param is {len(param)}, but expected {N}."
        else:
            assert (
                len(param) == N - 2
            ), f"Length of param is {len(param)}, but expected {N-2}."
        input_v = st
        qml.QubitStateVector(input_v, wires=gsc.input_nodes)
        for j in gsc.inputc:
            qml.Hadamard(j)
        for i, j in gr.edges():
            qml.CZ(wires=[i, j])

        topord_no_output = [
            x for x in gsc.measurement_order if (x not in gsc.output_nodes)
        ]
        for indx, p in zip(topord_no_output, param[: len(gsc.outputc)]):
            qml.RZ(p, wires=indx)
            qml.Hadamard(wires=indx)
            m_0 = qml.measure(indx)
            qml.cond(m_0, qml.PauliX)(wires=gsc.flow(indx))
            for neigh in gr.neighbors(gsc.flow(indx)):
                if neigh != indx and (
                    gsc.measurement_order.index(neigh)
                    > gsc.measurement_order.index(indx)
                ):
                    qml.cond(m_0, qml.PauliZ)(wires=neigh)

        if output == "expval":
            for indx, p in zip(gsc.output_nodes, param[len(gsc.outputc) :]):
                qml.RZ(p, wires=indx)
            return [qml.expval(qml.PauliX(j)) for j in gsc.output_nodes]
        elif output == "sample":
            for indx, p in zip(gsc.output_nodes, param[len(gsc.outputc) :]):
                qml.RZ(p, wires=indx)
            return [qml.sample(qml.PauliX(j)) for j in gsc.output_nodes]
        elif output == "density":
            return qml.density_matrix(gsc.output_nodes)

    return circuit
