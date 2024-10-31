from rest_framework import serializers
from .models import Client, Book, Loan
from .services import calculate_fees

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name', 'email']

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'status']

class LoanSerializer(serializers.ModelSerializer):
    fees = serializers.SerializerMethodField()

    class Meta:
        model = Loan
        fields = ['id', 'client', 'book', 'loan_date', 'return_date', 'fees']

    def get_fees(self, obj):
        return calculate_fees(obj.loan_date, obj.return_date)
