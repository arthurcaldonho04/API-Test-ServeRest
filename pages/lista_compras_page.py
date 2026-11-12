"""Page Object da lista de compras (/minhaListaDeProdutos)."""
from playwright.sync_api import Page


class ListaComprasPage:
    def __init__(self, page: Page):
        self.page = page
        self.nomes_produtos = page.get_by_test_id("shopping-cart-product-name")
        self.quantidades = page.get_by_test_id("shopping-cart-product-quantity")
        self.botao_aumentar = page.get_by_test_id("product-increase-quantity")
        self.botao_diminuir = page.get_by_test_id("product-decrease-quantity")
        self.botao_limpar = page.get_by_test_id("limparLista")
        self.mensagem_vazia = page.get_by_test_id("shopping-cart-empty-message")
