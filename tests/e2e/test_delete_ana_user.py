from playwright.sync_api import Page


def test_delete_ana_user(page: Page) -> None:
    page.goto("http://localhost:8000/admin/login/?next=/admin/")
    page.get_by_label("Username:").fill("admin")
    page.get_by_label("Username:").press("Tab")
    page.get_by_label("Password:").fill("admin")
    page.get_by_label("Password:").press("Enter")
    page.get_by_role("link", name="Users").click()
    page.get_by_role("link", name="ana").click()
    page.get_by_role("link", name="Delete").click()
    page.get_by_role("button", name="Yes, I’m sure").click()
