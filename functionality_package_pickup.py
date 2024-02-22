import json


def package_pickup():
    package_number = input("Proszę wpisać numer swojej paczki: ")
    searching_package_in_file(package_number)


def searching_package_in_file(package_number):
    with open("parcel_list.json", "r") as f:
        parcel_dict = json.load(f)

        package = parcel_dict.pop(package_number, None)
        if package:
            with open("parcel_list.json", "w") as plik_zapis:
                json.dump(
                    parcel_dict,
                    plik_zapis,
                    sort_keys=True,
                    indent=4,
                    separators=(",", ": "),
                    ensure_ascii=False,
                )
                print("\nPaczka gotowa do odbioru, wyciągnij paczkę z Paczkomatu")
        else:
            print(
                f"\nNiestety w systemie nie odnajdujemy paczki o numerze {package_number}"
            )
