import os, argparse

from mlagents.plugins.trainer_type import register_trainer_plugins

##### The order of following imports is important
from pythonnet import load
load("coreclr")

import clr, pathlib

CURRENT_DIR = pathlib.Path(__file__).parent.resolve()
print(f"CurDir: {CURRENT_DIR}")
ANIMO_UNITY_DLL_DIR = os.path.realpath(os.path.join(CURRENT_DIR, "lib"))

# Load Animo DLLs
for f in os.listdir(ANIMO_UNITY_DLL_DIR):
    dll_path = os.path.join(ANIMO_UNITY_DLL_DIR, f)
    if os.path.isfile(dll_path) and dll_path.endswith(".dll"):
        clr.AddReference(dll_path)

from animo_trainer.animo_training_session import AnimoTrainingSession
from animo_trainer.animo_trainer_controller import AnimoTrainerController
from animo_trainer.animo_stats_writers import register_animo_stats_writers

ASCII_LOGO = f"""
---------------------
Transitional Forms Inc.
---------------------
"""

parser = argparse.ArgumentParser()
parser.add_argument(
    "training_session_full_path", nargs="?", default=None
)


def main():
    print(ASCII_LOGO)

    register_trainer_plugins()
    
    training_session_folder_path = parser.parse_args().training_session_full_path
    if training_session_folder_path is None:
        raise ValueError("Training session full path must be provided")
    
    training_session_data = AnimoTrainingSession(training_session_folder_path)

    register_animo_stats_writers(training_session_data.run_options)
    
    animo_trainer_controller = AnimoTrainerController(training_session_data)
    print(f"Animo-Learn::Started")
    animo_trainer_controller.train()


if __name__ == "__main__":
    main()