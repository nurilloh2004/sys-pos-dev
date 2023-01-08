from apps.core.services.status import *
from apps.core.services.generics import CustomAPIView, CustomModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from . import serializers as ser
from apps.core.services.generics import POSResponse
from . models import Region, District


class RegionsAPIView(CustomAPIView):
    """
    GET: {{BASE}}api/v1/address/regions/
    """
    tags = ["Regions list API"]
    serializer_class = ser.RegionSerializer
    queryset = Region.objects.all()
    permission_classes = [AllowAny, ]

    def get(self, request):
        data = []
        regions = Region.objects.all()
        if regions.exists():
            for region in regions:
                data.append({"id": region.id, "name": region.name})
            return self.success_response(results=data)
        else:
            self.update_error_text(catch="Regions")
            self.code = POSResponse.CODE_4
            self.error_message = POSResponse.MSG_4
            return self.error_response()


class DistrictAPIView(CustomAPIView):
    """
    GET: {{BASE}}api/v1/address/district/{id}/
    """
    tags = ["District list API"]
    serializer_class = ser.DistrictSerializer
    queryset = District.objects.all()
    permission_classes = [AllowAny, ]

    def get(self, request, pk):
        data = []
        try:
            qs = District.objects.filter(region_id=pk)
            for district in qs:
                data.append({"id": district.id, "name": district.name})
            return self.success_response(results=data)
        except Exception as e:
            self.code = POSResponse.CODE_3
            self.error_message = POSResponse.MSG_3
            self.exception = e.args
            return self.error_response()
