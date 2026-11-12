"""Casos de teste de interface: cadastro de usuário.

Os dados criados pela tela são conferidos e removidos pela API, mostrando
a integração entre os dois níveis de teste.
"""
import re

import pytest
from playwright.sync_api import Page, expect

from pages.cadastro_usuario_page import CadastroUsuarioPage
from pages.home_cliente_page import HomeClientePage
from utils.dados import novo_usuario

pytestmark = pytest.mark.web


def test_ct_web_06_cadastro_de_cliente_pela_tela(page: Page, api):
    usuario = novo_usuario()
    cadastro = CadastroUsuarioPage(page).abrir()

    cadastro.cadastrar(usuario["nome"], usuario["email"], usuario["password"])

    expect(cadastro.alerta).to_contain_text("Cadastro realizado com sucesso")
    expect(page).to_have_url(re.compile(r"/home$"), timeout=10_000)
    expect(HomeClientePage(page).titulo).to_be_visible()

    # Verificação pela API: o usuário foi gravado com os dados corretos
    encontrados = api.listar_usuarios(email=usuario["email"]).json()["usuarios"]
    assert len(encontrados) == 1
    assert encontrados[0]["nome"] == usuario["nome"]
    assert encontrados[0]["administrador"] == "false"
    api.excluir_usuario(encontrados[0]["_id"])  # limpeza


def test_ct_web_07_cadastro_com_email_ja_usado(page: Page, cliente):
    cadastro = CadastroUsuarioPage(page).abrir()

    cadastro.cadastrar("Outro Nome", cliente["email"], "Senha@123")

    expect(cadastro.alerta).to_contain_text("Este email já está sendo usado")
    expect(page).to_have_url(re.compile(r"/cadastrarusuarios$"))
