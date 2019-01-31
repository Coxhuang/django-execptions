from django.shortcuts import render
from app import models
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from drf_dynamic_fields import DynamicFieldsMixin
from app.execption import myException422
from rest_framework.response import Response
from rest_framework import status



class getserializer(DynamicFieldsMixin,serializers.ModelSerializer):
    class Meta:
        model = models.Student
        fields = ["name","age"]
        extra_kwargs = {
            'age': {"required": True},
        }




class get_view(mixins.CreateModelMixin,
               mixins.DestroyModelMixin,
               mixins.UpdateModelMixin,
               mixins.ListModelMixin,
               mixins.RetrieveModelMixin,
               GenericViewSet):

    queryset = models.Student.objects.all()
    serializer_class = getserializer

    def validation_error(self,serializer):
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            d = e.__dict__
            list_field = []
            for i,k in d["detail"].items():
                list_field.append(dict(field=i,message=k[0]))
            raise myException422({"code": 422, "message": "Validation Failed", "errors": list_field})
        return None

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        self.validation_error(serializer)  # 自定义序列化异常
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
