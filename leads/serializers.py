from rest_framework import serializers
from .models import Lead, LeadNote, Customer

class LeadSerializers(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = '__all__'

class LeadNoteSerializers(serializers.ModelSerializer):
    class Meta:
        model = LeadNote
        fields = '__all__'


class CustomerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'