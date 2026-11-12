"""Geração de massa de dados única para cada teste.

Cada execução cria usuários e produtos novos, evitando conflito com
dados de outras pessoas no ServeRest público.
"""
import uuid

from faker import Faker

fake = Faker("pt_BR")


def _sufixo() -> str:
    return uuid.uuid4().hex[:8]


def novo_usuario(administrador: bool = False) -> dict:
    return {
        "nome": fake.name(),
        "email": f"qa_{_sufixo()}@teste.com.br",
        "password": "Senha@123",
        "administrador": "true" if administrador else "false",
    }


def novo_produto(quantidade: int = 10) -> dict:
    return {
        "nome": f"Produto QA {_sufixo()}",
        "preco": fake.random_int(min=10, max=500),
        "descricao": "Produto criado por teste automatizado",
        "quantidade": quantidade,
    }
