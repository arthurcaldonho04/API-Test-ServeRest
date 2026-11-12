"""Fixtures compartilhadas pelos testes de API e de interface.

Fixtures são as "pré-condições" dos casos de teste: criam os dados de que
cada teste precisa e removem esses dados no final (teardown).
"""
import pytest
from playwright.sync_api import Playwright

from utils.api_client import ServeRestApi
from utils.config import API_URL, FRONT_URL
from utils.dados import novo_produto, novo_usuario


@pytest.fixture(scope="session")
def base_url():
    """URL do front-end usada pelo pytest-playwright em page.goto("/...")."""
    return FRONT_URL


@pytest.fixture(scope="session")
def api(playwright: Playwright):
    contexto = playwright.request.new_context(
        base_url=API_URL,
        extra_http_headers={"Content-Type": "application/json"},
    )
    yield ServeRestApi(contexto)
    contexto.dispose()


def _criar_usuario(api: ServeRestApi, administrador: bool) -> dict:
    usuario = novo_usuario(administrador=administrador)
    resposta = api.criar_usuario(usuario)
    assert resposta.status == 201, resposta.text()
    usuario["_id"] = resposta.json()["_id"]
    usuario["token"] = api.token(usuario["email"], usuario["password"])
    return usuario


@pytest.fixture
def admin(api):
    """Usuário administrador já cadastrado e com token de acesso."""
    usuario = _criar_usuario(api, administrador=True)
    yield usuario
    api.cancelar_compra(usuario["token"])
    api.excluir_usuario(usuario["_id"])


@pytest.fixture
def cliente(api):
    """Usuário comum (não administrador) já cadastrado e com token."""
    usuario = _criar_usuario(api, administrador=False)
    yield usuario
    api.cancelar_compra(usuario["token"])
    api.excluir_usuario(usuario["_id"])


@pytest.fixture
def produto(api, admin):
    """Produto cadastrado via API por um administrador."""
    dados = novo_produto()
    resposta = api.criar_produto(dados, admin["token"])
    assert resposta.status == 201, resposta.text()
    dados["_id"] = resposta.json()["_id"]
    yield dados
    api.excluir_produto(dados["_id"], admin["token"])
