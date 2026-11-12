"""Page Object da tela de cadastro de usuário (/cadastrarusuarios)."""
from playwright.sync_api import Page


class CadastroUsuarioPage:
    def __init__(self, page: Page):
        self.page = page
        self.campo_nome = page.get_by_test_id("nome")
        self.campo_email = page.get_by_test_id("email")
        self.campo_senha = page.get_by_test_id("password")
        self.check_administrador = page.get_by_test_id("checkbox")
        self.botao_cadastrar = page.get_by_test_id("cadastrar")
        self.alerta = page.locator(".alert").first

    def abrir(self):
        self.page.goto("/cadastrarusuarios")
        return self

    def cadastrar(self, nome: str, email: str, senha: str, administrador: bool = False):
        self.campo_nome.fill(nome)
        self.campo_email.fill(email)
        self.campo_senha.fill(senha)
        if administrador:
            self.check_administrador.check()
        self.botao_cadastrar.click()
