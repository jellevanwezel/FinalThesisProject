from classifications_service.services.valuea.machine_learning.training_service.preprocessing import normalize, gml
from classifications_service.services.valuea.machine_learning.training_service.preprocessing.pass_through import \
    pass_through


class PreprocessingDictionary(object):

    _function_map = {
        'none' : pass_through,
        'normalize': normalize.normalize,
        'gml': gml.gml
    }

    def __init__(self):
        pass

    def get_preprocessing_method(self, params):
        """

        :type params: List of function names, one or more of {'normalize', 'gml'}
        """
        try:
            return self._function_map[params['function_name']]
        except TypeError:
            print('Unknown preprocessing parameter, skipping:')
            print(params['function_name'])
            return self._function_map['none']
