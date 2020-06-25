from django.http import JsonResponse

"""
Paquete que contiene las respuestas que el servidor enviara al cliente
"""


def bad_request():
    """
    Respuesta cuando se envia una solicitud mala desde el cliente

    Returns:
        obj (JsonResponse): Respuesta que se le envia al cliente, indicandole que la
        peticion es erronea con el codigo 400 del protocolo http
    """
    return JsonResponse(
        {
            'success': False,
            'data': {},
            'messages': 'Bad request',
            'code': 400
        }
    ), 400


def not_found():
    """
    Respuesta cuando no se encuentran los datos solicitados por el cliente

    Returns:
        obj (JsonResponse): Respuesta que se le envia al cliente, indicandole que los
        datos solicitados no se encontraron con el codigo 404 del protocolo http
    """
    return JsonResponse(
        {
            'success': False,
            'data': {},
            'message': 'Resource not found',
            'code': 404
        }
    ), 404


def response(data):
    """
    Respuesta que contiene los datos solicitados por el cliente

    Parameters:
        data (dict): Los datos que se enviaran al cliente

    Returns:
        obj (JsonResponse): Respuesta que se le envia al cliente, con los datos necesarios
        y el codigo 200 del protocolo http
    """
    return JsonResponse(
        {
            'success': True,
            'data': data,
            'message': 'Success',
            'code': 200
        }
    ), 200
