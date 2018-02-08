from classifications_service.services.valuea.machine_learning.training_service.training import kmeans


class TrainingDictionary(object):

    _function_map = {
        'k-means': kmeans.train,
    }

    def __init__(self, params):
        self.params = params

    def get_training_method(self, params):
        try:
            return self._function_map[params['function_name']]
        except TypeError:
            print('Unknown training method, skipping:')
            print(params['function_name'])
            return None
