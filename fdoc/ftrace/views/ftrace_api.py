from ..models import *
from rest_framework import viewsets
from ..serializers import *
from ..filters import *
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filterset_class = CustomerFilter # 过滤类

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    #filter_class = BookFilter # 过滤类



class QuataViewSet(viewsets.ModelViewSet):
    queryset = Quata.objects.all()
    serializer_class = QuataSerializer
    
class Customer_natureViewSet(viewsets.ModelViewSet):
    queryset = Customer_nature.objects.all()
    serializer_class = Customer_natureSerializer
    
class Source_sectorViewSet(viewsets.ModelViewSet):
    queryset = Source_sector.objects.all()
    serializer_class = Source_sectorSerializer
    filterset_class = Source_sectorFilter
    
class SourceViewSet(viewsets.ModelViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
    
    
class SourceshipViewSet(viewsets.ModelViewSet):
    queryset = Sourceship.objects.all()
    serializer_class = SourceshipSerializer
    
class SourceshipModelViewSet(viewsets.ModelViewSet):
    queryset = Sourceship.objects.all()
    serializer_class = SourceshipModelSerializer
    
    
    