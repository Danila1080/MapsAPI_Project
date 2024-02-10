from geocoder import get_ll_span
import requests


def get_image(toponym, spn_value=None):
    '''
    функция получает изображение по запросу,
    возващает поток байт, либо false, в качестве аргумента принимает адрес
    и необязательный аргумент spn_value.
    :param toponym:
    :param spn_value:
    :return response, False:
    '''
    if toponym:
        ll, spn = get_ll_span(toponym)
        map_params = {
            "ll": ll,
            "spn": spn,
            "l": "map",
        }
        # если передан масштаб, то соответствующий параметр в запросе будет изменен
        if spn_value:
            map_params["spn"] = str(','.join(str(x) for x in spn_value))

        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=map_params)
        return response
    return False
