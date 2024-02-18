from geocoder import get_ll_span
import requests

current_pt_pos = None


def get_image(toponym, spn_custom_value, coords, set_pt):
    '''
    функция получает изображение по запросу,
    возващает поток байт и масштаб, либо false. В качестве аргумента принимает адрес
    и необязательный аргумент spn_value.
    :param coords:
    :param toponym:
    :param set_pt:
    :param spn_custom_value:
    :return response, spn_to_return:
    :return False:
    '''
    global current_pt_pos

    try:
        if toponym:
            ll, spn = get_ll_span(toponym)
            # текущее значение
            spn_to_return = [float(x) for x in spn.split(',')]
            coords_to_return = [float(i) for i in ll.split(',')]

            # параметры запроса
            map_params = {
                "ll": ll,
                "spn": spn,
                "l": "map",
                "pt": current_pt_pos
            }

            # если передан масштаб, то параметр для запроса будет изменен
            if spn_custom_value:
                map_params["spn"] = str(','.join(str(x) for x in spn_custom_value))
                spn_to_return = spn_custom_value

            if coords:
                map_params["ll"] = str(','.join(str(i) for i in coords))
                coords_to_return = coords

            if set_pt:
                current_pt_pos = ll
                map_params["pt"] = current_pt_pos

            # запрос
            map_api_server = "http://static-maps.yandex.ru/1.x/"
            response = requests.get(map_api_server, params=map_params)

            return response, spn_to_return, coords_to_return

    except Exception:
        return False
