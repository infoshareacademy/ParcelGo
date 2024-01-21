import json


def wybierz_metode_dostarczenia():
    print("\nMetody dostarczenia:")
    print("1. Dostarczenie pod wskazany adres przez kuriera")
    print("2. Dostawa do wybranego paczkomatu")

    wybor = input("Wybierz numer metody dostarczenia (1 lub 2): ")

    if wybor == "1":
        package_reciver = input("\nProszę podać imię i nazwisko odbiorcy :")
        deliv_town = input("Proszę podać miasto docelowe :")
        deliv_street = input("Podaj ulicę: ")
        deliv_number = input("Podaj numer budynku: ")
        return {"reciver":package_reciver, "town":deliv_town, "street":deliv_street, "number": deliv_number}

    elif wybor == "2":
        chosen_locker = send_to_locker()
        return chosen_locker
    else:
        print("\nNieprawidłowy wybór metody dostarczenia\nProszę o wybranie opcji ze wskazanej listy.")
        wybierz_metode_dostarczenia()


def selecting_locker_ver_loop():
    print("\nWybór opcji\n1 - Wybór urządzenia\n2 - Podaj listę urządzeń")
    chose_locker_option = input("proszę o wskazanie numeru opcji: ")
    if chose_locker_option != "1" and chose_locker_option != "2":
        print("\nBłędny wybór\nProszę o wybranie numeru opcji ze wskazanej listy\n")
        send_to_locker()
    else:
        return chose_locker_option


def send_to_locker():
    with open('machines_list.json', 'r') as f:
        machines_dict = json.load(f)

    chose_paczkomat_option = selecting_locker_ver_loop()

    if chose_paczkomat_option == "1":

        given_machine_id = input("\nwprowadź numer urządzenia :")
        chosen_machine = machines_dict.get(given_machine_id)
        if chosen_machine:
            print(
                f"\nWybrany Paczkomat:\nNumer urządzenia - {given_machine_id}\nAdres: {chosen_machine["miasto"]}, ul.{chosen_machine["ulica"]} {chosen_machine["numer"]}")
            return {given_machine_id:chosen_machine}
        else:
            print("\nWskazany numer urządzenia nie istnieje")
            send_to_locker()

    elif chose_paczkomat_option == "2":
        for machine in machines_dict:
            print(
                f"\nNumer urządzenia - {machine}\n Adres: {machines_dict.get(machine)["miasto"]}, "
                f"ul.{machines_dict.get(machine)["ulica"]} {machines_dict.get(machine)["numer"]}")
        send_to_locker()
