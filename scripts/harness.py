from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import fitz
import requests
import yaml
from dotenv import load_dotenv
from jsonschema import Draft202012Validator
from PIL import Image, ImageDraw
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
CLIENTS = DOCS / "clients"
KB_RAW = DOCS / "knowledge-base" / "raw-pdfs"
KB_EXTRACTED = DOCS / "knowledge-base" / "extracted"
SCHEMAS = ROOT / "schemas"


def client_output(client_id: str) -> Path:
    """Return the project-local output directory."""
    return CLIENTS / client_id / "output"


load_dotenv(ROOT / ".env")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def write_yaml(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def cmd_ingest_library(_: argparse.Namespace) -> None:
    KB_RAW.mkdir(parents=True, exist_ok=True)
    KB_EXTRACTED.mkdir(parents=True, exist_ok=True)
    pdfs = sorted(KB_RAW.rglob("*.pdf"))
    if not pdfs:
        print(f"Nenhum PDF encontrado em {KB_RAW}")
        return

    catalog = []
    for pdf in pdfs:
        rel_parts = pdf.relative_to(KB_RAW).parent.parts
        if len(rel_parts) >= 2:
            project_category = rel_parts[0]
            client_project = "/".join(rel_parts[1:])
        elif len(rel_parts) == 1:
            project_category = None
            client_project = rel_parts[0]
        else:
            project_category = None
            client_project = None
        doc_id = slug("-".join(p for p in (project_category, client_project, pdf.stem) if p))
        dest = KB_EXTRACTED / doc_id
        pages_dir = dest / "pages"
        images_dir = dest / "embedded-images"
        pages_dir.mkdir(parents=True, exist_ok=True)
        images_dir.mkdir(parents=True, exist_ok=True)

        doc = fitz.open(pdf)
        page_records = []
        full_text = []
        image_count = 0

        for idx, page in enumerate(doc):
            text = page.get_text("text")
            full_text.append(f"\n\n--- PAGE {idx + 1} ---\n{text}")
            pix = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5), alpha=False)
            page_img = pages_dir / f"page-{idx + 1:04d}.jpg"
            pix.save(page_img)

            embedded = []
            for img_idx, img in enumerate(page.get_images(full=True), start=1):
                xref = img[0]
                extracted = doc.extract_image(xref)
                ext = extracted["ext"]
                out = images_dir / f"page-{idx + 1:04d}-img-{img_idx:03d}.{ext}"
                out.write_bytes(extracted["image"])
                embedded.append(str(out.relative_to(ROOT)))
                image_count += 1

            page_records.append({
                "page": idx + 1,
                "page_image": str(page_img.relative_to(ROOT)),
                "embedded_images": embedded,
                "text_chars": len(text),
            })

        (dest / "document.txt").write_text("".join(full_text), encoding="utf-8")
        manifest = {
            "document_id": doc_id,
            "project_category": project_category,
            "client_project": client_project,
            "source": str(pdf.relative_to(ROOT)),
            "sha256": sha256(pdf),
            "pages": len(doc),
            "embedded_image_count": image_count,
            "ingested_at": now_iso(),
            "page_records": page_records,
        }
        write_json(dest / "manifest.json", manifest)
        catalog.append(manifest)
        label_parts = [p for p in (project_category, client_project) if p]
        label = "/".join(label_parts + [pdf.name]) if label_parts else pdf.name
        print(f"Extraído: {label} ({len(doc)} páginas)")

    write_json(KB_EXTRACTED / "catalog.json", {"documents": catalog})
    print(f"Catálogo criado em {KB_EXTRACTED / 'catalog.json'}")


def slug(text: str) -> str:
    return "".join(c.lower() if c.isalnum() else "-" for c in text).strip("-")


def cmd_new_client(args: argparse.Namespace) -> None:
    client_id = args.id
    target = CLIENTS / client_id
    if target.exists():
        raise SystemExit(f"Cliente já existe: {target}")
    template = CLIENTS / "_template"
    shutil.copytree(template, target)
    project_path = target / "brief" / "project.yaml"
    project = read_yaml(project_path)
    project["project_id"] = client_id
    project["client_name"] = args.name
    write_yaml(project_path, project)
    (target / "revisions").mkdir(exist_ok=True)
    print(f"Projeto criado: {target}")


def validate_schema(data_path: Path, schema_path: Path) -> list[str]:
    data = read_yaml(data_path)
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    return [
        f"{'/'.join(str(x) for x in e.absolute_path) or '<root>'}: {e.message}"
        for e in sorted(validator.iter_errors(data), key=lambda x: list(x.path))
    ]


def inventory_client(client_id: str) -> dict[str, Any]:
    base = CLIENTS / client_id
    records = []
    for path in sorted(base.rglob("*")):
        if path.is_file():
            records.append({
                "path": str(path.relative_to(ROOT)),
                "size_bytes": path.stat().st_size,
                "sha256": sha256(path),
                "extension": path.suffix.lower(),
            })
    return {"project_id": client_id, "generated_at": now_iso(), "files": records}


def cmd_validate(args: argparse.Namespace) -> None:
    base = CLIENTS / args.client
    if not base.exists():
        raise SystemExit(f"Projeto não encontrado: {args.client}")

    errors = []
    errors += validate_schema(base / "brief" / "project.yaml", SCHEMAS / "project.schema.json")
    errors += validate_schema(base / "brief" / "requirements.yaml", SCHEMAS / "requirements.schema.json")

    inventory = inventory_client(args.client)
    out = client_output(args.client) / "analysis"
    write_json(out / "input-inventory.json", inventory)

    report = ["# Relatório de validação", "", f"Projeto: `{args.client}`", ""]
    if errors:
        report += ["## Erros bloqueantes", ""] + [f"- {e}" for e in errors]
    else:
        report += ["## Resultado", "", "Estrutura e schemas válidos."]

    photos_root = base / "inputs" / "property-photos"
    room_photo_counts = {}
    if photos_root.exists():
        for room in photos_root.iterdir():
            if room.is_dir():
                room_photo_counts[room.name] = len([p for p in room.rglob("*") if p.is_file()])
    report += ["", "## Fotos por ambiente", ""]
    if room_photo_counts:
        report += [f"- {room}: {count}" for room, count in room_photo_counts.items()]
    else:
        report += ["- Nenhuma pasta de foto por ambiente encontrada."]

    (out / "validation-report.md").write_text("\n".join(report), encoding="utf-8")
    print("\n".join(report))
    if errors:
        sys.exit(2)


def prompt_for_room(project: dict, requirements: list[dict], room: dict, revision: int) -> dict:
    room_id = room["room_id"]
    reqs = [r for r in requirements if r["room_id"] in (room_id, "global")]
    positives = [r["statement"] for r in reqs if r["status"] in ("confirmed", "inferred")]
    negatives = [
        "não alterar a geometria confirmada do ambiente",
        "não inventar portas, janelas, pilares ou pontos técnicos",
        "não inserir textos, marcas d'água ou pessoas",
        "não apresentar soluções estruturalmente impossíveis",
    ]
    return {
        "project_id": project["project_id"],
        "room_id": room_id,
        "room_name": room["name"],
        "revision": revision,
        "generated_at": now_iso(),
        "requirements": [r["id"] for r in reqs],
        "positive_prompt": (
            f"Renderização arquitetônica residencial fotorrealista do ambiente {room['name']}. "
            + " ".join(positives)
            + " Manter coerência física, escala plausível, materiais realistas, iluminação natural "
              "e artificial tecnicamente plausível. Seguir o Design DNA aprovado da arquiteta."
        ),
        "negative_prompt": "; ".join(negatives),
        "preserve": [
            "aberturas confirmadas",
            "elementos estruturais confirmados",
            "pontos técnicos identificados",
        ],
        "reference_paths": [],
        "status": "draft",
    }


def cmd_build_prompts(args: argparse.Namespace) -> None:
    base = CLIENTS / args.client
    project = read_yaml(base / "brief" / "project.yaml")
    req_data = read_yaml(base / "brief" / "requirements.yaml")
    prompts_dir = client_output(args.client) / "prompts"
    prompts_dir.mkdir(parents=True, exist_ok=True)

    index = []
    for room in project["rooms"]:
        p = prompt_for_room(project, req_data["requirements"], room, revision=1)
        path = prompts_dir / f"{room['room_id']}-r001.json"
        write_json(path, p)
        index.append(str(path.relative_to(ROOT)))
    write_json(prompts_dir / "index.json", {"prompts": index})
    print(f"{len(index)} prompts criados em {prompts_dir}")


class ImageProvider:
    def generate(self, prompt: dict, output_path: Path) -> None:
        raise NotImplementedError


class MockProvider(ImageProvider):
    def generate(self, prompt: dict, output_path: Path) -> None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        img = Image.new("RGB", (1536, 1024), "white")
        draw = ImageDraw.Draw(img)
        text = (
            "MOCK — SUBSTITUIR POR PROVEDOR DE IMAGEM\n\n"
            f"Projeto: {prompt['project_id']}\n"
            f"Ambiente: {prompt['room_name']}\n"
            f"Revisão: {prompt['revision']}\n\n"
            f"{prompt['positive_prompt'][:800]}"
        )
        draw.multiline_text((80, 80), text, fill="black", spacing=12)
        img.save(output_path, quality=92)


class RestProvider(ImageProvider):
    def __init__(self) -> None:
        self.url = os.environ.get("IMAGE_API_URL", "")
        self.key = os.environ.get("IMAGE_API_KEY", "")
        self.model = os.environ.get("IMAGE_MODEL", "")
        if not self.url:
            raise RuntimeError("IMAGE_API_URL não configurada.")

    def generate(self, prompt: dict, output_path: Path) -> None:
        headers = {"Content-Type": "application/json"}
        if self.key:
            headers["Authorization"] = f"Bearer {self.key}"
        payload = {
            "model": self.model,
            "prompt": prompt["positive_prompt"],
            "negative_prompt": prompt["negative_prompt"],
            "width": 1536,
            "height": 1024,
            "metadata": {
                "project_id": prompt["project_id"],
                "room_id": prompt["room_id"],
                "revision": prompt["revision"],
            },
        }
        response = requests.post(self.url, headers=headers, json=payload, timeout=300)
        response.raise_for_status()
        content_type = response.headers.get("content-type", "")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        if content_type.startswith("image/"):
            output_path.write_bytes(response.content)
            return
        data = response.json()
        image_url = data.get("image_url") or data.get("url")
        if not image_url:
            raise RuntimeError("API não retornou imagem nem image_url.")
        img_response = requests.get(image_url, timeout=300)
        img_response.raise_for_status()
        output_path.write_bytes(img_response.content)


def provider() -> ImageProvider:
    name = os.environ.get("IMAGE_PROVIDER", "mock").lower()
    if name == "mock":
        return MockProvider()
    if name == "rest":
        return RestProvider()
    raise RuntimeError(f"Provider desconhecido: {name}")


def cmd_render(args: argparse.Namespace) -> None:
    prompts_dir = client_output(args.client) / "prompts"
    paths = sorted(prompts_dir.glob("*-r*.json"))
    if not paths:
        raise SystemExit("Nenhum prompt encontrado. Execute build-prompts.")
    engine = provider()
    manifest = []
    for path in paths:
        prompt = json.loads(path.read_text(encoding="utf-8"))
        rev = f"r{int(prompt['revision']):03d}"
        room_dir = client_output(args.client) / "concepts" / prompt["room_id"] / rev
        image_path = room_dir / "view-01.jpg"
        engine.generate(prompt, image_path)
        manifest.append({
            "prompt": str(path.relative_to(ROOT)),
            "image": str(image_path.relative_to(ROOT)),
            "sha256": sha256(image_path),
            "requirements": prompt["requirements"],
        })
        print(f"Gerado: {image_path}")
    write_json(client_output(args.client) / "concepts" / "manifest.json", {"images": manifest})


def cmd_detailing(args: argparse.Namespace) -> None:
    base = CLIENTS / args.client
    project = read_yaml(base / "brief" / "project.yaml")
    reqs = read_yaml(base / "brief" / "requirements.yaml")["requirements"]
    out = client_output(args.client) / "detailing"
    out.mkdir(parents=True, exist_ok=True)

    md = [
        f"# Detalhamento preliminar — {project['client_name']}",
        "",
        "> Documento preliminar. Requer validação e complementação profissional.",
        "",
    ]
    for room in project["rooms"]:
        md += [f"## {room['name']}", ""]
        room_reqs = [r for r in reqs if r["room_id"] == room["room_id"]]
        md += [f"- [{r['id']}] {r['statement']} — **{r['status']}**" for r in room_reqs]
        md += ["", "### Pendências técnicas", "", "- Conferir medidas em levantamento.", "- Validar instalações e normas aplicáveis.", ""]

    md_path = out / "detailing-preliminary.md"
    md_path.write_text("\n".join(md), encoding="utf-8")

    pdf_path = out / "detailing-preliminary.pdf"
    c = canvas.Canvas(str(pdf_path), pagesize=A4)
    width, height = A4
    y = height - 50
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, f"Detalhamento preliminar — {project['client_name']}")
    y -= 30
    c.setFont("Helvetica", 9)
    for line in md:
        clean = line.replace("#", "").replace("**", "").replace("`", "")
        for chunk_start in range(0, len(clean), 105):
            chunk = clean[chunk_start:chunk_start + 105]
            if y < 50:
                c.showPage()
                c.setFont("Helvetica", 9)
                y = height - 50
            c.drawString(50, y, chunk)
            y -= 13
    c.save()
    print(f"Gerados: {md_path} e {pdf_path}")


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Jeniffer Architecture Harness")
    sub = p.add_subparsers(dest="command", required=True)

    s = sub.add_parser("ingest-library")
    s.set_defaults(func=cmd_ingest_library)

    s = sub.add_parser("new-client")
    s.add_argument("--id", required=True)
    s.add_argument("--name", required=True)
    s.set_defaults(func=cmd_new_client)

    s = sub.add_parser("validate")
    s.add_argument("--client", required=True)
    s.set_defaults(func=cmd_validate)

    s = sub.add_parser("build-prompts")
    s.add_argument("--client", required=True)
    s.set_defaults(func=cmd_build_prompts)

    s = sub.add_parser("render")
    s.add_argument("--client", required=True)
    s.set_defaults(func=cmd_render)

    s = sub.add_parser("detailing")
    s.add_argument("--client", required=True)
    s.set_defaults(func=cmd_detailing)
    return p


if __name__ == "__main__":
    args = parser().parse_args()
    args.func(args)
