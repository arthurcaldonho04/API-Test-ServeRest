# Testes automatizados do ServeRest com Playwright + Python

Trabalho da disciplina **Qualidade e Teste de Software**, UNESC Colatina, Sistemas de Informação, 8º período.

Integrantes: Andrey Porto Brumatti, Arthur Ronchetti Caldonho, Eduardo Bertoldi e Gustavo Santos.

A suíte tem **39 testes**: 28 de API REST e 11 de interface web (end-to-end), executados sobre o
[ServeRest](https://serverest.dev), com o front-end em [front.serverest.dev](https://front.serverest.dev).

## Estrutura

```
serverest-tests/
├── conftest.py            # fixtures: cliente de API, usuários admin/cliente, produto
├── pytest.ini             # configuração, marcadores e relatório HTML
├── requirements.txt
├── pages/                 # Page Objects (uma classe por tela)
├── schemas/               # JSON Schemas para teste de contrato
├── tests/
│   ├── api/               # login, usuários, produtos, carrinhos
│   └── web/               # login, cadastro, compras, área do administrador
├── utils/                 # configuração, massa de dados, cliente da API, contrato
└── .github/workflows/     # execução automática no GitHub Actions
```

## Como rodar (Windows, VS Code)

1. Instale o **Python 3.10 ou superior** (marque "Add Python to PATH" no instalador).
2. Abra a pasta `serverest-tests` no VS Code e abra o terminal (`Ctrl + '`).
3. Crie e ative um ambiente virtual:
   ```
   python -m venv .venv
   .venv\Scripts\activate
   ```
   No Linux/macOS: `source .venv/bin/activate`.
4. Instale as dependências e o navegador:
   ```
   pip install -r requirements.txt
   playwright install chromium
   ```
5. Execute os testes:
   ```
   pytest                 # todos os testes
   pytest -m api          # só API
   pytest -m web          # só interface
   pytest -m web --headed --slowmo 500   # mostra o navegador em câmera lenta
   ```
6. Abra o relatório gerado em `reports/relatorio.html`.

Em caso de falha, prints, vídeos e traces ficam em `test-results/`. Para ver um trace passo a passo:
`playwright show-trace test-results/<pasta-do-teste>/trace.zip`.

### Rede da empresa

Se a rede bloquear o acesso a `serverest.dev`, rode o ServeRest localmente (precisa do Node.js):

```
npx serverest@latest
```

e aponte os testes de API para ele:

```
set API_URL=http://localhost:3000        (Windows cmd)
$env:API_URL="http://localhost:3000"     (PowerShell)
pytest -m api
```

## Execução contínua

O workflow `.github/workflows/testes.yml` roda a suíte a cada push, pull request, manualmente e em dias
úteis às 08:00. Os relatórios ficam disponíveis como artefato da execução no GitHub.
