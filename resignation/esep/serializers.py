from rest_framework import serializers
from .models import Registration, Resignation
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model

import time

class RegisterationSerializer(serializers.ModelSerializer):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Registration
        exclude = ['created_on','updated_on']

class ResignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resignation
        exclude = ['created_on','updated_on']

    def get_fields(self):
        fields = super().get_fields()
        exclude_fields = self.context.get('exclude_fields', [])
        for field in exclude_fields:
            fields.pop(field)

        return fields