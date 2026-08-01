from __future__ import annotations
import argparse
from datetime import datetime
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]

p = argparse.ArgumentParser()
p.add_argument("--client", required=True)
p.add_argument("--room", required=True)
p.add_argument("--request", required=True)
args = p.parse_args()

folder = ROOT / "docs" / "clients" / args.client / "revisions"
folder.mkdir(parents=True, exist_ok=True)
existing = sorted(folder.glob("REV-*.yaml"))
number = len(existing) + 1
path = folder / f"REV-{number:04d}.yaml"

data = {
    "revision_id": f"REV-{number:04d}",
    "project_id": args.client,
    "room_id": args.room,
    "created_at": datetime.now().isoformat(),
    "requested_by": "arquiteta",
    "raw_request": args.request,
    "changes": [],
    "preserve": [],
    "new_requirements": [],
    "superseded_requirements": [],
    "conflicts": [],
    "status": "pending-analysis",
}
path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
print(path)
