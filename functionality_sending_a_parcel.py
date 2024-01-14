def get_package_dimensions():
    print("\nProszę o wprowadzenie wymiarów przesyłki")
    wt = float(input("Waga w kg :"))
    dpt = float(input("Głębokość w cm :"))
    ht = float(input("Wysokość w cm :"))
    wd = float(input("szerokość w cm :"))
    return [wt, dpt, ht, wd]

