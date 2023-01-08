from rest_framework import serializers
from apps.core.services.status import *
from .models import UserBalance, Transaction


class UserBalanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserBalance
        fields = (
            "id",
            "amount",
            "is_blocked"
        )


