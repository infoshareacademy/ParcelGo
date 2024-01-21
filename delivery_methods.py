def wybierz_metode_dostarczenia():
    print("\nMetody dostarczenia:")
    print("1. Dostarczenie pod wskazany adres przez kuriera")
    print("2. Dostawa do wybranego paczkomatu")

    wybor = input("Wybierz numer metody dostarczenia (1 lub 2): ")

    if wybor == "1":
        package_reciver = input("\nProszę podać imię i nazwisko odbiorcy :").lower
        deliv_town = input("Proszę podać miasto docelowe :").lower
        deliv_street = input("Podaj ulicę: ")
        deliv_number = input("Podaj numer budynku: ")
    elif wybor == "2":
        numer_paczkomatu = input("Podaj numer paczkomatu: ")
        print(f"Dostawa do wybranego paczkomatu. Numer paczkomatu: {numer_paczkomatu}")
    else:
        print("\nNieprawidłowy wybór metody dostarczenia\nProszę o wybranie opcji ze wskazanej listy.")
        wybierz_metode_dostarczenia()
