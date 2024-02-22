import json


def package_pickup():
    package_number = input("Proszę wpisać numer swojej paczki: ")
    searching_package_in_file(package_number)


def searching_package_in_file(package_number):
    with open("parcel_list.json", "r") as f:
        parcel_dict = json.load(f)

        search_key = package_number

        if search_key in parcel_dict:
            print("Paczka gotowa do odbioru, wyciągnij paczkę z Paczkomatu")
            del parcel_dict[search_key]  # Usunięcie klucza

            with open("parcel_list.json", "w") as plik_zapis:
                json.dump(
                    parcel_dict,
                    plik_zapis,
                    sort_keys=True,
                    indent=4,
                    separators=(",", ": "),
                    ensure_ascii=False,
                )

        else:
            print(f"Niestety w systemie nie odnajdujemy paczki o numerze {search_key}")
