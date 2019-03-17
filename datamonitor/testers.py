import glob
import os

import pandas as pd
from .inputs import AbstractInput


class Test:
    def __init__(self):
        self.message = ""
        self.status = None
        pass

    def run(self, Input: AbstractInput):
        """
        get the input and perform the test
        returns true if test passes
        """
        return False

    def set_status(self, ok: bool, message: str):
        if self.status:
            raise Exception("Already executed")
        self.status = ok
        self.message = message

    def __repr__(self):
        return "Status: %s, Message: %s" % (self.status, self.message)


class FreezeFilesystem(Test):
    def __init__(self,
                 path,
                 max_copies=2,
                 compression=None):
        # TODO: verify valid path
        super().__init__()
        self.max_copies = max_copies
        self.path = path
        self.compression = compression
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def run(self, input_data: AbstractInput):
        new_data = input_data.get()
        old_data = self.get_last_copy()
        if not new_data.equals(old_data):
            self.save_copy(new_data)
            self.set_status(False, "Data has changed")
            return
        self.set_status(True, "Data is the same as the last time")

    def get_copy_path(self, number: int) -> str:
        extension = self.compression
        extensions = {
            'gzip': ".csv.gz",
            None: '.csv'
        }
        if self.compression in extensions:
            extension = extensions[self.compression]

        path = os.path.join(self.path, str(number) + extension)
        return path

    def get_copy(self, path: str) -> pd.DataFrame:
        if os.path.isfile(path):
            return pd.read_csv(path, compression=self.compression)
        return pd.DataFrame()

    def get_last_copy(self) -> pd.DataFrame:
        path = self.get_copy_path(self.last_copy_number())
        return self.get_copy(path)

    def last_copy_number(self) -> int:
        for i in range(0, self.max_copies):
            if not os.path.isfile(self.get_copy_path(i)):
                return i - 1
        raise Exception(
            "Copy Limit reached, remove copies or increase the limit."
        )

    def get_next_copy(self) -> str:
        return self.get_copy_path(self.last_copy_number() + 1)

    def save_copy(self, copy: pd.DataFrame):
        path = self.get_copy_path(self.last_copy_number() + 1)
        copy.to_csv(path,
                    compression=self.compression,
                    index=False)

    def reset(self):
        """
        remove all files
        """
        raise NotImplementedError()


RegisteredTests = {
    'FreezeFilesystem': FreezeFilesystem
}
