"""Casos de teste de interface: cadastro de produto pelo administrador."""
import re

import pytest
from playwright.sync_api import Page, expect

from pages.admin_page import CadastroProdutoPage, HomeAdminPage, ListaProdutosAdminPage
from pages.login_page import LoginPage
from utils.dados import novo_produto

pytestmark = pytest.mark.web


def test_ct_web_11_administrador_cadastra_produto(page: Page, api, admin):
    produto = novo_produto(quantidade=7)
    LoginPage(page).abrir().entrar(admin["email"], admin["password"])
    HomeAdminPage(page).botao_cadastrar_produtos.click()

    CadastroProdutoPage(page).cadastrar(produto)

    expect(page).to_have_url(re.compile(r"/admin/listarprodutos$"))
    linha = ListaProdutosAdminPage(page).linha_do_produto(produto["nome"])
    expect(linha).to_have_count(1)
    expect(linha).to_contain_text(str(produto["preco"]))
    expect(linha).to_contain_text(produto["descricao"])

    # Verificação e limpeza pela API
    encontrados = api.listar_produtos(nome=produto["nome"]).json()["produtos"]
    assert encontrados[0]["quantidade"] == 7
    api.excluir_produto(encontrados[0]["_id"], admin["token"])
