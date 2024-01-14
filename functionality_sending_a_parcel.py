def get_package_dimensions():
    print("\nProszę o wprowadzenie wymiarów przesyłki")
    wt = input("Waga w kg :")
    dpt = input("Głębokość w cm :")
    ht = input("Wysokość w cm :")
    wd = input("szerokość w cm :")

    try:
        return [float(wt), float(dpt), float(ht), float(wd)]

    except Exception as e:
        print(
            f"{e} - Proszę o wskazanie prawidłowej wartości w postaci cyfr.\nPodawanie wartości dziesiętnych powinno nastąpić po znaku '.' "
        )
        get_package_dimensions()
