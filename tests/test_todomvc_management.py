from selene import have
from selene.support.shared import browser
from tests.contexts import AtTodoMvcTest


class TestUserWorkflow(AtTodoMvcTest):

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
        assert_todos('a', 'b', 'c')

        toggle('a')
        filter('Active')
        assert_todos('b', 'c')

        filter('Completed')
        assert_todos('a')

        filter('All')
        assert_todos('a', 'b', 'c')


todos = browser.all('#todo-list>li')


def todo(name: str):
    return todos.element_by(have.exact_text(name))


def add(*names) -> None:
    for name in names:
        browser.element('#new-todo').type(name).press_enter()


def start_edit(name: str, new_name: str):
    todo(name).double_click()
    return todos.element_by(have.css_class('editing')).element('.edit').set_value(new_name)


def edit(name: str, new_name: str):
    return start_edit(name, new_name).press_enter()


def cancel_editing(name: str, new_name: str):
    return start_edit(name, new_name).press_escape()


def delete(name: str) -> None:
    todo(name).hover().element('.destroy').click()


def toggle(name: str) -> None:
    todo(name).element('.toggle').click()


def clear_completed() -> None:
    browser.element('#clear-completed').click()


def assert_todos(*names) -> None:
    todos.should(have.exact_texts(*names))


def filter(name: str) -> None:
    browser.all('#filters>li').element_by(have.exact_text(name)).click()
