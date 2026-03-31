from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Lead, LeadNote, Customer
from .serializers import LeadSerializers, LeadNoteSerializers, CustomerSerializers
from accounts.models import CustomUser
from django.db import models
# Create your views here.

class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializers

    # Assign Lead
    @action(detail=True, methods=['patch'])
    def assign(self, request, pk=None):
        lead = self.get_object()
        user_id = request.data.get('assigned_to')

        try:
            user = CustomUser.objects.get(id=user_id)
            lead.assigned_to = user
            lead.save()
            return Response({'message': 'Lead assigned successfully'})
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

    # Update Status
    @action(detail=True, methods=['patch'])
    def status(self, request, pk=None):
        lead = self.get_object()
        new_status = request.data.get('status')

        lead.status = new_status
        lead.save()

        return Response({'message': 'Status updated successfully'})

    # Add Note
    @action(detail=True, methods=['post'])
    def notes(self, request, pk=None):
        lead = self.get_object()
        note_text = request.data.get('note')

        note = LeadNote.objects.create(
            lead=lead,
            note=note_text
        )

        return Response(LeadNoteSerializers(note).data)
    

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            return Lead.objects.none()

        # ADMIN 
        if user.roles == 'admin':
            return Lead.objects.all()

        # SALES 
        elif user.roles == 'sales':
            return Lead.objects.filter(assigned_to=user)

        # INVENTORY 
        elif user.roles == 'inventory':
            return Lead.objects.filter(status='converted')

        return Lead.objects.none()

        

    @action(detail=True, methods=['post'])
    def convert(self, request, pk=None):
        lead = self.get_object()

        if lead.status != 'converted':
            return Response({"error": "Lead is not converted yet"}, status=400)

        # check already converted
        if hasattr(lead, 'customer'):
            return Response({"message": "Already converted"})

        customer = Customer.objects.create(
            lead=lead,
            name=lead.name,
            email=lead.email,
            phone=lead.phone
        )

        return Response({
            "message": "Lead converted to customer",
            "customer_id": customer.id
        })
        


class CustomerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializers