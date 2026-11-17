def display_countries(countries, title="DAFTAR NEGARA"):
    print(f"\\n{'=' * 78}\\n{title.upper()} ({len(countries)} data)\\n{'=' * 78}")
    if not countries:
        print("Tidak ada data.")
        return
    print(f"{'No.':<5}{'Nama negara':<30}{'Ibu kota':<22}{'Populasi':>18}")
    print("-" * 78)
    for i, c in enumerate(countries, 1):
        print(f"{i:<5}{c.get('name','N/A')[:28]:<30}{c.get('capital','N/A')[:20]:<22}{c.get('population',0):>18,}")

def show_country_detail(c):
    print(f"\\nDETAIL NEGARA: {c.get('name', 'N/A').upper()}")
    print("=" * 55)
    fields = [
        ("Nama resmi", "official_name"), ("Ibu kota", "capital"),
        ("Wilayah", "region"), ("Subwilayah", "subregion"),
        ("Populasi", "population"), ("Luas (km2)", "area"),
        ("Mata uang", "currencies"), ("Bahasa", "languages"),
        ("Kode ISO-2", "cca2"), ("Kode ISO-3", "cca3"),
        ("Negara perbatasan", "borders")
    ]
    for label, key in fields:
        value = c.get(key, "N/A")
        if isinstance(value, list):
            value = ", ".join(map(str, value)) or "N/A"
        if key == "population":
            value = f"{value:,}"
        elif key == "area":
            value = f"{value:,.2f}"
        print(f"{label:<22}: {value}")
    print(f"{'Koordinat':<22}: {c.get('latitude')}, {c.get('longitude')}")

def compare_countries(countries, first_name, second_name):
    def find(name):
        return next((c for c in countries if c["name"].casefold() == name.casefold()), None)
    a, b = find(first_name), find(second_name)
    if not a or not b:
        print("Negara tidak ditemukan. Gunakan nama persis seperti pada dataset.")
        return
    print(f"\\nPERBANDINGAN: {a['name']} vs {b['name']}")
    print("-" * 70)
    for label, key in [("Ibu kota", "capital"), ("Wilayah", "region"),
                       ("Populasi", "population"), ("Luas km2", "area")]:
        x, y = a.get(key, "N/A"), b.get(key, "N/A")
        if key in ("population", "area"):
            x, y = f"{x:,}", f"{y:,}"
        print(f"{label:<16} | {a['name']}: {x} | {b['name']}: {y}")