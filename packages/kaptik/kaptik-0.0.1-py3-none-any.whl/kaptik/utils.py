import threading
import pyarrow as pa
import msgpack

TABLE_TYPE_KEY = "__kaptik_pyarrow_table__"

class SingletonMetaclass(type):
    _instances = {}
    _singleton_lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        # double-checked locking pattern (https://en.wikipedia.org/wiki/Double-checked_locking)
        if cls not in cls._instances:
            with cls._singleton_lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super(SingletonMetaclass,
                                                cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def serialize(obj: object):
    if isinstance(obj, pa.Table):
        obj = {TABLE_TYPE_KEY: obj.to_pydict()}
    return msgpack.packb(obj)


def deserialize(bin: bytes):
    obj = msgpack.unpackb(bin)
    if isinstance(obj, dict):
        if len(obj) == 1 and TABLE_TYPE_KEY in obj:
            obj = pa.Table.from_pydict(obj[TABLE_TYPE_KEY])
    return obj
