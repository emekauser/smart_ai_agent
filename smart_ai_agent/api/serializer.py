from rest_framework import serializers
from .models import Document, FlightTicket


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = "__all__"


class FlightTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlightTicket
        fields = "__all__"
