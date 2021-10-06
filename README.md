# dictpy (Dictionary Python)

![PyPI](https://img.shields.io/pypi/v/dictpy)
![tests](https://raw.githubusercontent.com/dylanwal/dictpy/master/tests/badges/tests-badge.svg)
![coverage](https://raw.githubusercontent.com/dylanwal/dictpy/master/tests/badges/coverage-badge.svg)
![flake8](https://raw.githubusercontent.com/dylanwal/dictpy/master/tests/badges/flake8-badge.svg)
![downloads](https://img.shields.io/pypi/dm/dictpy)
![license](https://img.shields.io/github/license/dylanwal/dictpy)

Advanced tools for Python dictionaries.

Included Tools:

* `DictSearch`: Search large and complex Python dictionaries/JSON files.
* `Serializer`: Make custom JSON serializable Python classes serializable (make safe for conversion to JSON).

## Installation

Pip installable package available.

`pip install dictpy`


---

---

## Searching (DictSearch)

Imagine you have some big ugly Python dictionary (like the one produced by [PubChem](https://pubchem.ncbi.nlm.nih.gov/)
when you download the JSON file
for [CID 6](https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/6/JSON/?response_type=display)) and you want to
extract some specific piece of information. This section will show how `DictSearch` can make this easy.

To perform the search we can pass the Python dictionary, and a search target (more discussion below on this) to
`DictSearch`. It will find **all** valid objects for the search. The results of the search will be stored in `.result`.

```python
import dictpy

search = dictpy.DictSearch(data=json_data, target=target)
print(search.result)

```

The return object is a `list[list[tree, obj]]`

* `tree`: shows the navigation to get to the data ('.' separated)
    * Keys are recorded for dictionaries
    * Integer are recorded for position in lists
    * Example: `Record.Section.1.Description`
        ```python
        {"Record": {
            "Section": [
                ######,
                {"Description": #####}  # A match to the search!
            ]
        }}
        ```
* `obj` return the object
    * **Options**:
        * Return current object (default)
            * Returns the object you search for
            * Example:
                * search: `{"dog": "*"}`; returns: `{"dog": "golden retriever"}`
                * search: `"dog"`; returns: `{"dog": "golden retriever"}`
                * search: `{"dog": "golden retriever"}`; returns: `{"dog": "golden retriever"}`
        * Return parent object
            * Returns parent object or whole current level
            * To switch to returning parent objects, change `return_func`.
              ```pyhton
              search = dictpy.DictSearch(data=json_data, target=target, return_func=dictpy.DictSearch.return_parent_object)
              ```
            * Example
                * search: `{"dog": "*"}`; returns:
                  ```python
                  {
                  "dog": "golden retriever", 
                  "cat": "bangel", 
                  "fish": "goldfish"
                  }
                  ```
                    * search: `"dog"`; returns:
                  ```python
                  {
                  "dog": "golden retriever", 
                  "cat": "bangel", 
                  "fish": "goldfish"
                  }
                  ```

### How to format `target`

Target can take match accept `strings`, `int`, `floats`, single line `dictionaries`, and `regex` (regular expression).
Wild cards(`*`) can also be used for partial dictionary searches.

Example Targets:
* `{"RecordType": "CID"}`
    * Will match exactly to both 'key', and 'value' (won't match to list entries)
* `{"RecordNumber": 6}`
    * Will match exactly to both 'key', and 'value' (won't match to list entries)
    * With numbers, the default search behavior auto-coverts strings to number. 
        * So this would hit to {"RecordNumber": "6"}
        * To change this behavior set `op_convert_str_to_num=False`
* `2526`
    * Will look for 2526 in either 'key', 'value' or list entry.
* `3D Conformer`
    * Will look for "3D Conformer" in either 'key', 'value' or list entry.
* `{"MoveToTop": "*"}`
    * Will look for "MoveToTop" as a dictionary 'key' and the 'value' can be anything. (won't match to list entries)
* `{"*": "Chemical Safety"}`
    * Will look for "Chemical Safety" as a dictionary 'value' and the 'key' can be anything. (won't match to list entries)
* `"^[A-I]{3}$"`
    * Regular expression search will match in either 'key', 'value' or list entry.
* `{"^RecordT": "*"}`
    * Regular expression search will match for 'key' and 'value' can be anything. (won't match to list entries)
    
For more examples see 
[tests/test_dict_search.py](https://github.com/dylanwal/dictpy/blob/master/tests/test_dict_search.py).



### Example

This example will extract data from a JSON for "1-Chloro-2,4-dinitrobenzene" download from
[PubChem](https://pubchem.ncbi.nlm.nih.gov/).

[Example JSON File](https://github.com/dylanwal/dictpy/blob/master/tests/cid_6.json)

First, we will load our example above (change "/path/to/data/" to your file location for the file above):

```python
import json

with open("C:/path/to/data/cid_6.json", "r") as f:
    text = f.read()
    json_data = json.loads(text)

print(json_data)
```

You will get a massive printout of the 12,000 line JSON file.

```python
import dictpy

search = dictpy.DictSearch(data=json_data, target={"RecordType": "CID"})
print(search.result)
```
Print out:
```python
[['Record.RecordType', {'RecordType': 'CID'}]]
```

Integer search target:
```python
search = dictpy.DictSearch(data=json_data, target=2526)
print(search.result)
```
Print out:
```python
[
    ['Record.Section.3.Section.1.Section.14.Information.1.Value.Number', 2526],
    ['Record.Section.3.Section.1.Section.14.Information.1.Value.Number', 2526]
]
```

---

---

## Serialization (Serializer)

`Serializer` is useful for turning custom python classes into JSON compatible dictionaries.

This serialization class is a useful pre-process step for complex custom python class that contain non-JSON serializable
safe objects (Example: datatime objects, custom classes, any classes from other packages, ObjectIDs, etc.)

Inherit `Serializer` in to your custom python class.

```python
import json
import datetime

import dictpy

class Example(dictpy.Serializer):

    def __init__(self, datetime_obj, stuff2):
        self.datetime_obj = datetime_obj  # NOT JSON serializable object
        self.stuff2 = stuff2
        self.stuff3 = None 


example = Example(datetime.time(), "stuff2")

# json_output = json.dumps(example)  # This will fail with NOT JSON serializable objects

dict_of_example = example.as_dict()
dict_of_example = dictpy.Serializer.dict_cleanup(dict_of_example)  # converts NOT JSON serializable objects to strings. 
dict_of_example = dictpy.Serializer.remove_none(dict_of_example)  # Optional: remove None; self.stuff3 removed

json_output = json.dumps(dict_of_example)
```
