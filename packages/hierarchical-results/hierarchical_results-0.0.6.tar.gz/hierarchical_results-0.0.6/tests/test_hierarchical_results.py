import pytest
from hierarchical_results.hierarchical_results import HierarchicalResults, ParameterCombinations
import numpy as np


@pytest.fixture
def parameter_names():
    return ["a", "b", "c", "d"]


@pytest.fixture
def result_names():
    return ["result1", "result2", "result3"]


@pytest.fixture()
def hr(parameter_names, result_names):
    return HierarchicalResults(parameter_names, result_names)


def test_store_and_get_result(hr):
    parameters = ["asdf", "1", "123", "a"]
    hr.store_result(parameters, "result2", 1.5)
    assert hr.get_result(parameters, "result2") == 1.5


def test_results_as_dataframe(hr):
    hr.store_result(["asdf", 1, "test", "test"], "result3", 101)
    hr.store_result(["asdf", 2, "test", "test"], "result3", 102)
    hr.store_result(["asdf", 3, "test", "test"], "result3", 103)

    hr.store_result(["asdf", 1, "test", "test"], "result1", 1)
    hr.store_result(["asdf", 2, "test", "test"], "result1", 2)
    hr.store_result(["asdf", 3, "test", "test"], "result1", 3)

    parameter_combinations = ParameterCombinations(hr._parameter_names, ["asdf", [1, 2, 3], "test", "test"])
    df = hr.get_results_dataframe(parameter_combinations, ["result3", "result1"])
    assert np.all(df.result3 == [101, 102, 103]), df.result3
    assert np.all(df.result1 == [1, 2, 3])


def test_get_result_file_names(hr):
    parameter_combinations = ParameterCombinations(hr._parameter_names, ["asdf", [0, 2, 3], "test", "test"])
    parameter_combinations.set("d", ["one", "two"])
    file_names = hr.get_result_file_names(parameter_combinations, ["result1", "result2"])
    print(file_names)
    assert len(file_names) == 12


def test_array_result(hr):
    pass
