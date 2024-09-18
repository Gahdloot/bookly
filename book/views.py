from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from .models import Book, Customers, BookHistory
from .serializers import  BookSerializer, CustomersSerializer, BookHistorySerializer
from datetime import datetime
# Create your views here.


class PublicBookViewsets(ViewSet):
    authentication_classes = []

    def retrieve(self, request, pk):
        book =  Book.objects.get(id=pk)
        serializer = BookSerializer(book)
        return Response(serializer.data, status=200)

    @action(detail=False, methods=["get"])
    def available(self, request):
        available_books = Book.objects.filter(available_date__gte=datetime.now())
        serializer = BookSerializer(available_books, many=True)
        return Response(serializer.data, status=200)
        
    
    def list(self, request):
        #add filter
        book = Book.objects.all()
        serializer = BookSerializer(book, many=True)
        return  Response(serializer.data, status=200)
    

    @action(detail=False, methods=["post"])
    def sign_up(self, request):
        data = request.data
        try:
            customer = Customers.objects.get(email=data.get('email'))
        except ObjectDoesNotExist:
            if data.get("first_name") is None or  data.get("last_name") is None or data.get("email") is None:
                return Response({"error": "Please provide all required fields"}, status=400)
            customer = Customers.objects.create(email=data.get("email"),  first_name=data.get("first_name"), last_name=data.get("last_name"))
            customer.save()
        except Exception as e:
            return  Response({"error": f"{e}"}, status=400)
    
    @action(detail=False, methods=["post"])
    def borrow(self, request):
        data = request.data
        try:
            customer = Customers.objects.get(email=data.get('email'))
        except ObjectDoesNotExist:
            if data.get("first_name") is None or  data.get("last_name") is None or data.get("email") is None:
                return Response({"error": "Please provide all required fields"}, status=400)
            customer = Customers.objects.create(email=data.get("email"),  first_name=data.get("first_name"), last_name=data.get("last_name"))
            customer.save()
        except Exception as e:
            return  Response({"error": f"{e}"}, status=400)
        
        try:
            book =  Book.objects.get(id=data.get('book_id'))
        except ObjectDoesNotExist:
            return  Response({"error": "Book not found"}, status=404)
        except Exception as e:
            return  Response({"error": f"{e}"}, status=400)
        try:
            date_obj = datetime.strptime(data.get("return_date"), "%Y-%m-%d").date()
            if book.is_avaliable is False:
                return  Response({"error": "Book  is not available"}, status=400)
            book.avaiable_date = date_obj
            book.save()
            book_history = BookHistory.objects.create(book=book, customer=customer, date_returned=date_obj)
            book_history.save()
            return Response({"message": "Book borrowed successfully"}, status=200)
        
        except Exception as e:
            return  Response({"error": f"{e}"}, status=400)
        

class AdminBookViewsets(ViewSet):
    authentication_classes = []

    @action(detail=False, methods=["post"])
    def add_book(self, request):
        data = request.data
        if data.get("title") is None or data.get("author") is None  or data.get("price") is None or data.get("pages") is None or  data.get("publisher") is None or data.get("category") is  None:
            return Response({"error": "Please provide all required fields"}, status=400)
        try:
            book = Book.objects.create(title=data.get("title"), 
                                       author=data.get("author"), 
                                       price=data.get("price"),
                                       pages=data.get("pages"),
                                       publisher=data.get("publisher"),
                                       category=data.get("category"))
            book.save()
            return Response({"message": "Book added successfully"}, status=201)
        except Exception as e:
            return Response({"error": f"{e}"}, status=400)
        
    @action(detail=False, methods=["get"])
    def users(self, request):
        users = Customers.objects.all()
        serializer = CustomersSerializer(users, many=True)
        return Response(serializer.data, status=200)
    
    @action(detail=False, methods=["post"])
    def delete_book(self, request, pk):
        try:
            book  = Book.objects.get(id=pk)
            book.delete()
            return Response({"message": "Book deleted successfully"}, status=200)
        except ObjectDoesNotExist:
            return Response({"error": "Book not found"}, status=404)
        except Exception as e:
            return Response({"error": f"{e}"}, status=400)
        
    @action(detail=False, methods=["get"])
    def book_history(self, request, pk):
        try:
            book = Book.objects.get(id=pk)
            book_history = BookHistory.objects.filter(book=book)
            serializer = BookHistorySerializer(book_history, many=True)
            return Response(serializer.data, status=200)
        except ObjectDoesNotExist:
            return Response({"error": "Book not found"}, status=404)
        except Exception as e:
            return Response({"error": f"{e}"}, status=400)
        

    @action(detail=False, methods=["get"])
    def customer_history(self, request, pk):
        try:
            customer = Customers.objects.get(email=pk)
            book_history = BookHistory.objects.filter(customer=customer)
            serializer = BookHistorySerializer(book_history, many=True)
            return Response(serializer.data, status=200)
        except ObjectDoesNotExist:
            return Response({"error": "Book not found"}, status=404)
        except Exception as e:
            return Response({"error": f"{e}"}, status=400)
        

    def all_books(self, request, pk):
        #get all books, their status, and next avaliable date
        try:
            books = Book.objects.all()
            serializer = BookSerializer(books, many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({"error": f"{e}"}, status=400)
