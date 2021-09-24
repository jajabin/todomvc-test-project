import pytest
from selene import have
from selene.support.shared import browser


class AtTodoMvcTest:

    @pytest.fixture(scope='function', autouse=True)
    def open_app(self):
        already_tested = browser.matching(have.url_containing(browser.config.base_url))

        browser.open(browser.config.base_url)
        browser.should(have.js_returned(
            True,
            'return Object.keys(require.s.contexts._.defined).length === 39'))

        if already_tested:
            browser.clear_local_storage()
            browser.driver.refresh()
            browser.should(have.js_returned(
                True,
                'return Object.keys(require.s.contexts._.defined).length === 39'))

        yield

