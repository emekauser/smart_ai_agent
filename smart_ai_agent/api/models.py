from django.db import models
from django.contrib.auth.models import User


class Document(models.Model):
    title = models.CharField()
    file_type = models.CharField(max_length=10)
    content = models.TextField()
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class FlightTicket(models.Model):
    departure = models.CharField(max_length=30)
    arrival = models.CharField(max_length=30)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_used = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    ticket_number = models.IntegerField()
    seat_number = models.IntegerField()
    pnr = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Flight Ticket {self.pnr} for {self.user.username} from {self.departure} to {self.arrival}"


class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=40)
    expire_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.session_id} ({self.user.username})"
