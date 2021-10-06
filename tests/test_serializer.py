import pytest
import datetime
import json

from dictpy import Serializer
from dictpy import DictSearch


def test_initialization():
    class Example(Serializer):
        pass
    a = Example()

    assert isinstance(a, Serializer)


@pytest.fixture(scope="session")
def example_class():
    class Example(Serializer):
        def __init__(self):
            self.number = 12
            self.llist = [123, 213, 123]
            self.llist2 = []
            self.obj = datetime.time()
            self.ddict = {"fish": "goldfish", "mammal": 10, "time": datetime.time()}
            self.list_dict = [{"fish": 2}, {"pig": "lots"}, {"cows": None}]
            self.nnone = None

    return Example()


def test_serialization(example_class):
    assert isinstance(example_class.as_dict(), dict)


def test_none(example_class):
    ddict = example_class.as_dict()
    result = DictSearch(ddict, None).result
    assert result == [["nnone", {"nnone": None}], ["list_dict.2.cows", {"cows": None}]]


def test_remove_none(example_class):
    ddict = Serializer.remove_none(example_class.as_dict())
    result = DictSearch(ddict, None).result
    assert result == []


def test_cleanup_negative(example_class):
    ddict = Serializer.remove_none(example_class.as_dict())
    with pytest.raises(TypeError):
        a = json.dumps(ddict)


def test_cleanup_positive(example_class):
    ddict = Serializer.remove_none(example_class.as_dict())
    clean_dict = json.dumps(Serializer.dict_cleanup(ddict))
    assert isinstance(clean_dict, str)


@pytest.fixture(scope="session")
def example_class2():
    class SubExample(Serializer):
        def __init__(self):
            self.number = 12
            self.llist = [123, 213, 123]
            self.obj = datetime.time()
            self.ddict = {"fish": "goldfish", "mammal": 10, "time": datetime.time()}

    class Example(Serializer):
        def __init__(self, subclass):
            self.subclass = subclass
            self.number = 12
            self.llist = [123, 213, 123]
            self.obj = datetime.time()
            self.ddict = {"fish": "goldfish", "mammal": 10, "time": datetime.time()}

    return Example(SubExample())


def test_serialization2(example_class2):
    assert isinstance(example_class2.as_dict(), dict)

