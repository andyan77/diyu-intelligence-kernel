#!/usr/bin/env python3
"""三件套之一：JSON Schema 校验。用法: validate_schema.py <instance.json> <schema.json>；exit 0=通过 1=违约。"""
import json, sys, os
from jsonschema import Draft7Validator, RefResolver

def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)

def validate(instance_path, schema_path):
    schema = load(schema_path)
    base = "file://" + os.path.abspath(os.path.dirname(schema_path)) + "/"
    resolver = RefResolver(base_uri=base, referrer=schema)
    errors = sorted(Draft7Validator(schema, resolver=resolver).iter_errors(load(instance_path)), key=lambda e: list(e.absolute_path))
    for e in errors:
        print(f"VIOLATION at /{'/'.join(map(str, e.absolute_path))}: {e.message}")
    return len(errors)

if __name__ == "__main__":
    n = validate(sys.argv[1], sys.argv[2])
    print(("SCHEMA_OK" if n == 0 else f"SCHEMA_INVALID ({n} violations)") + f" | {sys.argv[1]}")
    sys.exit(0 if n == 0 else 1)
