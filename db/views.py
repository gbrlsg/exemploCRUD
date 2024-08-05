from django.shortcuts import render
from rest_framework import status
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.db import connection
from db.models import Vehicle, Client
from db.serializers import VehicleSerializer, ClientSerializer

# Create your views here.

@csrf_exempt
def clients_list(request):
    if request.method == "GET":
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return JsonResponse(serializer.data,safe=False,status=status.HTTP_200_OK)
    elif request.method == "POST":
        client_data = JSONParser().parse(request)
        serializer = ClientSerializer(data=client_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else: return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def client_detail(request, pk):
    try:
        client = Client.objects.get(pk=pk)
    except Client.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    match request.method:
        case "GET": 
            serializer = ClientSerializer(client)
            return JsonResponse(serializer.data)
        case "DELETE":
            client.delete()
            return HttpResponse(status=status.HTTP_204_NO_CONTENT)
        case "PUT":
            clientUpdateData = JSONParser().parse(request)
            serializer = ClientSerializer(client,data=clientUpdateData)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors, status.HTTP_400_BAD_REQUEST)
        case "POST":
            vehicleData = JSONParser().parse(request)
            vehicleData['client'] = pk
            serializer = VehicleSerializer(data=vehicleData)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data,status=status.HTTP_201_CREATED)
            return JsonResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        case _: return HttpResponse(status=status.HTTP_501_NOT_IMPLEMENTED)

@csrf_exempt
def vehicle_detail(request, pk):
    try:
        vehicle = Vehicle.objects.get(pk=pk)
    except Vehicle.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    match request.method:
        case "GET": 
            serializer = VehicleSerializer(vehicle)
            return JsonResponse(serializer.data)
        case "DELETE":
            vehicle.delete()
            return HttpResponse(status=status.HTTP_204_NO_CONTENT)
        case "PUT":
            vehicleUpdateData = JSONParser().parse(request)
            serializer = VehicleSerializer(vehicle,data=vehicleUpdateData)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors, status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def clear_db(request):
    if request.method == 'GET':
        Client.objects.all().delete()
        Vehicle.objects.all().delete()
        with connection.cursor() as cursor:
            cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{Client._meta.db_table}';")
            cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{Vehicle._meta.db_table}';")
        return HttpResponse("O banco de dados foi esvaziado.", status=status.HTTP_204_NO_CONTENT)
    