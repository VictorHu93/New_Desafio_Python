from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Client, Book, Loan
from .serializers import ClientSerializer, BookSerializer, LoanSerializer
from django.shortcuts import get_object_or_404

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    @action(detail=True, methods=['get'])
    def books(self, request, pk=None):
        client = get_object_or_404(Client, pk=pk)
        loans = Loan.objects.filter(client=client, return_date__isnull=True)
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data)

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @action(detail=True, methods=['post'])
    def reserve(self, request, pk=None):
        book = get_object_or_404(Book, pk=pk)
        client_id = request.data.get('client_id')
        client = get_object_or_404(Client, pk=client_id)

        if Loan.objects.filter(client=client, book=book, return_date__isnull=True).exists():
            return Response({"error": "This book is already loaned by this client."}, status=status.HTTP_400_BAD_REQUEST)

        if book.status == 'loaned':
            return Response({"error": "Book is already loaned"}, status=status.HTTP_400_BAD_REQUEST)

        Loan.objects.create(client=client, book=book)
        book.status = 'loaned'
        book.save()
        return Response({"message": "Book reserved successfully"}, status=status.HTTP_201_CREATED)
