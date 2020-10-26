from .exception import ProjectUninitializedException, ExperimentUninitializedExcpetion
from .project import Project
from .experiment import Experiment

import pandas as pd

project = None


def init(output_path: str) -> None:
    global project
    project = Project(output_path=output_path)


def get_project() -> Project:
    # pylint: disable=global-statement
    global project
    if project is None:
        raise ProjectUninitializedException()
    return project


def get_experiment() -> Experiment:
    return get_project().get_current_experiment()


def create_experiment(name=None) -> Experiment:
    return get_project().create_experiment(name=name)


def log_params(name: str, params: dict) -> str:
    return get_experiment().log_params(name, params)


def log_dataset(name: str, dataset) -> str:
    return get_experiment().log_dataset(name, dataset)


def log_image(name: str, fig=None) -> str:
    return get_experiment().log_image(name, fig)


def log_artifact(name: str, artifact) -> str:
    return get_experiment().log_artifact(name, artifact)


def log_dataframe(name: str, df: pd.DataFrame) -> str:
    return get_experiment().log_dataframe(name, df)


def reset():
    global project
    if project is not None:
        project.close()
    project = None
