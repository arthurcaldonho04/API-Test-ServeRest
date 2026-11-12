"""Cliente da API ServeRest construído sobre o APIRequestContext do Playwright.

Centraliza as rotas da API para que os testes fiquem legíveis e para que
os testes web possam preparar dados (usuários, produtos) sem usar a tela.
"""
from playwright.sync_api import APIRequestContext, APIResponse


class ServeRestApi:
    def __init__(self, request: APIRequestContext):
        self.request = request

    # ---------- Login ----------
    def login(self, email: str, password: str) -> APIResponse:
        return self.request.post("/login", data={"email": email, "password": password})

    def token(self, email: str, password: str) -> str:
        resposta = self.login(email, password)
        assert resposta.status == 200, resposta.text()
        return resposta.json()["authorization"]

    # ---------- Usuários ----------
    def listar_usuarios(self, **filtros) -> APIResponse:
        return self.request.get("/usuarios", params=filtros or None)

    def criar_usuario(self, usuario: dict) -> APIResponse:
        return self.request.post("/usuarios", data=usuario)

    def buscar_usuario(self, _id: str) -> APIResponse:
        return self.request.get(f"/usuarios/{_id}")

    def editar_usuario(self, _id: str, usuario: dict) -> APIResponse:
        return self.request.put(f"/usuarios/{_id}", data=usuario)

    def excluir_usuario(self, _id: str) -> APIResponse:
        return self.request.delete(f"/usuarios/{_id}")

    # ---------- Produtos ----------
    def listar_produtos(self, **filtros) -> APIResponse:
        return self.request.get("/produtos", params=filtros or None)

    def criar_produto(self, produto: dict, token: str | None) -> APIResponse:
        headers = {"Authorization": token} if token else {}
        return self.request.post("/produtos", data=produto, headers=headers)

    def buscar_produto(self, _id: str) -> APIResponse:
        return self.request.get(f"/produtos/{_id}")

    def excluir_produto(self, _id: str, token: str) -> APIResponse:
        return self.request.delete(f"/produtos/{_id}", headers={"Authorization": token})

    # ---------- Carrinhos ----------
    def criar_carrinho(self, produtos: list[dict], token: str) -> APIResponse:
        return self.request.post(
            "/carrinhos", data={"produtos": produtos}, headers={"Authorization": token}
        )

    def buscar_carrinho(self, _id: str) -> APIResponse:
        return self.request.get(f"/carrinhos/{_id}")

    def concluir_compra(self, token: str) -> APIResponse:
        return self.request.delete("/carrinhos/concluir-compra", headers={"Authorization": token})

    def cancelar_compra(self, token: str) -> APIResponse:
        return self.request.delete("/carrinhos/cancelar-compra", headers={"Authorization": token})
