import yaml
from .testers import Test
from .inputs import AbstractInput
from .testers import RegisteredTests
from .inputs import RegisteredInputs


class Configuration:
    @staticmethod
    def load_yaml(file):
        with open(file, mode='r') as conf_file:
            data = yaml.load(conf_file, Loader=yaml.FullLoader)
            # TODO: Validate Configuration
            return Configuration(data)

    def __init__(self, data):
        self.data = data

    def get_tests(self) -> (Test, AbstractInput):
        for test, config in self.data['tests'].items():

            test_class = RegisteredTests[
                config['type']['class']
            ](**config['type']['args'])

            input_class = RegisteredInputs[
                config['input']['class']
            ](**config['input']['args'])

            yield test_class, input_class


class Runner:
    def __init__(self, conf: Configuration):
        self.conf = conf
        self.tests = list(conf.get_tests())

    def run_tests(self):
        for test, input_data in self.tests:
            try:
                test.run(input_data)
            except Exception as ex:
                test.set_status(False, str(ex))

    def print_result(self):
        for test, input_data in self.tests:
            print(test)
