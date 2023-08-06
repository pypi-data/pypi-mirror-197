import itertools
from typing import List, Dict
import os
from pathlib import Path
import logging
import pandas as pd
from shared_memory_wrapper import from_file, to_file

class ParameterCombinations:
    def __init__(self, names: List[str], values: List):
        assert isinstance(values, list) and isinstance(names, list)
        self._names = names
        self._values = values

    @classmethod
    def from_path(cls, names, path):
        values = path.split("/")
        # if path is shorter, we allow fewer names
        names = names[0:len(values)]
        assert len(values) == len(names), "Got %d values and %d names" % (len(values), len(names))
        return cls(names, values)

    def set(self, name, value):
        assert name in self._names, "Name %s not in hiearchy %s" % (name, self._names)
        index = self._names.index(name)
        self._values[index] = value

    def combinations(self):
        # wrap strs in list to make product work
        values = [[v] if isinstance(v, str) else v for v in self._values]
        return [list(i) for i in itertools.product(*values)]


class HierarchicalResults:
    def __init__(self, parameter_names: List[str], result_names: List[str], prefix=""):
        self._prefix = prefix
        self._parameter_names = parameter_names
        self._result_names = result_names

    def get_names(self):
        return self._parameter_names

    def _get_parameter_path(self, parameters: List[str]) -> str:
        return self._prefix + os.path.sep.join([str(p) for p in parameters])

    def _get_result_path(self, parameters, result):
        return self._get_parameter_path(parameters) + os.path.sep + result + ".txt"

    def get_result(self, parameters: List[str], result: str):
        assert len(parameters) <= len(self._parameter_names), "Got more parameters %d than in hieararchy %d" % (len(parameters), len(self._parameter_names))
        file_name = self._get_result_path(parameters, result)
        return from_file(file_name)
        #with open(file_name) as f:
        #    return float(f.read().strip())

    def get_result_file_names(self, parameters: ParameterCombinations, result_names):
        file_names = []
        combinations = parameters.combinations()
        for combination in combinations:
            for result_name in result_names:
                file_names.append(self._get_result_path(combination, result_name))

        return file_names

    def get_results_dataframe(self, parameters: ParameterCombinations, result_names):
        """
        Gets the results specified by result_names from all the parameter combinations.
        Returns a Pandas Dataframe.
        """
        if isinstance(result_names, str):
            result_names = [result_names]

        for n in result_names:
            assert n in self._result_names

        combinations = parameters.combinations()
        results = []

        for combination in combinations:
            row = list(combination)
            for result_name in result_names:
                result = self.get_result(combination, result_name)
                row.append(result)
            results.append(row)

        return pd.DataFrame(results, columns=parameters._names + result_names)

    def store_result(self, parameters, result_name, result_value):
        path = self._get_parameter_path(parameters)
        logging.info("Storing to path %s" % path)
        Path(path).mkdir(parents=True, exist_ok=True)
        to_file(result_value, self._get_result_path(parameters, result_name))
        #with open(self._get_result_path(parameters, result_name), "w") as f:
        #    f.write(str(result_value) + "\n")


    def get_sublogger(self, fixed_parameter_values: List[str]):
        """
        Returns a sublogger where the first n parameter values are fixed.
        Using this sublogger, you only need to specify the reminding parameters.
        """
        raise NotImplementedError
