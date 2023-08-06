from typing import Union
from torch.utils.data import IterableDataset
from kaptik.api import DataServerClient

SERVER_FETCH_BATCH_SIZE = 64


class KaptikDataset(IterableDataset):

    def __init__(self, ds_name: str):
        self.client = DataServerClient()
        self.ds_name = ds_name

    def get_metadata(self):
        return self.client.get_dataset_metadata(self.ds_name)

    def get_ds_info(self):
        return self.client.get_dataset_info(self.ds_name)

    def __iter__(self):
        batch_reader = self.client.get_batches(
            self.ds_name, SERVER_FETCH_BATCH_SIZE
        )
        for batch in batch_reader:
            for item in batch.iterrows():
                yield item

    def head(self, n_records: int = 100):
        table = self.client.do_action(
            "get_head", ds_name=self.ds_name, n_records=n_records
        )
        return table.to_pandas()

    def __getitem__(self, val: Union[int, list, slice]):
        if isinstance(val, int):
            table = self.client.do_action(
                "get_records", ds_name=self.ds_name, record_idxs=[val]
            )
        elif isinstance(val, list):
            table = self.client.do_action(
                "get_records", ds_name=self.ds_name, record_idxs=val
            )
        elif isinstance(val, slice):
            assert val.step is None or val.step == 1, "Index step != 1 is currently not supported"
            table = self.client.do_action(
                "get_slice",
                ds_name=self.ds_name,
                start=val.start,
                stop=val.stop
            )
        return table.to_pandas()
