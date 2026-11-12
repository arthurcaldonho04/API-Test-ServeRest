"""Casos de teste da rota POST /login."""
import pytest

pytestmark = pytest.mark.api


def test_ct_api_01_login_com_credenciais_validas(api, cliente):
    resposta = api.login(cliente["email"], cliente["password"])

    assert resposta.status == 200
    corpo = resposta.json()
    assert corpo["message"] == "Login realizado com sucesso"
    assert corpo["authorization"].startswith("Bearer ")


def test_ct_api_02_login_com_senha_incorreta(api, cliente):
    resposta = api.login(cliente["email"], "senha_errada")

    assert resposta.status == 401
    assert resposta.json()["message"] == "Email e/ou senha inválidos"


@pytest.mark.parametrize(
    "email, senha, campo",
    [
        ("", "Senha@123", "email"),
        ("qa@teste.com.br", "", "password"),
        ("email_invalido", "Senha@123", "email"),
    ],
    ids=["email-vazio", "senha-vazia", "email-formato-invalido"],
)
def test_ct_api_03_login_com_campos_invalidos(api, email, senha, campo):
    resposta = api.login(email, senha)

    assert resposta.status == 400
    assert campo in resposta.json()
