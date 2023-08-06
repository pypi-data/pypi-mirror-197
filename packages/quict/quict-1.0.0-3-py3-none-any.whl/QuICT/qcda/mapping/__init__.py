from .mcts import MCTSMapping
from .sabre import SABREMapping

try:
    from QuICT_ml.rl_mapping.rl_mapping import RlMapping as RLMapping

except:
    RLMapping = None
    print(
        "Please install pytorch, torch-geometric, torch-sparse, tensorboard, cupy and quict_ml first, you can use 'pip install quict-ml' to install quict_ml. "
    )
