from geocoder import get_ll_span
import requests


def get_image(toponym, spn_custom_value=None):
    '''
    функция получает изображение по запросу,
    возващает поток байт и масштаб, либо false. В качестве аргумента принимает адрес
    и необязательный аргумент spn_value.
    :param toponym:
    :param spn_custom_value:
    :return response, spn_to_return:
    :return False:
    '''
    if toponym:
        ll, spn = get_ll_span(toponym)
        # текущее значение
        spn_to_return = [float(x) for x in spn.split(',')]

        # параметры запроса
        map_params = {
            "ll": ll,
            "spn": spn,
            "l": "map",
        }

        # если передан масштаб, то параметр для запроса будет изменен
        if spn_custom_value:
            map_params["spn"] = str(','.join(str(x) for x in spn_custom_value))
            spn_to_return = spn_custom_value

        # запрос
        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=map_params)

        return response, spn_to_return

    return False
