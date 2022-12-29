from .models import *
from rest_framework import serializers

class QuataSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Quata
        fields = '__all__'
        
class ContactSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Contact
        fields = '__all__'
        
class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Customer
        fields = '__all__'
                     

        
class SourceshipSerializer(serializers.HyperlinkedModelSerializer):
    
    contacts = ContactSerializer(many=True, source="contact_set", allow_null=True, read_only=True, required=False)
    quatas = QuataSerializer(many=True, source="quata_set", allow_null=True, read_only=True, required=False)
    class Meta:
        model = Sourceship
        fields = '__all__'
        
class SourceshipModelSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True, required=False)
    contacts = ContactSerializer(many=True, source="contact_set", allow_null=True, read_only=True, required=False)
    quatas = QuataSerializer(many=True, source="quata_set", allow_null=True, read_only=True, required=False)
    class Meta:
        model = Sourceship
        fields = '__all__'
        
        
class SourceSerializer(serializers.HyperlinkedModelSerializer):
    sourceships = SourceshipModelSerializer(many=True, source="sourceship_set", allow_null=True, read_only=True, required=False)
    class Meta:
        model = Source
        fields = '__all__'
        
class Source_sectorSerializer(serializers.HyperlinkedModelSerializer):
    sources = SourceSerializer(many=True, source="source_set", allow_null=True, read_only=True, required=False)
    class Meta:
        model = Source_sector
        fields = '__all__'
                
class Customer_natureSerializer(serializers.HyperlinkedModelSerializer):
    source_sectors = Source_sectorSerializer(many=True, source="source_sector_set", allow_null=True, read_only=True, required=False)
    class Meta:
        model = Customer_nature
        fields = '__all__'