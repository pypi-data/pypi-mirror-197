from .statevector_simulator import StateVectorSimulator

try:
    from QuICT_sim.cpu_simulator import CircuitSimulator as HPStateVecotrSimulator
except:
    HPStateVecotrSimulator = None
    print("Please install quict_sim first, you can use 'pip install quict_sim' to install. ")
