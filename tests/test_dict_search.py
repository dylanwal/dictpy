from pathlib import Path
import json
import pytest

from dictpy import DictSearch

parent_path = Path(__file__).parent


@pytest.fixture(scope="session")
def example_json():
    data_path = (parent_path / Path(r"cid_6.json")).resolve()
    with open(data_path, "r") as f:
        text = f.read()
        json_data = json.loads(text)
    return json_data


def test_result(example_json):
    search = DictSearch(data=example_json, target={"RecordType": "CID"}, return_func=None)
    assert search.result == [["Record.RecordType", {"RecordType": "CID"}]]


targets = [
    [{"RecordType": "CID"}, [['Record.RecordType', {'RecordType': 'CID'}]]],

    [{"RecordNumber": 6}, [['Record.RecordNumber', {'RecordNumber': 6}]]],

    [{"TOCHeading": "Structures"}, [['Record.Section.TOCHeading', {'TOCHeading': 'Structures'}]]],

    [{"TOCHeading": "3D Conformer"}, [['Record.Section.Section.TOCHeading', {'TOCHeading': '3D Conformer'}]]],

    [{"MoveToTop": "*"}, [['Record.Section.DisplayControls.MoveToTop', {'MoveToTop': True}],
                          ['Record.Section.Section.DisplayControls.MoveToTop', {'MoveToTop': True}],
                          ['Record.Section.Section.DisplayControls.MoveToTop', {'MoveToTop': True}],
                          ['Record.Section.Section.DisplayControls.MoveToTop', {'MoveToTop': True}],
                          ['Record.Section.Section.DisplayControls.MoveToTop', {'MoveToTop': True}],
                          ['Record.Section.Section.DisplayControls.MoveToTop', {'MoveToTop': True}],
                          ['Record.Section.Section.DisplayControls.MoveToTop', {'MoveToTop': True}],
                          ['Record.Section.Section.Section.DisplayControls.MoveToTop', {'MoveToTop': True}],
                          ['Record.Section.Section.Section.DisplayControls.MoveToTop', {'MoveToTop': True}]]
     ],
    [{"*": "Chemical Safety"}, [['Record.Section.TOCHeading', {'TOCHeading': 'Chemical Safety'}],
                                ['Record.Section.Information.Name', {'Name': 'Chemical Safety'}]]],

    [2526, [['Record.Section.Section.Section.Information.Value.Number', 2526],
            ['Record.Section.Section.Section.Information.Value.Number', 2526]]],

    ["3D Conformer", [['Record.Section.Section.TOCHeading', {'TOCHeading': '3D Conformer'}]]],

    [None, [['test_null', {'test_null': None}]]]
]


@pytest.mark.parametrize("input, output", targets)
def test_result_multi(example_json, input, output):
    search = DictSearch(data=example_json, target=input, return_func=None)
    assert search.result == output


def test_result_v_error(example_json):
    with pytest.raises(TypeError):
        search = DictSearch(data=example_json, target={"*", "*"}, return_func=None)


def test_result_t_error(example_json):
    with pytest.raises(TypeError):
        search = DictSearch(data=example_json, target=["fish"], return_func=None)


def test_result_parent(example_json):
    search = DictSearch(data=example_json, target="3D Conformer", return_func=DictSearch.return_parent_object)
    assert search.result == [['Record.Section.Section.TOCHeading', {
        'TOCHeading': '3D Conformer',
        'Description': 'A three-dimensional representation of the compound. The 3D structure is not experimentally determined, but computed by PubChem. More detailed information on this conformer model is described in the PubChem3D thematic series published in the Journal of Cheminformatics.',
        'DisplayControls': {'MoveToTop': True},
        'Information': [{'ReferenceNumber': 73, 'Description': '1-Chloro-2,4-dinitrobenzene', 'Value': {'Number': [6]}}]
    }]]
