"""Casos de teste de interface: fluxo de compra do cliente.

O produto é criado pela API (pré-condição rápida e confiável) e todo o
fluxo do cliente é executado pela tela.
"""
import re

import pytest
from playwright.sync_api import Page, expect

from pages.home_cliente_page import HomeClientePage
from pages.lista_compras_page import ListaComprasPage
from pages.login_page import LoginPage

pytestmark = pytest.mark.web


@pytest.fixture
def home_logada(page: Page, produto, cliente) -> HomeClientePage:
    LoginPage(page).abrir().entrar(cliente["email"], cliente["password"])
    home = HomeClientePage(page)
    expect(home.titulo).to_be_visible()
    return home


def test_ct_web_08_pesquisar_produto(home_logada: HomeClientePage, produto):
    home_logada.pesquisar(produto["nome"])

    expect(home_logada.cards).to_have_count(1)
    expect(home_logada.cards.first).to_contain_text(produto["nome"])
    expect(home_logada.cards.first).to_contain_text(str(produto["preco"]))


def test_ct_web_09_adicionar_produto_na_lista(page: Page, home_logada, produto):
    home_logada.pesquisar(produto["nome"])

    home_logada.adicionar_na_lista(produto["nome"])

    expect(page).to_have_url(re.compile(r"/minhaListaDeProdutos$"))
    lista = ListaComprasPage(page)
    expect(lista.nomes_produtos).to_have_count(1)
    expect(lista.nomes_produtos.first).to_contain_text(produto["nome"])
    expect(lista.quantidades.first).to_contain_text("1")


def test_ct_web_10_alterar_quantidade_e_limpar_lista(page: Page, home_logada, produto):
    home_logada.pesquisar(produto["nome"])
    home_logada.adicionar_na_lista(produto["nome"])
    lista = ListaComprasPage(page)

    lista.botao_aumentar.first.click()
    lista.botao_aumentar.first.click()
    expect(lista.quantidades.first).to_contain_text("3")

    lista.botao_diminuir.first.click()
    expect(lista.quantidades.first).to_contain_text("2")

    lista.botao_limpar.click()
    expect(lista.mensagem_vazia).to_have_text("Seu carrinho está vazio")
