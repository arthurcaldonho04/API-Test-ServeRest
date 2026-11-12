"""Page Object da tela de login (/login)."""
from playwright.sync_api import Page


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.campo_email = page.get_by_test_id("email")
        self.campo_senha = page.get_by_test_id("senha")
        self.botao_entrar = page.get_by_test_id("entrar")
        self.link_cadastrar = page.get_by_test_id("cadastrar")
        self.alerta_erro = page.locator(".alert").first

    def abrir(self):
        self.page.goto("/login")
        return self

    def entrar(self, email: str, senha: str):
        self.campo_email.fill(email)
        self.campo_senha.fill(senha)
        self.botao_entrar.click()
