def sort_countries(countries, key):
    result = countries.copy()
    for i in range(len(result)):
        selected = i
        for j in range(i + 1, len(result)):
            current, best = result[j].get(key), result[selected].get(key)
            if key == "name":
                condition = str(current).casefold() < str(best).casefold()
            else:
                condition = (current or 0) > (best or 0)
            if condition:
                selected = j
        result[i], result[selected] = result[selected], result[i]
    return result