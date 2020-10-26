from .experiment import Experiment
from .exception import ExperimentUninitializedExcpetion
import os


class Project:
    def __init__(self, output_path):
        self.output_path = output_path
        self.current_experiment = None

        if not os.path.exists(self.output_path):
            os.mkdir(self.output_path)

    def create_experiment(self, name=None) -> Experiment:
        self.current_experiment = Experiment(self.output_path, name)
        return self.get_current_experiment()

    def get_current_experiment(self) -> Experiment:
        if self.current_experiment is None:
            raise ExperimentUninitializedExcpetion()
        return self.current_experiment

    def close(self):
        pass
