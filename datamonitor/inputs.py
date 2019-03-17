import pandas as pd


class AbstractInput:
    def get(self) -> pd.DataFrame:
        return pd.DataFrame()


class DatabaseInput(AbstractInput):
    def __init__(self, file):
        self.file = file

    def get(self) -> pd.DataFrame:
        data = pd.DataFrame()
        # Query database
        return data


class FileInput(AbstractInput):
    def __init__(self, file):
        self.file = file

    def get(self) -> pd.DataFrame:
        data = pd.read_csv(self.file)
        return data


RegisteredInputs = {
    'FileInput': FileInput
}
