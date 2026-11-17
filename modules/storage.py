
import json
from pathlib import Path
from countryinfo import CountryInfo

DATA_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "countries.json"
)

def normalize_country(raw, fallback_name="Unknown"):
    """Menyeragamkan format data negara."""

    iso = raw.get("ISO", {})
    if not isinstance(iso, dict):
        iso = {}

    name_data = raw.get("name", {})

    if isinstance(name_data, dict):
        name = name_data.get("common", fallback_name)
        official = name_data.get("official", name)
    else:
        name = str(name_data or fallback_name)
        official = str(raw.get("nativeName") or name)

    # Mata uang
    currencies = raw.get("currencies", [])

    if isinstance(currencies, dict):
        currencies = [
            f"{info.get('name', code)} ({code})"
            if isinstance(info, dict) else str(code)
            for code, info in currencies.items()
        ]
    elif not isinstance(currencies, list):
        currencies = [str(currencies)] if currencies else []

    # Bahasa
    languages = raw.get("languages", [])

    if isinstance(languages, dict):
        languages = list(languages.values())
    elif not isinstance(languages, list):
        languages = []

    # Ibu kota
    capital = raw.get("capital", "N/A")
    if isinstance(capital, list):
        capital = capital[0] if capital else "N/A"

    # Kode ISO
    cca2 = raw.get("cca2") or iso.get("alpha2", "")
    cca3 = raw.get("cca3") or iso.get("alpha3", "")

    # Koordinat
    latlng = raw.get("latlng") or [None, None]

    return {
        "name": name,
        "official_name": official,
        "capital": capital or "N/A",
        "region": raw.get("region", "Unknown"),
        "subregion": raw.get("subregion", "Unknown"),
        "population": int(raw.get("population") or 0),
        "area": float(raw.get("area") or 0),
        "currencies": currencies,
        "languages": languages,
        "borders": raw.get("borders") or [],
        "cca2": cca2,
        "cca3": cca3,
        "latitude": latlng[0] if len(latlng) > 0 else None,
        "longitude": latlng[1] if len(latlng) > 1 else None,
    }


def initialize_dataset():
    """Mengambil dataset seluruh negara dari CountryInfo."""

    try:
        # Gunakan class method, bukan CountryInfo()
        raw_data = CountryInfo.all()

        if not isinstance(raw_data, dict) or not raw_data:
            print("Dataset CountryInfo kosong.")
            return []

        countries = []

        for key, raw in raw_data.items():

            if not isinstance(raw, dict):
                continue

            country = normalize_country(
                raw,
                str(key).replace("_", " ").title()
            )

            countries.append(country)

        # Menghilangkan duplikasi
        unique_countries = {}

        for country in countries:
            identifier = country["cca3"] or country["name"]
            unique_countries[identifier] = country

        result = list(unique_countries.values())

        # Urutkan berdasarkan nama negara
        result.sort(key=lambda x: x["name"].casefold())

        print(f"Berhasil mengambil {len(result)} negara.")

        return result

    except Exception as exc:
        print(f"Kesalahan saat mengambil dataset: {exc}")
        return []


def load_countries():
    """Membaca dataset dari JSON."""

    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        return data if isinstance(data, list) else []

    except (OSError, json.JSONDecodeError) as exc:
        print(f"Gagal membaca JSON: {exc}")
        return []


def save_countries(countries):
    """Menyimpan dataset ke JSON."""

    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    temp_file = DATA_FILE.with_suffix(".tmp")

    with temp_file.open("w", encoding="utf-8") as file:
        json.dump(
            countries,
            file,
            ensure_ascii=False,
            indent=4
        )

    temp_file.replace(DATA_FILE)

    print(f"Dataset berhasil disimpan: {DATA_FILE}")
