import os
import joblib
import yaml
import pytest
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

import expmgr


@pytest.fixture(autouse=True)
def cleanup():
    yield
    expmgr.reset()


@pytest.fixture
def project(tmp_path):
    path = os.path.join(tmp_path.resolve().as_posix(), "test")
    expmgr.init(path)
    return expmgr.get_project()


@pytest.fixture
def experiment(project):
    return project.create_experiment("test")


@pytest.fixture
def dataframe():
    return pd.DataFrame({"numbers": [1, 2, 3], "colors": ["red", "white", "blue"]})


@pytest.fixture
def image():
    b = np.arange(1, 20)
    f = plt.figure()
    plt.plot(b, np.sin(b))
    return f


@pytest.fixture
def params():
    return {"param1": 1, "b": "abc", "obj": {"subparam11": 22}}


def test_uninitialized_project():
    with pytest.raises(expmgr.exception.ProjectUninitializedException):
        expmgr.get_project()


def test_init(tmp_path):
    path = os.path.join(tmp_path.resolve().as_posix(), "test")

    assert not os.path.exists(path)
    expmgr.init(path)
    assert os.path.exists(path)


def test_uninitialized_experiment(tmp_path):

    path = os.path.join(tmp_path.resolve().as_posix(), "test")

    with pytest.raises(expmgr.exception.ProjectUninitializedException):
        expmgr.get_experiment()

    expmgr.init(path)

    with pytest.raises(expmgr.exception.ExperimentUninitializedExcpetion):
        expmgr.get_experiment()


def test_create_experiment(project):

    exp_name = "test"

    exp = expmgr.create_experiment(exp_name)
    assert type(exp) == expmgr.experiment.Experiment
    assert exp.output_path.startswith(project.output_path)
    assert len(exp.output_path) > len(project.output_path)
    assert exp.output_path.endswith(exp_name)


def test_log_params(experiment, params):

    fname = expmgr.log_params("test", params)
    with open(fname, "r") as f:
        params_loaded = yaml.load(f, yaml.FullLoader)

    assert params == params_loaded


def test_log_image(experiment, image):
    fname = expmgr.log_image("test", image)

    with open(fname, "rb") as f:
        bytes = f.read(8)

    magic_bytes_png = b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A"
    assert bytes == magic_bytes_png


def test_log_dataframe(experiment, dataframe):
    fname = expmgr.log_dataframe("test", dataframe)

    df_loaded = pd.read_excel(fname, index_col=0)
    pd.testing.assert_frame_equal(dataframe, df_loaded)


def test_log_dataset(experiment, dataframe):
    fname = expmgr.log_dataset("test", dataframe)

    df_loaded = joblib.load(fname)
    pd.testing.assert_frame_equal(dataframe, df_loaded)


def test_log_artifact(experiment, dataframe):
    fname = expmgr.log_artifact("test", dataframe)

    df_loaded = joblib.load(fname)
    pd.testing.assert_frame_equal(dataframe, df_loaded)
