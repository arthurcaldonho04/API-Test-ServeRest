"""Casos de teste de /produtos, incluindo regras de autorização."""
import pytest

from utils.contrato import validar_contrato
from utils.dados import novo_produto

pytestmark = pytest.mark.api

MSG_TOKEN = "Token de acesso ausente, inválido, expirado ou usuário do token não existe mais"


def test_ct_api_11_listar_produtos_valida_contrato(api, produto):
    resposta = api.listar_produtos()

    assert resposta.status == 200
    validar_contrato(resposta.json(), "lista_produtos")


def test_ct_api_12_cadastrar_produto_como_administrador(api, admin):
    dados = novo_produto()

    resposta = api.criar_produto(dados, admin["token"])

    assert resposta.status == 201
    assert resposta.json()["message"] == "Cadastro realizado com sucesso"
    _id = resposta.json()["_id"]
    cadastrado = api.buscar_produto(_id).json()
    assert cadastrado["nome"] == dados["nome"]
    assert cadastrado["preco"] == dados["preco"]
    api.excluir_produto(_id, admin["token"])  # limpeza


def test_ct_api_13_cadastrar_produto_sem_token(api):
    resposta = api.criar_produto(novo_produto(), token=None)

    assert resposta.status == 401
    assert resposta.json()["message"] == MSG_TOKEN


def test_ct_api_14_cadastrar_produto_com_token_invalido(api):
    resposta = api.criar_produto(novo_produto(), token="Bearer token.invalido.123")

    assert resposta.status == 401
    assert resposta.json()["message"] == MSG_TOKEN


def test_ct_api_15_cadastrar_produto_como_usuario_comum(api, cliente):
    resposta = api.criar_produto(novo_produto(), cliente["token"])

    assert resposta.status == 403
    assert resposta.json()["message"] == "Rota exclusiva para administradores"


def test_ct_api_16_cadastrar_produto_com_nome_duplicado(api, admin, produto):
    duplicado = novo_produto()
    duplicado["nome"] = produto["nome"]

    resposta = api.criar_produto(duplicado, admin["token"])

    assert resposta.status == 400
    assert resposta.json()["message"] == "Já existe produto com esse nome"


def test_ct_api_17_buscar_produto_por_nome(api, produto):
    resposta = api.listar_produtos(nome=produto["nome"])

    assert resposta.status == 200
    corpo = resposta.json()
    assert corpo["quantidade"] == 1
    assert corpo["produtos"][0]["_id"] == produto["_id"]
