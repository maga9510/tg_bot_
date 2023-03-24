import requests
from math import cos, sin, sqrt, atan2, radians
from tgbot.models import Branch

def get_address_from_coords(coords):
    PARAMS = {
        "apikey": "06faa5e6-679e-4f71-9f49-af861c064b53",
        "format": "json",
        "lang": "ru_RU",
        "kind": "house",
        "geocode": coords
    }

    try:
        r = requests.get(url="https://geocode-maps.yandex.ru/1.x/", params=PARAMS)
        json_data = r.json()
        address_str = json_data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"][
            "GeocoderMetaData"]["AddressDetails"]["Country"]["AddressLine"]
        return address_str

    except Exception as e:
        #единственное что тут изменилось, так это сообщение об ошибке.
        return "Lokatsiyangizni aniqlanmadi.):"


def distance(x : float, y : float) -> dict:
    loc = Branch.objects.all()
    R = 6373.0
    min = 9999999999
    for i in loc:
        lat1 = radians(y)
        long1 = radians(x)
        lat2 = radians(i.position_latitude)
        long2 = radians(i.position_longitude)
        dlat = lat1 - lat2
        dlong = long1 - long2
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlong / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distan = R * c
        if min > distan:
            min = distan
            long = i.position_longitude
            lat = i.position_latitude
            name = i.name
    return {'long': long, 'lat': lat, 'name': name}