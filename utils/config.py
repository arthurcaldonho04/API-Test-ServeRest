"""Endereços da aplicação testada.

Por padrão os testes usam o ServeRest público. Para rodar contra uma
instância local, defina as variáveis de ambiente API_URL e FRONT_URL.
"""
import os

API_URL = os.getenv("API_URL", "https://serverest.dev").rstrip("/")
FRONT_URL = os.getenv("FRONT_URL", "https://front.serverest.dev").rstrip("/")
