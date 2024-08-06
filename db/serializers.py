from rest_framework import serializers

from db.models import Vehicle, Client, Onixsat


class VehicleSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    plate = serializers.CharField(max_length=7)
    serialNumber = serializers.CharField(max_length=10)
    vehicleType = serializers.ChoiceField(choices=Vehicle.VehicleType)
    client = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all())
    creationDate = serializers.DateTimeField(read_only=True,format='%d/%m/%y %H:%M')
    lastModified = serializers.DateTimeField(read_only=True,format='%d/%m/%y %H:%M')

    def create(self, validated_data):
        return Vehicle.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.plate = validated_data.get('plate', instance.plate)
        instance.serialNumber = validated_data.get('serialNumber', instance.serialNumber)
        instance.client = validated_data.get('client', instance.client)
        instance.save()        
        return instance

class ClientSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=150)
    cnpj = serializers.CharField(max_length=14)
    fleetSize = serializers.SerializerMethodField()
    fleet = serializers.SerializerMethodField()
    creationDate = serializers.DateTimeField(read_only=True,format='%d/%m/%y %H:%M')
    lastModified = serializers.DateTimeField(read_only=True,format='%d/%m/%y %H:%M')

    def get_fleetSize(self, obj):
        return len(obj.vehicle_set.all())

    def get_fleet(self, obj):
        return VehicleSerializer(obj.vehicle_set.all(), many=True).data 

    def create(self, validated_data):
        return Client.objects.create(**validated_data)
    
    def update(self, instance, validate_data):
        instance.name = validate_data.get('name', instance.name)
        instance.cnpj = validate_data.get('cnpj', instance.cnpj)
        instance.save()    
        return instance

class OnixsatSerializer(serializers.ModelSerializer):
    """"""
    class Meta:
        model = Onixsat
        fields = '__all__'
