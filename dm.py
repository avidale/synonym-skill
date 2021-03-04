from dialogic.cascade import Cascade
from dialogic.dialog_manager import TurnDialogManager

csc = Cascade()


def make_dm() -> TurnDialogManager:
    dm = TurnDialogManager(
        cascade=csc,
        intents_file='data/intents.yaml'
    )
    return dm
