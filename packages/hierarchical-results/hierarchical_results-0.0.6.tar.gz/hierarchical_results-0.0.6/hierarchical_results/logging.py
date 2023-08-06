loggers = {}
from .hierarchical_results import HierarchicalResults


def init_logger(name, parameter_names, result_names):
    global loggers
    loggers[name] = HierarchicalResults(parameter_names, result_names)
    return loggers[name]

def get_logger(name):
    return loggers[name]

