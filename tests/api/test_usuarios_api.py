"""Casos de teste do CRUD de usuários (/usuarios)."""
import pytest

from utils.contrato import validar_contrato
from utils.dados import novo_usuario

pytestmark = pytest.mark.api


def test_ct_api_04_cadastrar_usuario(api):
    usuario = novo_usuario()

    resposta = api.criar_usuario(usuario)

    assert resposta.status == 201
    corpo = resposta.json()
    assert corpo["message"] == "Cadastro realizado com sucesso"
    assert corpo["_id"]
    api.excluir_usuario(corpo["_id"])  # limpeza


def test_ct_api_05_cadastrar_usuario_com_email_ja_usado(api, cliente):
    duplicado = novo_usuario()
    duplicado["email"] = cliente["email"]

    resposta = api.criar_usuario(duplicado)

    assert resposta.status == 400
    assert resposta.json()["message"] == "Este email já está sendo usado"


@pytest.mark.parametrize(
    "campo, valor",
    [("nome", ""), ("email", "sem-arroba"), ("password", ""), ("administrador", "talvez")],
    ids=["nome-vazio", "email-invalido", "senha-vazia", "administrador-invalido"],
)
def test_ct_api_06_cadastrar_usuario_com_dados_invalidos(api, campo, valor):
    usuario = novo_usuario()
    usuario[campo] = valor

    resposta = api.criar_usuario(usuario)

    assert resposta.status == 400
    assert campo in resposta.json()


def test_ct_api_07_buscar_usuario_por_id_valida_contrato(api, cliente):
    resposta = api.buscar_usuario(cliente["_id"])

    assert resposta.status == 200
    corpo = resposta.json()
    validar_contrato(corpo, "usuario")
    assert corpo["email"] == cliente["email"]
    assert corpo["nome"] == cliente["nome"]


def test_ct_api_08_buscar_usuario_inexistente(api):
    # O ServeRest exige IDs com 16 caracteres alfanuméricos
    resposta = api.buscar_usuario("IdInexistente000")

    assert resposta.status == 400
    assert resposta.json()["message"] == "Usuário não encontrado"


def test_ct_api_09_editar_usuario(api, cliente):
    alterado = {
        "nome": "Nome Alterado Pelo Teste",
        "email": cliente["email"],
        "password": cliente["password"],
        "administrador": "false",
    }

    resposta = api.editar_usuario(cliente["_id"], alterado)

    assert resposta.status == 200
    assert resposta.json()["message"] == "Registro alterado com sucesso"
    assert api.buscar_usuario(cliente["_id"]).json()["nome"] == "Nome Alterado Pelo Teste"


def test_ct_api_10_excluir_usuario(api):
    usuario = novo_usuario()
    _id = api.criar_usuario(usuario).json()["_id"]

    resposta = api.excluir_usuario(_id)

    assert resposta.status == 200
    assert resposta.json()["message"] == "Registro excluído com sucesso"
    assert api.buscar_usuario(_id).status == 400
