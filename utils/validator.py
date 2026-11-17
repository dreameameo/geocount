def ask_non_empty(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Inputan tidak boleh kosong.")