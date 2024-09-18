from rest_framework import serializers
from .models import Book, Customers, BookHistory

class  BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class  CustomersSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Customers
        fields  = '__all__'

class   BookHistorySerializer(serializers.ModelSerializer):
    book = serializers.SerializerMethodField()
    customer = serializers.SerializerMethodField()
    class Meta:
        model = BookHistory