from selene import have
from selene.support.shared import browser


class TestTodoMVCManagement:

    def test_basic_todos_workflow(self):
        open_app()

        add('a', 'b', 'c')
        assert_todos('a', 'b', 'c')

        edit('a', 'a edited')

        delete('a edited')
        assert_todos('b', 'c')

        cancel_editing('b', 'b to be canceled')

        toggle('b')

        clear_completed()
        assert_todos('c')

    def test_filtering(self):
        open_app()

        add('a', 'b', 'c')

        toggle('a')

        filter_active()
        assert_todos('b', 'c')

        filter_completed()
        assert_todos('a')

        filter_all()
        assert_todos('a', 'b', 'c')


def open_app():
    already_tested = browser.matching(have.url_containing(browser.config.base_url))

    if already_tested:
        browser.clear_local_storage()

    browser.open('#/')
    browser.should(have.js_returned(
        True,
        'return Object.keys(require.s.contexts._.defined).length === 39'))

    yield


todos = browser.all('#todo-list>li')


def todo(name: str):
    return todos.element_by(have.exact_text(name))


def add(*names):
    for name in names:
        browser.element('#new-todo').type(name).press_enter()


def start_edit(name: str, new_name: str):
    todo(name).double_click()
    return todos.element_by(have.css_class('editing')).element('.edit').set_value(new_name)


def edit(name: str, new_name: str):
    return start_edit(name, new_name).press_enter()


def cancel_editing(name: str, new_name: str):
    return start_edit(name, new_name).press_escape()


def delete(name: str):
    todo(name).hover().element('.destroy').click()


def toggle(name: str):
    todo(name).element('.toggle').click()


def clear_completed():
    browser.element('#clear-completed').click()


def assert_todos(*names):
    todos.should(have.exact_texts(*names))


def filter_active():
    browser.element('//*[@href="#/active"]').click()


def filter_completed():
    browser.element('//*[@href="#/completed"]').click()


def filter_all():
    browser.element('//*[@href="#/"]').click()

