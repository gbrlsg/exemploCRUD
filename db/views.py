from random import uniform,randint
from typing import List

from django.shortcuts import render
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
from django.db import connection
from db.models import *
from db.serializers import *

from shapely.geometry import Polygon

from db.utils import gen_mock_cnpj,gen_square_area

# Create your views here.

@csrf_exempt
def clients_list(request):
    if request.method == "GET":
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data,safe=False,status=status.HTTP_200_OK)
    elif request.method == "POST":
        client_data = JSONParser().parse(request)
        serializer = ClientSerializer(data=client_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else: return Response(status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def client_detail(request, pk):
    try:
        client = Client.objects.get(pk=pk)
    except Client.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    match request.method:
        case "GET": 
            serializer = ClientSerializer(client)
            return Response(serializer.data)
        case "DELETE":
            client.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        case "PUT":
            clientUpdateData = JSONParser().parse(request)
            serializer = ClientSerializer(client,data=clientUpdateData)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        case "POST":
            vehicleData = JSONParser().parse(request)
            vehicleData['client'] = pk
            serializer = VehicleSerializer(data=vehicleData)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        case _: return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

@csrf_exempt
def vehicle_detail(request, pk):
    try:
        vehicle = Vehicle.objects.get(pk=pk)
    except Vehicle.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    match request.method:
        case "GET": 
            serializer = VehicleSerializer(vehicle)
            return Response(serializer.data)
        case "DELETE":
            vehicle.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        case "PUT":
            vehicleUpdateData = JSONParser().parse(request)
            serializer = VehicleSerializer(vehicle,data=vehicleUpdateData)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def onix_test(pk: int):
    onix_vehicles = OnixsatSerializer(
        Onixsat.objects.using('onixPos').get(pk=pk)) 
    return Response(
        onix_vehicles.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def clear_db(request: Request):
    Client.objects.all().delete()
    Vehicle.objects.all().delete()
    Area.objects.all().delete()
    with connection.cursor() as cursor:
        cursor.execute(
        f"DELETE FROM sqlite_sequence WHERE name='{Vehicle._meta.db_table}';")
        cursor.execute(
        f"DELETE FROM sqlite_sequence WHERE name='{Area._meta.db_table}';")
        cursor.execute(
        f"DELETE FROM sqlite_sequence WHERE name='{Client._meta.db_table}';")
    return Response(
        "O banco de dados foi esvaziado.", status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([AllowAny])
def test(request: Request):
    test_clients:List[Client] = []
    n_of_test_clients = randint(3,10)
    for n in range(1,n_of_test_clients+1):
        client = Client(
                name = f'Cliente Teste {n}',
                cnpj = gen_mock_cnpj([clnt.cnpj for clnt in test_clients])
            )
        client.save()
        n_of_test_areas = randint(1,3)
        for n in range(1,n_of_test_areas+1):
            area_perimeter = gen_square_area(5.0)
            area = Area(
                name = f'{client.name}/ Area teste {n}',
                client=client,
                perimeter= ' '.join([str(point) for point in area_perimeter])
            )
            area.save()
        test_clients.append(client) 
    serialized_clients = ClientSerializer(test_clients, many=True)
    return Response(serialized_clients.data, status=status.HTTP_200_OK)