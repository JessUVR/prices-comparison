import re
import requests
from bs4 import BeautifulSoup
from datetime import date

START_URL = "https://www.oxxo.com/promociones/cerveza-vinos-y-licores"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}

# Meses básicos (incluye septiembre)
MONTHS_ES = {
    "enero":"01","febrero":"02","marzo":"03","abril":"04","mayo":"05","junio":"06",
    "julio":"07","agosto":"08","septiembre":"09","septiembre":"09",
    "octubre":"10","noviembre":"11","diciembre":"12"
}

def _first_image_url(img):
    """Toma la URL de imagen de los atributos más comunes (src, data-src, srcset)."""
    # 1) src directo
    u = (img.get("src") or "").strip()
    if u:
        return _abs_url(u)
    # 2) data-src
    u = (img.get("data-src") or "").strip()
    if u:
        return _abs_url(u)
    # 3) srcset: toma la primera URL antes del espacio
    srcset = (img.get("srcset") or img.get("data-srcset") or "").strip()
    if srcset:
        first = srcset.split(",")[0].strip().split(" ")[0]
        return _abs_url(first)
    return ""

def _abs_url(u):
    """Normaliza URLs relativas o con // al formato https absoluto."""
    if not u: return ""
    if u.startswith("//"):
        return "https:" + u
    if u.startswith("/"):
        return "https://www.oxxo.com" + u
    return u

def _pad2(n):
    """Devuelve el día con 2 dígitos (01..31)."""
    return str(n).zfill(2)

def parse_vigencia(texto):
    """
    Intenta leer 'Vigencia del 1 al 15 de septiembre de 2025' o
    'Vigencia del 17 de julio al 20 de agosto de 2025'.
    Si no puede, regresa (None, None, texto_limpio).
    """
    if not texto:
        return None, None, ""

    t = texto.lower().strip()

    # patrón 1: del 17 de julio al 20 de agosto de 2025 ...
    m = re.search(r"del\s+(\d{1,2})\s+de\s+([a-záéíóú]+)\s+al\s+(\d{1,2})\s+de\s+([a-záéíóú]+)\s+de\s+(\d{4})(.*)", t)
    if m:
        d1, mon1, d2, mon2, year, rest = m.groups()
        m1 = MONTHS_ES.get(mon1.strip(), "")
        m2 = MONTHS_ES.get(mon2.strip(), "")
        vfrom  = f"{year}-{m1}-{_pad2(d1)}" if m1 else None
        vuntil = f"{year}-{m2}-{_pad2(d2)}" if m2 else None
        notes = rest.strip(" .")
        return vfrom, vuntil, notes

    # patrón 2 (mismo mes): del 1 al 15 de septiembre de 2025 ...
    m = re.search(r"del\s+(\d{1,2})\s+al\s+(\d{1,2})\s+de\s+([a-záéíóú]+)\s+de\s+(\d{4})(.*)", t)
    if m:
        d1, d2, mon, year, rest = m.groups()
        mm = MONTHS_ES.get(mon.strip(), "")
        vfrom  = f"{year}-{mm}-{_pad2(d1)}" if mm else None
        vuntil = f"{year}-{mm}-{_pad2(d2)}" if mm else None
        notes = rest.strip(" .")
        return vfrom, vuntil, notes

    # si no matchea, deja el texto como notas
    return None, None, t

def get_promotions():
    """Devuelve lista de promos con name, image, valid_from, valid_until, notes, store."""
    try:
        r = requests.get(START_URL, headers=HEADERS, timeout=15)
    except Exception:
        return []
    if r.status_code != 200:
        return []

    soup = BeautifulSoup(r.text, "html.parser")
    boxes = soup.select("div.promotion_image")
    out = []

    for box in boxes:
        img = box.find("img")
        if not img:
            continue
        name  = (img.get("alt") or "").strip()
        image = _first_image_url(img)

        onclick = img.get("onclick", "")
        vig_text = ""
        if onclick:
            parts = onclick.split("'")
            if len(parts) >= 10:
                vig_text = parts[9].strip()

        vfrom, vuntil, notes = parse_vigencia(vig_text)

        out.append({
            "name": name,
            "image": image,
            "valid_from": vfrom,
            "valid_until": vuntil,
            "notes": notes,
            "store": "OXXO",
        })
    return out

def is_active(p, today_iso):
    """True si today está entre [valid_from, valid_until]; si faltan fechas, también pasa."""
    vf = p.get("valid_from")
    vu = p.get("valid_until")
    return (not vf or vf <= today_iso) and (not vu or today_iso <= vu)

if __name__ == "__main__":
    items = get_promotions()
    today = date.today().isoformat()
    active = [p for p in items if is_active(p, today)]

    print("Total promos:", len(items))
    print("Activas hoy:", len(active))
    print("\nEjemplos (máx 5):")
    for p in active[:5]:
        print("-")
        print("  name       :", p["name"])
        print("  image      :", p["image"])
        print("  valid_from :", p.get("valid_from"))
        print("  valid_until:", p.get("valid_until"))
        print("  notes      :", p.get("notes"))
        print("  store      :", p["store"])
