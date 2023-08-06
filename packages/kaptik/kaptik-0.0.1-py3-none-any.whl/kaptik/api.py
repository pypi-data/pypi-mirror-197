import pandas as pd
from typing import List, Callable, Union, Any
import pyarrow as pa
from pyarrow import flight
from kaptik.utils import SingletonMetaclass
from kaptik.utils import serialize, deserialize
from kaptik import DATA_SERVER_HOST, DATA_SERVER_PORT


class DataServerClient(metaclass=SingletonMetaclass):

    def __init__(
        self, host: str = None, port: int = None, certificate=None, **kwargs
    ):
        host = host or DATA_SERVER_HOST
        port = port or DATA_SERVER_PORT
        scheme = "grpc" if certificate is None else "grpc+tls"
        location = "{}://{}:{}".format(scheme, host, port)

        self.client = flight.FlightClient(location, **kwargs)
        self._dataset: flight.FlightInfo = None
        print(f"Connected to {location}")

    def get_dataset_info(self, dataset: str):
        descriptor = flight.FlightDescriptor.for_path(dataset)
        flight_info = self.client.get_flight_info(descriptor)
        return flight_info

    def get_dataset_metadata(self, dataset: str):
        flight_info = self.get_dataset_info(dataset)
        metadata = flight_info.schema.metadata
        return metadata

    def list_datasets(self):
        for flight in self.client.list_flights():
            flight: flight.FlightInfo

            descriptor = flight.descriptor
            endpoints = flight.endpoints
            print(
                "Path:", descriptor.path[0].decode('utf-8'), "Rows:",
                flight.total_records, "Size:", flight.total_bytes
            )
            print([e.ticket for e in endpoints])
            print("=== Schema ===")
            print(flight.schema)
            print("==============")

    def get_batches(
        self,
        dataset: str,
        batch_size: int,
        batch_preprocess_fn: Callable = None
    ) -> Union[pd.DataFrame, Any]:
        # Read content of the dataset
        dataset_info = self.get_dataset_info(dataset)
        endpoints = dataset_info.endpoints

        # TODO: can parallelize this across endpoints
        for endpoint in endpoints:
            # NOTE: Don't use deserialize here
            # FlightDescriptor.for_path() automatically serializes with path.encode("utf-8")
            request = {
                "ds_name": endpoint.ticket.ticket.decode('utf-8'),
                "batch_size": batch_size
            }
            ticket = flight.Ticket(serialize(request))
            reader = self.client.do_get(ticket)
            for chunk in reader:
                data: pd.DataFrame = chunk.data.to_pandas()
                if batch_preprocess_fn:
                    data = batch_preprocess_fn(data)
                yield data

    def do_action(self, action_name, **kwargs):
        kwargs = serialize(kwargs)
        action = flight.Action(action_name, kwargs)
        return [
            deserialize(result.body.to_pybytes())
            for result in self.client.do_action(action)
        ][0]

    def get_indexes(self, dataset: str, record_idxs: List[int]):
        return self.do_action(
            "get_record", ds_name=dataset, record_idxs=record_idxs
        )

    def shutdown(self):
        return self.do_action("server_shutdown")
