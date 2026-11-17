from modules.storage import load_countries, save_countries, initialize_dataset
from modules.country import display_countries, show_country_detail, compare_countries
from modules.search import search_country
from modules.sorting import sort_countries
from modules.statistics import show_statistics
from utils.formatter import print_header, print_message, pause
from utils.validator import ask_non_empty

def main():
    countries = load_countries()
    if not countries:
        print_message("Dataset lokal belum ada. Menginisialisasi dataset...", "warning")
        countries = initialize_dataset()
        if not countries:
            print_message("Dataset gagal dibuat. Periksa instalasi CountryInfo.", "error")
            return
        save_countries(countries)
        print_message(f"{len(countries)} negara disimpan ke data/countries.json", "success")

    while True:
        print_header("GEODATA EXPLORER")
        print("1. Tampilkan seluruh negara")
        print("2. Cari negara")
        print("3. Detail negara")
        print("4. Urutkan negara")
        print("5. Filter berdasarkan wilayah/benua")
        print("6. Bandingkan dua negara")
        print("7. Statistik dataset")
        print("8. Perbarui dataset")
        print("9. Keluar")
        choice = input("\nPilih [1-9]: ").strip()

        if choice == "1":
            display_countries(countries)
        elif choice == "2":
            keyword = ask_non_empty("Nama/kata kunci: ")
            display_countries(search_country(countries, keyword), f"Hasil pencarian: {keyword}")
        elif choice == "3":
            keyword = ask_non_empty("Nama negara: ")
            found = search_country(countries, keyword)
            if found:
                exact = next((c for c in found if c["name"].casefold() == keyword.casefold()), found[0])
                show_country_detail(exact)
            else:
                print_message("\nNegara tidak ditemukan.", "warning")
        elif choice == "4":
            print("1. Nama A-Z\\n2. Populasi terbesar\\n3. Luas wilayah terbesar")
            option = input("Pilih: ").strip()
            keys = {"1": "name", "2": "population", "3": "area"}
            if option in keys:
                display_countries(sort_countries(countries, keys[option]), "Hasil pengurutan")
            else:
                print_message("Pilihan tidak valid.", "error")
        elif choice == "5":
            regions = sorted({c.get("region", "Unknown") for c in countries})
            print("Wilayah tersedia:", ", ".join(regions))
            region = ask_non_empty("Masukkan wilayah: ")
            result = [c for c in countries if c.get("region", "").casefold() == region.casefold()]
            display_countries(result, f"Negara di {region}")
        elif choice == "6":
            compare_countries(countries, ask_non_empty("Negara pertama: "), ask_non_empty("Negara kedua: "))
        elif choice == "7":
            show_statistics(countries)
        elif choice == "8":
            if input("Ambil ulang dataset? [y/N]: ").strip().lower() == "y":
                updated = initialize_dataset()
                if updated:
                    countries = updated
                    save_countries(countries)
                    print_message("Dataset berhasil diperbarui.", "success")
                else:
                    print_message("Pembaruan gagal; data lama dipertahankan.", "error")
        elif choice == "9":
            print_message("Terima kasih!", "success")
            break
        else:
            print_message("Pilihan tidak valid.", "error")
        pause()

if __name__ == "__main__":
    main()