from rest_framework import serializers
from apps.core.services.status import *
from .models import Region, District, Address, WorkingDay


class AddressWorkingDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkingDay
        fields = ("is_working_day", "day", "work_start", "work_end")


class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Region
        fields = ('id', 'name')


class DistrictSerializer(serializers.ModelSerializer):

    class Meta:
        model = District
        fields = ('id', 'name')


class AddressDetailSerializer(serializers.ModelSerializer):
    region = RegionSerializer()
    district = DistrictSerializer()

    class Meta:
        model = Address
        fields = (
            'id',
            'address1',
            'address2',
            'latitude',
            'longitude',
            'region',
            'district',
        )


class AddressShortSerializer(serializers.ModelSerializer):
    region = RegionSerializer()
    district = DistrictSerializer()

    class Meta:
        model = Address
        fields = (
            'id',
            'address1',
            'address2',
            'latitude',
            'longitude',
            'region',
            'district',
        )


class AddressMiniSerializer(serializers.ModelSerializer):
    region = RegionSerializer()
    district = DistrictSerializer()

    class Meta:
        model = Address
        fields = (
            'id',
            'address1',
            'region',
            'district',
        )

