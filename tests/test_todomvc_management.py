from selene import have
from selene.support.shared import browser
from tests.contexts import AtTodoMvcTest


class TestTodoMVCManagement(AtTodoMvcTest):

    def test_add(self):
        add('a')
        assert_todos('a')

    def test_edit(self):
        add('a', 'b')
        edit('a', 'a edited')
        assert_todos('a edited', 'b')

    def test_delete(self):
        add('a', 'b')
        delete('a')
        assert_todos('b')

    def test_complete(self):
        add('a')
        toggle('a')
        assert_todos_completed()

    def test_uncomplete(self):
        add('a', 'b')
        toggle('a')
        toggle('a')
        assert_todos_completed()

    def test_complete_all(self):
        add('a', 'b')
        toggle_all()
        assert_todos_completed()

    def test_uncomplete_all(self):
        add('a', 'b')
        toggle_all()
        toggle_all()
        assert_todos_completed()

    def test_number_left(self):
        add('a', 'b')
        toggle('a')
        assert_todos_left()

    def test_is_clear_completed_visible(self):
        add('a', 'b')
        assert_is_clear_completed_visible()

    def test_clear_completed(self):
        add('a', 'b')
        toggle('a')
        clear_completed()
        assert_todos('b')

    def test_basic_todos_workflow(self):
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
        add('a', 'b', 'c')

        toggle('a')

        filter_active()
        assert_todos('b', 'c')

        filter_completed()
        assert_todos('a')

        filter_all()
        assert_todos('a', 'b', 'c')



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


def toggle_all():
    browser.element('#toggle-all').click()


def clear_completed():
    browser.element('#clear-completed').click()


def filter_active():
    browser.element('[href="#/active"]').click()


def filter_completed():
    browser.element('[href="#/completed"]').click()


def filter_all():
    browser.element('[href="#/all"]').click()


def assert_todos(*names):
    todos.should(have.exact_texts(*names))


def assert_todos_completed():
    pass


def assert_todos_left():
    pass


def assert_is_clear_completed_visible():
    pass