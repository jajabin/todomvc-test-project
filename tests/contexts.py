import pytest
from selene import have
from selene.support.shared import browser


class AtTodoMvcTest:

    @pytest.fixture(scope='function', autouse=True)
    def open_app(self):
        browser.open('#/')
        browser.should(have.js_returned(True, 'return Object.keys(require.s.contexts._.defined).length === 39'))

    @pytest.fixture(scope='function', autouse=True)
    def clear_data_after_each_test(self):
        yield
        browser.clear_local_storage()
