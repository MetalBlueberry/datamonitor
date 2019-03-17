import yaml

from .runner import Runner, Configuration

c = Configuration.load_yaml("tests/test.yaml")
r = Runner(c)
r.run_tests()
r.print_result()
