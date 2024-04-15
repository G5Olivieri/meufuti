import pytest
from playwright.sync_api import Page


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, playwright):
    return {**playwright.devices["Galaxy S9+"]}


def test_delete_court(page: Page) -> None:
    page.goto("http://localhost:8000/courts/")
    page.get_by_label("Toggle navigation").click()
    page.get_by_label("Toggle navigation").click()
    page.get_by_role("link", name="Entrar").click()
    page.get_by_label("Usuário").click()
    page.get_by_label("Usuário").fill("ana")
    page.get_by_label("Usuário").press("Tab")
    page.get_by_label("Senha").fill("ana")
    page.get_by_label("Senha").press("Enter")
    page.get_by_role("link", name="Falc R. Dos Bobos, Jardim Ali").click()
    page.get_by_role("button", name="Excluir").click()
