def search_country(countries, keyword):
    keyword = keyword.strip().casefold()
    if not keyword:
        return []
    results = []
    for country in countries:
        text = " ".join([
            str(country.get("name", "")),
            str(country.get("official_name", "")),
            str(country.get("capital", "")),
            str(country.get("region", "")),
            " ".join(country.get("languages", []))
        ]).casefold()
        if keyword in text:
            results.append(country)
    return results