"""Descarga el estado público de Microsoft 365 y lo guarda en data/microsoft.json.

La API de status.cloud.microsoft no permite peticiones desde el navegador (sin CORS),
por eso este script corre en GitHub Actions y deja el resultado como archivo estático.
"""
import datetime
import html
import json
import pathlib
import re
import urllib.request

BASE = "https://status.cloud.microsoft/api/posts/"
OUT = pathlib.Path(__file__).resolve().parent.parent / "data" / "microsoft.json"


def get(workload):
    req = urllib.request.Request(BASE + workload, headers={"User-Agent": "estado-servicios"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def clean(text):
    text = html.unescape(re.sub(r"<[^>]+>", " ", text or ""))
    return re.sub(r"\s+", " ", text).strip()[:500]


def main():
    consumer = [
        {
            "name": p["ServiceDisplayName"],
            "status": p["Status"],
            "title": clean(p.get("Title")),
            "message": clean(p.get("Message")),
        }
        for p in get("m365Consumer")
    ]
    admin = get("mac")
    # Este aviso solo se publica cuando hay un incidente grave en Microsoft 365 empresarial.
    admin_incident = None
    if admin.get("Title"):
        admin_incident = {
            "status": admin.get("Status"),
            "title": clean(admin.get("Title")),
            "message": clean(admin.get("Message")),
            "updated": admin.get("LastUpdatedTime"),
        }

    # Hora redondeada: así solo se hace commit una vez por hora o cuando cambia un estado.
    checked = datetime.datetime.now(datetime.timezone.utc).replace(second=0, microsecond=0)
    data = {"checked": checked.isoformat(), "consumer": consumer, "admin_incident": admin_incident}
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
