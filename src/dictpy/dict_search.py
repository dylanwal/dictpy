"""
This contains DictSearch which is used to search python dictionaries.
"""


from typing import Union, Dict, List, Callable, Optional, Any
import re


class DictSearch:

    def __init__(self,
                 data: Dict[str, Any],
                 target: Union[str, int, float, Dict[str, Any], None],
                 return_func: Optional[Callable[[Any, Any], Any]] = None,
                 op_regex: bool = False,
                 op_convert_str_to_num: bool = True,
                 op_sort_result: bool = True
                 ):
        """

        :param data: The python dictionary you want to search
        :param target: The target you want to find in the python dictionary
        :param return_func: The return you want to get. Default -> current object
        :param op_regex: target strings are regular expression
        :param op_convert_str_to_num: Option to covert numbers that are strings into numerical values when searching
        (not used when op_regex is True)
        :param op_sort_result: Option to sort  result by tree length (short first) then alphabetical.
        """
        self._target_not_dict = False
        self.op_regex = op_regex
        self._check_target_function = self.target_check_function_selector(target)
        self.op_convert_str_to_num = op_convert_str_to_num if op_regex is False else False
        self.data = data
        self.target = target
        self.return_func = return_func if return_func is not None else DictSearch.return_current_object

        self.result = self.sort_result(self.extract(self.data)) if op_sort_result else self.extract(self.data)

    def target_check_function_selector(self, target) -> Callable[[Any, Optional[Any]], Any]:
        """Given a target choose the correct target check function."""
        if not self.op_regex:
            if isinstance(target, dict) and len(target.keys()) == 1 and len(target.values()) == 1:
                if list(target.keys())[0] == "*":
                    func_out = self._check_target_wild_key
                elif list(target.values())[0] == "*":
                    func_out = self._check_target_wild_value
                else:
                    func_out = self._check_target_dict

            elif isinstance(target, str):
                self._target_not_dict = True
                func_out = self._check_target_str

            elif isinstance(target, (float, int)):
                self._target_not_dict = True
                func_out = self._check_target_num

            elif target is None:
                self._target_not_dict = True
                func_out = self._check_target_none

            else:
                raise TypeError("Invalid 'target' type, or both key and value were wildcards (*) which is invalid.")

        else:
            if isinstance(target, dict) and len(target.keys()) == 1 and len(target.values()) == 1:
                if list(target.keys())[0] == "*":
                    func_out = self._check_target_wild_key_regex
                elif list(target.values())[0] == "*":
                    func_out = self._check_target_wild_value_regex
                else:
                    func_out = self._check_target_dict_regex

            elif isinstance(target, str):
                self._target_not_dict = True
                func_out = self._check_target_str_regex

            elif isinstance(target, (float, int)):
                self._target_not_dict = True
                func_out = self._check_target_num

            elif target is None:
                self._target_not_dict = True
                func_out = self._check_target_none

            else:
                raise TypeError("Invalid 'target' type, or both key and value were wildcards (*) which is invalid.")

        return func_out

    # Check target functions
    def _check_target_dict(self, k: str, v: Any) -> bool:
        if self.op_convert_str_to_num:
            v = self.str_to_num(v)

        if k == list(self.target.keys())[0] and v == list(self.target.values())[0]:
            return True
        return False

    def _check_target_dict_regex(self, k: str, v: Any) -> bool:
        if (isinstance(k, str) and bool(re.match(list(self.target.keys())[0], k))) and \
                (isinstance(v, str) and bool(re.match(list(self.target.values())[0], v))):
            return True
        return False

    def _check_target_wild_value(self, k: str, _: Any) -> bool:
        if k == list(self.target.keys())[0]:
            return True
        return False

    def _check_target_wild_value_regex(self, k: str, _: Any) -> bool:
        if (isinstance(k, str) and bool(re.match(list(self.target.keys())[0], k))):
            return True
        return False

    def _check_target_wild_key(self, _: str, v: Any) -> bool:
        if self.op_convert_str_to_num:
            v = self.str_to_num(v)

        if v == list(self.target.values())[0]:
            return True
        return False

    def _check_target_wild_key_regex(self, _: str, v: Any) -> bool:
        if (isinstance(v, str) and bool(re.match(list(self.target.values())[0], v))):
            return True
        return False

    def _check_target_str(self, k: Any, v: Optional[Any] = None) -> bool:
        if (isinstance(k, str) and k == self.target) or (isinstance(v, str) and v == self.target):
            return True
        return False

    def _check_target_str_regex(self, k: Any, v: Optional[Any] = None) -> bool:
        if (isinstance(k, str) and bool(re.match(self.target, k))) or \
                (isinstance(v, str) and bool(re.match(self.target, v))):
            return True
        return False

    def _check_target_none(self, k: Any, v: Optional[Any] = "") -> bool:
        if (k is None) or (v is None):
            return True
        return False

    def _check_target_num(self, k: Any, v: Optional[Any] = None) -> bool:
        if self.op_convert_str_to_num:
            k = self.str_to_num(k)
            v = self.str_to_num(v)

        if k == self.target or v == self.target:
            return True
        return False

    @staticmethod
    def str_to_num(value):
        if isinstance(value, str):
            try:
                value = float(value.replace(" ", ""))
            except ValueError:
                pass

        return value

    # Return Options
    @staticmethod
    def return_current_object(_, obj):
        return obj

    @staticmethod
    def return_parent_object(parent, _):
        return parent

    # Main code
    def extract(self, obj) -> List[Any]:
        out = []
        if isinstance(obj, dict):
            for k, v in obj.items():
                if self._check_target_function(k, v):
                    out.append([k, self.return_func(obj, {k: v})])

                elif isinstance(v, dict) or isinstance(v, list):
                    results = self.extract(v)
                    if results != []:
                        for result in results:
                            if isinstance(result, list) and len(result) == 2:
                                result[0] = ".".join([k, result[0]])
                            else:
                                result = [k, result]
                            out.append(result)

        elif isinstance(obj, list):
            for i, obj_ in enumerate(obj):
                if isinstance(obj_, dict) or isinstance(obj_, list):
                    results = self.extract(obj_)
                    for result in results:
                        if isinstance(result, list) and len(result) == 2:
                            result[0] = ".".join([str(i), result[0]])
                        else:
                            result = [str(i), result]
                        out.append(result)
                elif self._target_not_dict:
                    if self._check_target_function(obj_):
                        out.append(self.return_func(obj, obj_))

        return out

    def sort_result(self, result: List[Any]) -> List[Any]:
        """Sorts on tree depth then alphabetically on last tree key"""
        if result == []:
            return result

        return sorted(result, key=lambda pair: (pair[0].count("."), pair[0].split(".")[-1]))
