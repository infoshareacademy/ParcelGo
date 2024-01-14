# Import Logo from ascii.py
from ascii import logo
from functionality_sending_a_parcel import get_package_dimensions

def main_menu():
# pętla głównego menu
    while True:
        print(f"{logo}\nMenu Główne\n1 - Nadaj paczkę\n2 - Odbierz paczkę\n3 - Status paczki\n4 - Wyjście z aplikacji")

        chosen_option = input("proszę o wskazanie numeru opcji: ")

        if chosen_option == "1":
            get_package_dimensions()

        elif chosen_option == "2":
            pass
    # TODO wywołać funkcjonalność opcji odbioru paczki
        elif chosen_option == "3":
            pass
    # TODO wywołać funkcjonalność opcji śledzenia paczki
        elif chosen_option == "4":
# zamknięcie programu, pętli menu głównego
            print("\nDziękujemy za skorzystanie z ParcelGo!\nDo widzenia")
            return False
# wybranie int innego niż wskazanie wyświetli użytkownikowi komunikat
        else:
            print("\nBłędny wybór\nProszę o wybranie numeru opcji ze wskazanej listy\n")

main_menu()