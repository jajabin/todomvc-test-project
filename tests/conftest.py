import pytest
from selene.support.shared import browser


def pytest_addoption(parser):
    parser.addoption("--base_url",
                     default="https://todomvc4tasj.herokuapp.com/",
                     type=str,
                     action="store")
    parser.addoption("--timeout",
                     default=4,
                     type=float,
                     action="store")
    parser.addoption("--save_page_source_on_failure",
                     default=True,
                     type=bool,
                     action="store")


@pytest.fixture(scope='function', autouse=True)
def browser_setup(pytestconfig):
    browser.config.base_url = pytestconfig.getoption("base_url")
    browser.config.timeout = pytestconfig.getoption("timeout")
    browser.config.save_page_source_on_failure = \
        pytestconfig.getoption("save_page_source_on_failure")

    browser.config.set_value_by_js = True

