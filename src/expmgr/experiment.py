import os
import datetime
import yaml
import joblib
import matplotlib.pyplot as plt
import pandas as pd


class Experiment:
    def __init__(self, output_path, name=None):
        self.output_path = output_path
        dtstr = datetime.datetime.now().strftime("%y%m%dT%H%M%S")
        self.name = dtstr
        if name is not None:
            self.name += f"_{name}"
        self.output_path = os.path.join(output_path, self.name)

        if not os.path.exists(self.output_path):
            os.mkdir(self.output_path)

    def _write_to_file(self, fname: str, content):
        with open(fname, "w") as f:
            f.write(content)

    def _get_filename(self, fname, suffix):
        return os.path.join(self.output_path, f"{fname}.{suffix}")

    def log_params(self, name: str, params: dict) -> str:
        s = yaml.dump(params)
        fname = self._get_filename(name, "yaml")
        self._write_to_file(fname, s)

        return fname

    def log_dataset(self, name: str, dataset) -> str:
        fname = self._get_filename(name, "dump.gz")
        joblib.dump(dataset, fname)

        return fname

    def log_dataframe(self, name: str, df: pd.DataFrame) -> str:
        fname = self._get_filename(name, "xlsx")
        df.to_excel(fname)

        return fname

    def log_image(self, name: str, fig=None) -> str:
        fname = self._get_filename(name, "png")
        if fig is None:
            fig = plt.gcf()
        fig.savefig(fname)

        return fname

    def log_artifact(self, name: str, artifact) -> str:
        fname = self._get_filename(name, "dump.gz")
        joblib.dump(artifact, fname)

        return fname
