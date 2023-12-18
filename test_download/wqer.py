from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view('GET')
def get(request):
    # Логика обработки GET запроса
    return Response({'method': 'GET'})

# @api_view('POST')
# def post(request):
#     # Логика обработки POST запроса
#     return Response({'method': 'POST'})
#
# @api_view('PUT')
# def put(request):
#     # Логика обработки PUT запроса
#     return Response({'method': 'PUT'})
#
# @api_view('DELETE')
# def delete(request):
#     # Логика обработки DELETE запроса
#     return Response({'method': 'DELETE'})
