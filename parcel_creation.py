import random
import json

PACKAGE_VOLUME_RANGE = 5


def generating_parcel_number():
    with open("parcel_list.json", "r") as f:
        parcel_dict = json.load(f)

    parcel_number = str(
        random.randint(0, PACKAGE_VOLUME_RANGE)
    )
    while parcel_number in parcel_dict.keys():
        parcel_number = str(
            random.randint(0, PACKAGE_VOLUME_RANGE)
        )

    return parcel_number


def generating_parcel(data_for_send):

    parcel_number = generating_parcel_number()

    with open("parcel_list.json") as json_file:
        json_decoded = json.load(json_file)

    json_decoded[parcel_number] = data_for_send

    with open("parcel_list.json", "w") as f:
        f.write(
            json.dumps(
                json_decoded,
                sort_keys=True,
                indent=4,
                separators=(",", ": "),
                ensure_ascii=False,
            )
        )

    return parcel_number
