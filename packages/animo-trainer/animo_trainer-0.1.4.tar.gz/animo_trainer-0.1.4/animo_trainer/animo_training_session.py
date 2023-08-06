import pathlib, os
import numpy as np
from typing import Dict

from mlagents.trainers.cli_utils import parser as ml_agents_parser
from mlagents.trainers.settings import RunOptions, TrainerSettings

from TransformsAI.Animo.Data.Models import AgentData, LevelData
from TransformsAI.Animo.Data.Utility import AgentCheckpointAccumulator, Serializer


INPUT_FOLDER_NAME = "Input"
OUTPUT_FOLDER_NAME = "Output"
AGENTS_FOLDER_NAME = "Agents"
CONFIG_FILE_NAME = "config.yaml"
LEVEL_FILE_NAME = "level.json"
AGENT_DATA_FILE_NAME = "AgentData.json"
AGENT_CHECKPOINT_FILE_NAME =  "checkpoint.pt"

BehaviorName = str

class AnimoTrainingSession:

    def __init__(self, folder_path: str) -> None:
        self.id: str
        self.run_options: RunOptions
        self.level_data: LevelData
        self.agent_datas: Dict[BehaviorName, AgentData] = {}
        self.checkpoint_accumulators: Dict[BehaviorName, AgentCheckpointAccumulator] = {}
        self.agent_output_paths: Dict[BehaviorName, str] = {}

        ## Folders
        training_session_full_folder_path = pathlib.Path(folder_path)
        if not os.path.isdir(training_session_full_folder_path):
            raise ValueError("Training session folder not found")

        input_folder_full_path = os.path.join(training_session_full_folder_path, INPUT_FOLDER_NAME)
        if not os.path.isdir(input_folder_full_path):
            raise ValueError("Input folder not found")

        input_agents_full_path = os.path.join(input_folder_full_path, AGENTS_FOLDER_NAME)
        if not os.path.isdir(input_agents_full_path):
            raise ValueError("Input agents folder not found")

        ## Config
        config_full_path = os.path.join(input_folder_full_path, CONFIG_FILE_NAME)
        if not os.path.isfile(config_full_path):
            raise ValueError("Config.yaml not found")

        args = ml_agents_parser.parse_args([config_full_path])
        self.run_options = RunOptions.from_argparse(args)

        if self.run_options.env_settings.seed == -1:
            self.run_options.env_settings.seed = np.random.randint(0, 10000) #type:ignore

        self.id = training_session_full_folder_path.name
        self.run_options.checkpoint_settings.run_id = self.id
        self.run_options.checkpoint_settings.results_dir = str(os.path.join(training_session_full_folder_path, OUTPUT_FOLDER_NAME, AGENTS_FOLDER_NAME))

        ##TODO: check if path exists and offset the name or smth to allow for seamless hyperparameter tuning

        ## Level
        level_full_path = os.path.join(input_folder_full_path, LEVEL_FILE_NAME)
        if not os.path.isfile(level_full_path):
            raise ValueError("Level.json not found")

        json_level = None
        with open(level_full_path, mode='r') as file:
            json_level = file.read()
        level_data: LevelData = Serializer.FromJson[LevelData](json_level)
        self.level_data = level_data

        #Agents
        for character in level_data.SavedGrid.Characters:
            character_id: str = str(character.CharacterId)

            agent_full_path = os.path.join(input_agents_full_path, character_id)
            if not os.path.isdir(agent_full_path):
                raise ValueError(f"Agent {character_id} folder not found")

            agent_data_full_path = os.path.join(agent_full_path, AGENT_DATA_FILE_NAME)
            if not os.path.isfile(agent_data_full_path):
                raise ValueError(f"Agent {character_id} AgentData.json not found")

            json_agent_data = None
            with open(agent_data_full_path, mode='r') as file:
                json_agent_data = file.read()

            agent_data = Serializer.FromJson[AgentData](json_agent_data)
            self.agent_datas[character_id] = agent_data
            self.checkpoint_accumulators[character_id] = AgentCheckpointAccumulator()

            agent_checkpoint_full_path = os.path.join(agent_full_path, AGENT_CHECKPOINT_FILE_NAME)
            if os.path.isfile(agent_checkpoint_full_path):
                trainer_settings: TrainerSettings = self.run_options.behaviors.get(character_id) #type: ignore
                trainer_settings.init_path = agent_checkpoint_full_path

            self.agent_output_paths[character_id] = os.path.join(training_session_full_folder_path, OUTPUT_FOLDER_NAME, AGENTS_FOLDER_NAME, character_id)
