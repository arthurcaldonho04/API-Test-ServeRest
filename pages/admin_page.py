"""Page Objects da área administrativa (/admin/...)."""
from playwright.sync_api import Page


class HomeAdminPage:
    def __init__(self, page: Page):
        self.page = page
        self.boas_vindas = page.get_by_role("heading", name="Bem Vindo")
        self.botao_cadastrar_produtos = page.get_by_test_id("cadastrarProdutos")
        self.botao_listar_produtos = page.get_by_test_id("listarProdutos")


class CadastroProdutoPage:
    def __init__(self, page: Page):
        self.page = page
        self.campo_nome = page.get_by_test_id("nome")
        self.campo_preco = page.get_by_test_id("preco")
        self.campo_descricao = page.get_by_test_id("descricao")
        self.campo_quantidade = page.get_by_test_id("quantity")
        self.botao_cadastrar = page.get_by_test_id("cadastarProdutos")

    def cadastrar(self, produto: dict):
        self.campo_nome.fill(produto["nome"])
        self.campo_preco.fill(str(produto["preco"]))
        self.campo_descricao.fill(produto["descricao"])
        self.campo_quantidade.fill(str(produto["quantidade"]))
        self.botao_cadastrar.click()


class ListaProdutosAdminPage:
    def __init__(self, page: Page):
        self.page = page
        self.linhas = page.locator("table tbody tr")

    def linha_do_produto(self, nome: str):
        return self.linhas.filter(has_text=nome)
