from playwright.sync_api import Page


class HomeClientePage:
    def __init__(self, page: Page):
        self.page = page
        self.titulo = page.get_by_role("heading", name="Serverest Store")
        self.campo_pesquisa = page.get_by_test_id("pesquisar")
        self.botao_pesquisar = page.get_by_test_id("botaoPesquisar")
        self.cards = page.locator(".card")
        self.menu_lista_compras = page.get_by_test_id("lista-de-compras")
        self.botao_logout = page.get_by_test_id("logout")

    def pesquisar(self, termo: str):
        # Espera a lista inicial de produtos carregar antes de pesquisar;
        # sem isso, a lista completa pode chegar depois e sobrescrever o filtro.
        self.cards.first.wait_for()
        self.campo_pesquisa.fill(termo)
        self.botao_pesquisar.click()

    def card_do_produto(self, nome: str):
        return self.cards.filter(has_text=nome)

    def adicionar_na_lista(self, nome: str):
        self.card_do_produto(nome).get_by_test_id("adicionarNaLista").click()
