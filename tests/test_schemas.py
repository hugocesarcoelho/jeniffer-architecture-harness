import json
from pathlib import Path
import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]

def test_template_project_schema():
    data = yaml.safe_load((ROOT / "docs/clients/_template/brief/project.yaml").read_text(encoding="utf-8"))
    schema = json.loads((ROOT / "schemas/project.schema.json").read_text(encoding="utf-8"))
    assert list(Draft202012Validator(schema).iter_errors(data)) == []

def test_template_requirements_schema():
    data = yaml.safe_load((ROOT / "docs/clients/_template/brief/requirements.yaml").read_text(encoding="utf-8"))
    schema = json.loads((ROOT / "schemas/requirements.schema.json").read_text(encoding="utf-8"))
    assert list(Draft202012Validator(schema).iter_errors(data)) == []
