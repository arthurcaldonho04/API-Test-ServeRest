"""Validação de contrato: confere se o JSON da resposta segue o schema esperado."""
import json
from pathlib import Path

from jsonschema import validate

PASTA_SCHEMAS = Path(__file__).resolve().parent.parent / "schemas"


def validar_contrato(corpo: dict, nome_schema: str) -> None:
    schema = json.loads((PASTA_SCHEMAS / f"{nome_schema}.json").read_text(encoding="utf-8"))
    validate(instance=corpo, schema=schema)
