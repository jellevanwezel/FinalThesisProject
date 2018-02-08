import valuea_framework.broker.Service

from classifications_service.services.valuea.machine_learning.training_service.method_dictionaries.pre_processing_dictionary import \
    PreprocessingDictionary
from classifications_service.services.valuea.machine_learning.training_service.method_dictionaries.training_dictionary import \
    TrainingDictionary


class Service(valuea_framework.broker.Service.BaseService):

    pre_processing_dict = PreprocessingDictionary()
    training_dict = TrainingDictionary()

    def __init__(self, *args, **kwargs):
        super(Service, self).__init__(*args, **kwargs)

    def execute(self):
        params = self.get_message()
        pre_processing_params = params['preProcessingParams']
        training_params = params['trainingParams']
        database = params['db']

        preprocessed_results = self.start_preprocessing(pre_processing_params, database)

        return "success"

    def start_training(self, training_params, data_labels):
        trainer = self.training_dict.get_training_method(training_params)
        return trainer(data_labels,training_params)

    def start_preprocessing(self, pre_processing_params, db):
        for current_param in pre_processing_params:
                preprocessor = self.pre_processing_dict.get_preprocessing_method(current_param)
                db = preprocessor(db)
        return db
