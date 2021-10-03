# dictpy (Dictionary Python)

This Python Package can help with finding data in large complex Python dictionaries. These data structures of typical of
JSON Files.

## Installation

`pip install dictpy`

## Usage

Load in a JSON file.

```python
    import json

    with open(data_path, "r") as f:
        text = f.read()
        json_data = json.loads(text)
```

Preform search. It will find all valid objects in the search.

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

### Options on return

Currently, there are two return options. The exact object (default) or parent object.
To change to parent object, change return fucntion:
```python
    search = DictSearch(data=json_data, target=target, return_func=DictSearch.return_parent_object)    
```

