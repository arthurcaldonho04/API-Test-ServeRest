"""Casos de teste de /carrinhos: regras de negócio de estoque e compra.

Ordem dos parâmetros (produto, cliente): o pytest desfaz as fixtures na
ordem inversa, então o carrinho do cliente é cancelado antes de o produto
ser excluído.
"""
import pytest

pytestmark = pytest.mark.api


def _estoque(api, produto_id: str) -> int:
    return api.buscar_produto(produto_id).json()["quantidade"]


def test_ct_api_18_criar_carrinho_reduz_estoque(api, produto, cliente):
    resposta = api.criar_carrinho(
        [{"idProduto": produto["_id"], "quantidade": 3}], cliente["token"]
    )

    assert resposta.status == 201
    assert resposta.json()["message"] == "Cadastro realizado com sucesso"
    assert _estoque(api, produto["_id"]) == produto["quantidade"] - 3

    carrinho = api.buscar_carrinho(resposta.json()["_id"]).json()
    assert carrinho["quantidadeTotal"] == 3
    assert carrinho["precoTotal"] == produto["preco"] * 3


def test_ct_api_19_cancelar_compra_devolve_estoque(api, produto, cliente):
    api.criar_carrinho([{"idProduto": produto["_id"], "quantidade": 4}], cliente["token"])

    resposta = api.cancelar_compra(cliente["token"])

    assert resposta.status == 200
    assert "Estoque dos produtos reabastecido" in resposta.json()["message"]
    assert _estoque(api, produto["_id"]) == produto["quantidade"]


def test_ct_api_20_concluir_compra_mantem_estoque_reduzido(api, produto, cliente):
    api.criar_carrinho([{"idProduto": produto["_id"], "quantidade": 2}], cliente["token"])

    resposta = api.concluir_compra(cliente["token"])

    assert resposta.status == 200
    assert resposta.json()["message"] == "Registro excluído com sucesso"
    assert _estoque(api, produto["_id"]) == produto["quantidade"] - 2


def test_ct_api_21_nao_permite_dois_carrinhos(api, produto, cliente):
    item = [{"idProduto": produto["_id"], "quantidade": 1}]
    api.criar_carrinho(item, cliente["token"])

    resposta = api.criar_carrinho(item, cliente["token"])

    assert resposta.status == 400
    assert resposta.json()["message"] == "Não é permitido ter mais de 1 carrinho"


def test_ct_api_22_quantidade_maior_que_estoque(api, produto, cliente):
    resposta = api.criar_carrinho(
        [{"idProduto": produto["_id"], "quantidade": produto["quantidade"] + 1}],
        cliente["token"],
    )

    assert resposta.status == 400
    assert resposta.json()["message"] == "Produto não possui quantidade suficiente"


def test_ct_api_23_nao_exclui_usuario_com_carrinho(api, produto, cliente):
    api.criar_carrinho([{"idProduto": produto["_id"], "quantidade": 1}], cliente["token"])

    resposta = api.excluir_usuario(cliente["_id"])

    assert resposta.status == 400
    assert resposta.json()["message"] == "Não é permitido excluir usuário com carrinho cadastrado"
