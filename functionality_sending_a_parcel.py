import json

def get_package_dimensions():
    print("\nProszę o wprowadzenie wymiarów przesyłki")
    wt = float(input("Waga w kg :"))
    dpt = float(input("Głębokość w cm :"))
    ht = float(input("Wysokość w cm :"))
    wd = float(input("szerokość w cm :"))
    return [wt, dpt, ht, wd]

def dimensions_validation(wt, dpt, ht, wd):
    if wt > 20:
        print(f"\n Przekoroczono makymalną wagę paczki o {round((wt - 20), 2)}kg\n")
        return True
    if wd > 40:
        print(f"\n Przekoroczono makymalny rozmiar szerokości paczki o {round((wd - 40), 2)}cm\n")
        return True
    if ht > 40:
        print(f"\n Przekoroczono makymalny rozmiar wysokości paczki o {round((ht - 40), 2)}cm\n")
        return True
    if dpt > 60:
        print(f"\n Przekoroczono makymalny rozmiar głebokości paczki o {round((dpt - 60), 2)}cm\n")
        return True


def dm_ver_loop(chosen_option):
    dm_list = get_package_dimensions()
    if dimensions_validation(dm_list[0], dm_list[1], dm_list[2], dm_list[3]):
        dm_ver_loop(chosen_option)

def selecting_paczkomat_ver_loop():
    print("\nWybór opcji\n1 - Wybór urządzenia\n2 - Podaj listę urządzeń")
    chose_paczkomat_option = int(input("proszę o wskazanie numeru opcji: "))
    if chose_paczkomat_option != 1 and chose_paczkomat_option != 2 and chose_paczkomat_option != 3:
        print("\nBłędny wybór\nProszę o wybranie numeru opcji ze wskazanej listy\n")
        selecting_paczkomat_ver_loop()
    else:
        return chose_paczkomat_option

        
def sending_method():
    print("\nWybór metody wysyłki\n1 - wysyłka pod wskazany adres\n2 - wysyłka do Paczkomatu")
    chosen_method_option = int(input("proszę o wskazanie numeru opcji: "))
    
    if chosen_method_option == 1:
        package_revicer = input("\nProszę podać imię i nazwisko odbiorcy :").lower
        deliv_town = input("Proszę podać miasto docelowe :").lower
        deliv_street = input("Proszę podać nazwę ulicy :").lower
        deliv_building_number = input("Proszę podać numer budynku :")
        deliv_apart_number = input("Proszę podać numer lokalu jeżeli występuje :")

    elif chosen_method_option == 2:
        with open('machines_list.json', 'r') as f:
            machines_dict = json.load(f)
        while True:
            chose_paczkomat_option = selecting_paczkomat_ver_loop()

            if chose_paczkomat_option == 1:
                sup_list = []
                given_machine_id = input("\nwprowadź numer urządzenia :")

                for dct in machines_dict["paczkomaty"]:
                    if dct["id"] == int(given_machine_id):
                        print(f"\nWybrany Paczkomat:\nNumer urządzenia - {dct["id"]}\n Adres: {dct["miasto"]}, ul.{dct["ulica"]} {dct["numer"]}")
                        return False
                    else:
                        sup_list.append(1)
                if len(sup_list) > 0:
                    print("\nWskazany numer urządzenia nie istnieje")


            elif chose_paczkomat_option == 2:
                for dct in machines_dict["paczkomaty"]:
                    print(f"\nNumer urządzenia - {dct["id"]}\n Adres: {dct["miasto"]}, ul.{dct["ulica"]} {dct["numer"]}")

    else:
        print("\nBłędny wybór\nProszę o wybranie numeru opcji ze wskazanej listy\n")
        sending_method()



