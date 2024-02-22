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
            f"{e} - Proszę o wskazanie prawidłowej wartości w postaci cyfr.\nPodawanie wartości dziesiętnych powinno "
            f"nastąpić po znaku '.'"
        )
        get_package_dimensions()


def dimensions_validation(wt, dpt, ht, wd):
    is_package_ok = True
    if wt > 20:
        print(f"\n Przekoroczono makymalną wagę paczki o {round((wt - 20), 2)}kg\n")
        is_package_ok = False
    if wd > 40:
        print(
            f"\n Przekoroczono makymalny rozmiar szerokości paczki o {round((wd - 40), 2)}cm\n"
        )
        is_package_ok = False
    if ht > 40:
        print(
            f"\n Przekoroczono makymalny rozmiar wysokości paczki o {round((ht - 40), 2)}cm\n"
        )
        is_package_ok = False
    if dpt > 60:
        print(
            f"\n Przekoroczono makymalny rozmiar głebokości paczki o {round((dpt - 60), 2)}cm\n"
        )
        is_package_ok = False
    return is_package_ok


def dm_ver_loop(chosen_option):
    dm_list = get_package_dimensions()
    if not dimensions_validation(dm_list[0], dm_list[1], dm_list[2], dm_list[3]):
        return dm_ver_loop(chosen_option)
