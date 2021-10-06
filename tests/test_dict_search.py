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

    [{"TOCHeading": "Structures"}, [['Record.Section.0.TOCHeading', {'TOCHeading': 'Structures'}]]],

    [{"TOCHeading": "3D Conformer"}, [['Record.Section.0.Section.1.TOCHeading', {'TOCHeading': '3D Conformer'}]]],

    [{"MoveToTop": "*"}, [['Record.Section.1.DisplayControls.MoveToTop', {'MoveToTop': True}],
                          ['Record.Section.0.Section.0.DisplayControls.MoveToTop', {'MoveToTop': True}],
                          ['Record.Section.0.Section.1.DisplayControls.MoveToTop', {'MoveToTop': True}],
                          ['Record.Section.2.Section.0.DisplayControls.MoveToTop', {'MoveToTop': True}],
                          ['Record.Section.2.Section.2.DisplayControls.MoveToTop', {'MoveToTop': True}],
                          ['Record.Section.2.Section.5.DisplayControls.MoveToTop', {'MoveToTop': True}],
                          ['Record.Section.2.Section.6.DisplayControls.MoveToTop', {'MoveToTop': True}],
                          ['Record.Section.2.Section.4.Section.1.DisplayControls.MoveToTop', {'MoveToTop': True}],
                          ['Record.Section.3.Section.0.Section.0.DisplayControls.MoveToTop', {'MoveToTop': True}]]
     ],
    [{"*": "Chemical Safety"}, [['Record.Section.1.TOCHeading', {'TOCHeading': 'Chemical Safety'}],
                                ['Record.Section.1.Information.0.Name', {'Name': 'Chemical Safety'}]]],

    [2526, [['Record.Section.3.Section.1.Section.14.Information.1.Value.Number', 2526],
            ['Record.Section.3.Section.1.Section.14.Information.1.Value.Number', 2526]]],

    ["3D Conformer", [['Record.Section.0.Section.1.TOCHeading', {'TOCHeading': '3D Conformer'}]]],

    [None, [['test_null', {'test_null': None}]]],

    ["cat", [['testing.1', 'cat']]]
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
    assert search.result == [['Record.Section.0.Section.1.TOCHeading', {
        'TOCHeading': '3D Conformer',
        'Description': 'A three-dimensional representation of the compound. The 3D structure is not experimentally determined, but computed by PubChem. More detailed information on this conformer model is described in the PubChem3D thematic series published in the Journal of Cheminformatics.',
        'DisplayControls': {'MoveToTop': True},
        'Information': [{'ReferenceNumber': 73, 'Description': '1-Chloro-2,4-dinitrobenzene', 'Value': {'Number': [6]}}]
    }]]


targets_regex = [
    ["^[A-I]{3}$", [['Record.RecordType', {'RecordType': 'CID'}],
                    ['Record.Section.18.Section.0.Section.0.Information.0.Name', {'Name': 'HID'}],
                    ['Record.Section.18.Section.0.Section.1.Information.0.Name', {'Name': 'HID'}],
                    ['Record.Section.18.Section.0.Section.2.Information.0.Name', {'Name': 'HID'}],
                    ['Record.Section.18.Section.0.Section.3.Information.0.Name', {'Name': 'HID'}],
                    ['Record.Section.18.Section.0.Section.4.Information.0.Name', {'Name': 'HID'}],
                    ['Record.Section.18.Section.0.Section.5.Information.0.Name', {'Name': 'HID'}],
                    ['Record.Section.18.Section.0.Section.6.Information.0.Name', {'Name': 'HID'}],
                    ['Record.Section.18.Section.0.Section.7.Information.0.Name', {'Name': 'HID'}],
                    ['Record.Section.18.Section.0.Section.8.Information.0.Name', {'Name': 'HID'}],
                    ['Record.Section.14.Section.6.Information.0.Value.StringWithMarkup.5.String', {'String': 'CID'}],
                    ['Record.Section.14.Section.6.Information.0.Value.StringWithMarkup.6.String', {'String': 'CID'}],
                    ['Record.Section.14.Section.7.Information.0.Value.StringWithMarkup.5.String', {'String': 'CID'}],
                    ['Record.Section.14.Section.8.Information.0.Value.StringWithMarkup.5.String', {'String': 'CID'}],
                    ['Record.Section.4.Section.1.Section.2.Information.20.Value.StringWithMarkup.0.String',
                     {'String': 'CID'}]]
     ],

    [{"*": ".*compound$"},
     [['Record.Section.13.Description', {'Description': 'Disease information available for this compound'}],
      ['Record.Section.0.Section.0.Description', {'Description': 'A two-dimensional representation of the compound'}]]],

    [{"^RecordT": "*"}, [['Record.RecordTitle', {'RecordTitle': '1-Chloro-2,4-dinitrobenzene'}],
                         ['Record.RecordType', {'RecordType': 'CID'}]]],

    [{"^TOC.*": "Chemical.{0,10}$"}, [['Record.Section.1.TOCHeading', {'TOCHeading': 'Chemical Safety'}],
                                      ['Record.Section.6.TOCHeading', {'TOCHeading': 'Chemical Vendors'}]]],

    [2526, [['Record.Section.3.Section.1.Section.14.Information.1.Value.Number', 2526],
            ['Record.Section.3.Section.1.Section.14.Information.1.Value.Number', 2526]]],

    [None, [['test_null', {'test_null': None}]]]
]


@pytest.mark.parametrize("input, output", targets_regex)
def test_result_multi2(example_json, input, output):
    search = DictSearch(data=example_json, target=input, op_regex=True, return_func=None)
    assert search.result == output


def test_result_v_error2(example_json):
    with pytest.raises(TypeError):
        search = DictSearch(data=example_json, target={"*", "*"}, op_regex=True, return_func=None)