from functionality_sending_a_parcel import dm_ver_loop, sending_method
from ascii import logo
def main_menu():
    while True:
        print(f"{logo}\nMenu Główne\n1 - Nadaj paczkę\n2 - Odbierz paczkę\n3 - Status paczki\n4 - Wyjście z aplikacji")
        try:
            chosen_option = int(input("proszę o wskazanie numeru opcji: "))
        except ValueError:
            print("\nBłędny wybór\nProszę o wybranie numeru opcji ze wskazanej listy\n")
            continue

        if chosen_option == 1:
            dm_ver_loop(chosen_option)
            sending_method()

        elif chosen_option == 2:
            pass
        elif chosen_option == 3:
            pass
        elif chosen_option == 4:
            print("\nDziękujemy za skorzystanie z ParcelGo!\nDo widzenia")
            return False
        else:
            print("\nBłędny wybór\nProszę o wybranie numeru opcji ze wskazanej listy\n")




