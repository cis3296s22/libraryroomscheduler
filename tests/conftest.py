
def pytest_addoption(parser):
    parser.addoption("--user", action="store", default="default name")
    parser.addoption("--passW", action="store", default="default name")


def pytest_generate_tests(metafunc):
    # This is called for every test. Only get/set command line arguments
    # if the argument is specified in the list of test "fixturenames".
    option_value = metafunc.config.option.user
    option_value2 = metafunc.config.option.passW
    if 'user' in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("user", [option_value])
    if 'passW' in metafunc.fixturenames and option_value2 is not None:
        metafunc.parametrize("passW", [option_value2])
