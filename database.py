import random

from docarray import BaseDoc
from docarray.typing import NdArray
from docarray import DocList
from vectordb import InMemoryExactNNVectorDB
import joblib


class FlowDoc(BaseDoc):
    text: str = ''
    embedding: NdArray[4096]


class VectorDB:
    def __init__(self):
        self.db = InMemoryExactNNVectorDB[FlowDoc](workspace='./workspace_path')

    def fill_db(self, path_to_dict="./data/vec_dict.joblib"):
        vec_dict = joblib.load(path_to_dict)
        doc_list = [FlowDoc(text=path[0], embedding=vec[0]) for path, vec in vec_dict.items()]
        self.db.index(inputs=DocList[FlowDoc](doc_list))

    def find_sims(self, query, limit=6):
        results = self.db.search(inputs=DocList[FlowDoc]([query]), limit=limit)
        return results
