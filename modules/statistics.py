def show_statistics(countries):
    if not countries:
        print("Dataset kosong.")
        return
    total_population = sum(c.get("population", 0) for c in countries)
    total_area = sum(c.get("area", 0) for c in countries)
    region_counts = {}
    for c in countries:
        region = c.get("region", "Unknown")
        region_counts[region] = region_counts.get(region, 0) + 1
    highest = max(countries, key=lambda c: c.get("population", 0))
    populated = [c for c in countries if c.get("population", 0) > 0]
    lowest = min(populated, key=lambda c: c["population"]) if populated else None

    print("\\nSTATISTIK DATASET")
    print("=" * 45)
    print(f"Jumlah entri negara : {len(countries)}")
    print(f"Total populasi      : {total_population:,}")
    print(f"Total luas wilayah  : {total_area:,.2f} km2")
    print(f"Populasi tertinggi  : {highest['name']} ({highest['population']:,})")
    if lowest:
        print(f"Populasi terendah   : {lowest['name']} ({lowest['population']:,})")
    print("\nJumlah negara per wilayah:")
    for region, count in sorted(region_counts.items()):
        print(f"- {region}: {count}")