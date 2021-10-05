# dictpy (Dictionary Python)

![PyPI](https://img.shields.io/pypi/v/dictpy)
![tests](https://raw.githubusercontent.com/dylanwal/dictpy/master/tests/badges/tests-badge.svg)
![coverage](https://raw.githubusercontent.com/dylanwal/dictpy/master/tests/badges/coverage-badge.svg)
![flake8](https://raw.githubusercontent.com/dylanwal/dictpy/master/tests/badges/flake8-badge.svg)
![downloads](https://img.shields.io/pypi/dm/dictpy)
![license](https://img.shields.io/github/license/dylanwal/dictpy)



This Python Package can help with finding data in large complex Python dictionaries. These data structures of typical of
JSON Files.

Additionally, a serialization tool is included to turning custom python classes into JSON compatible dictionaries.
 

## Installation

Pip installable package available. 

`pip install dictpy`


---

---

## Search Usage

Load in a JSON file.

```python
import json

with open(data_path, "r") as f:
    text = f.read()
    json_data = json.loads(text)
```

Preform search. It will find all valid objects in the search. Use `.result` to view results.

```python
import dictpy

search = DictSearch(data=json_data, target=target)
print(search.result)
    
```

Example return object:
The return object is a `list[list[tree, obj]]`.

`tree` shows the navigation to get to the data ('.' separated)

`obj` shows the object found

```python
[['Record.Section.TOCHeading', {'TOCHeading': 'Chemical Safety'}],
 ['Record.Section.Information.Name', {'Name': 'Chemical Safety'}]]
```

### How to format target

You can exact match on `strings`, `int`, `floats` and single line `dictionaries`. Examples:

```python
{"RecordType": "CID"}
{"RecordNumber": 6}
{"TOCHeading": "Structures"}
2526
"3D Conformer"
```

You also can do partial dictionary searches with "*" as a wild card.

```python
{"MoveToTop": "*"}
{"*": "Chemical Safety"}
```

### Options of what is returned

Currently, there are two return options. The exact object (default) or parent object.
To change to parent object, change return function:
```python
search = DictSearch(data=json_data, target=target, return_func=DictSearch.return_parent_object)    
```

---

---

## Serialization

This serialization class is a useful pre-process step for complex custom python class that contain non-JSON serializable
safe objects (Example: datatime objects, custom classes, any classes from other packages, ObjectIDs, etc.)

Inherit `Serializer` in to your custom python class.

```python
from dictpy import Serializer
import json

class Example(Serializer):

    def __init__(self, stuff, stuff2, stuff3):
        self.stuff = stuff # NOT JSON serializable object
        self.stuff2 = stuff2
        self.stuff3 = stuff3

example = Example(stuff, stuff2, stuff3)

# json_output = json.dumps(example)  # This will fail with NOT JSON serializable objects

dict_of_example = example.as_dict()
dict_of_example = Serializer.dict_cleanup(dict_of_example)  # converts NOT JSON serializable objects to strings. 
dict_of_example = Serializer.remove_none(dict_of_example)  # Optional: remove None 

json_output = json.dumps(dict_of_example)
```
