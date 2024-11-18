from . import models
from . import models
from . import serializers
from rest_framework import viewsets
from django.http import HttpResponse
from django.forms import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination  
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView


class ItemPagination(PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 100

class TheaterApiListCreateAPIView(ListCreateAPIView):
    queryset = models.Theater.objects.all()
    serializer_class = serializers.TheaterSerializer
    pagination_class = ItemPagination

    def create(self, request, *args, **kwargs):
        if models.Theater.objects.filter(address=request.data.get('address')).exists():
            return Response(
                {"detail": "A theater with this address already exists."},
                status=status.HTTP_226_IM_USED
            )
        return super().create(request, *args, **kwargs)
    
    

class TheaterPutClassApi(GenericAPIView):
    def put(self, request, id):
        try:
            theater = models.Theater.objects.get(id=id)
            theater_status = request.data.get('status')
            theater.theater_status = theater_status
            theater.save()
            return Response(status=status.HTTP_200_OK)
        except models.Theater.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class FetchTheaterStaff(GenericAPIView):
    permission_classes =[IsAuthenticated]
    def get(self, request, email):
        theaters = models.Theater.objects.filter(email=email)
        paginator = ItemPagination() 
        paginated_theaters = paginator.paginate_queryset(theaters, request) 
        serializer = serializers.TheaterSerializer(paginated_theaters, many=True)
        return paginator.get_paginated_response(serializer.data)


class TheaterApiRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = models.Theater.objects.all() 
    serializer_class = serializers.TheaterSerializer
    lookup_field='id'



class ScreenTypePostGet(ListCreateAPIView):
    queryset = models.ScreenType.objects.all()
    serializer_class = serializers.ScreenTypeSerializer
    pagination_class = ItemPagination

class ScreenTypeDeletePut(RetrieveUpdateDestroyAPIView):
    queryset = models.ScreenType.objects.all()
    serializer_class = serializers.ScreenTypeSerializer

    lookup_field='id'




class ScreenPostGet(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = serializers.ScreenSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(f'Serializer errors: {serializer.errors}')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ScreenGet(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, email):
        try:
            theaters = models.Theater.objects.filter(email=email)
            if not theaters.exists():
                return Response({"error": "Theater not found"}, status=status.HTTP_404_NOT_FOUND)

            screens = models.Screen.objects.filter(theater__in=theaters).prefetch_related('seats')
            paginator = ItemPagination()
            paginated_data = paginator.paginate_queryset(screens, request, view=self)
            serializer = serializers.ScreenGetSerializer(paginated_data, many=True)
            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
class ScreenApiGetShow(APIView):

    def get(self, request, id):
        try:
            if models.Theater.objects.filter(id=id).exists():
                screen = models.Screen.objects.filter(theater__in=[id])
                serializer = serializers.ScreenGetSerializer(screen, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class ScreenDeletePut(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = models.Screen.objects.all()
    serializer_class = serializers.ScreenSerializer

    lookup_field='id'


class SeatTypeCreateAPI(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = models.Seat_type.objects.all()
    serializer_class = serializers.SeatTypeCreateSerializer


class SeatTypeFetchAPI(GenericAPIView):
    def get(self, request):
        try:
            seat_types = models.Seat_type.objects.filter()
            paginator = ItemPagination()
            paginated_staff = paginator.paginate_queryset(seat_types, request, view=self)
            serializer = serializers.SeatTypeGetSerializer(paginated_staff, many=True)
            return paginator.get_paginated_response(serializer.data)
        except models.Theater.DoesNotExist as e:
            print(e)

class SeatTypeDeleteApi(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = models.Seat_type.objects.all()
    serializer_class = serializers.SeatTypeCreateSerializer
    lookup_field='id'


class SeatAllocationCreateApi(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
                serializer = serializers.SeatAllocationCreateSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as E:
            print(f'This is the error: {E}')
            return Response({'error': str(E)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def get(self, request, id):
        try:
            seat_allocations = models.Seats.objects.filter(screen = int(id))
            serializer = serializers.SeatAllocationGetOrDeleteSerializer(seat_allocations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
class SeatAllocationApiDelete(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = models.Seats.objects.all()
    serializer_class = serializers.SeatAllocationGetOrDeleteSerializer
    lookup_field='id'
