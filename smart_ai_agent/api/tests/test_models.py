from django.test import TestCase

from api.models import Document, FlightTicket
from django.contrib.auth.models import User


class FlightTicketModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass')

        self.flight_ticket = FlightTicket.objects.create(
            departure="New York",
            arrival="Los Angeles",
            departure_time="2024-07-01T10:00:00Z",
            arrival_time="2024-07-01T13:00:00Z",
            user=self.user,
            is_used=False,
            is_cancelled=False,
            ticket_number=123456,
            seat_number=12,
            pnr="ABC123"
        )

    def test_flight_ticket_creation(self):
        self.assertEqual(self.flight_ticket.departure, "New York")
        self.assertEqual(self.flight_ticket.arrival, "Los Angeles")
        self.assertEqual(self.flight_ticket.ticket_number, 123456)
        self.assertFalse(self.flight_ticket.is_used)
        self.assertFalse(self.flight_ticket.is_cancelled)

    def test_delete_flight_ticket(self):
        ticket_id = self.flight_ticket.id
        self.flight_ticket.delete()
        with self.assertRaises(FlightTicket.DoesNotExist):
            FlightTicket.objects.get(id=ticket_id)

    def test_edit_flight_ticket(self):
        self.flight_ticket.is_used = True
        self.flight_ticket.save()
        updated_ticket = FlightTicket.objects.get(id=self.flight_ticket.id)
        self.assertTrue(updated_ticket.is_used)


class DocumentModelTest(TestCase):
    def setUp(self):
        self.document = Document.objects.create(
            title="Sample Document",
            file_type="txt",
            content="This is a sample document.",
            url="http://example.com/sample-document"
        )

    def test_document_creation(self):
        self.assertEqual(self.document.title, "Sample Document")
        self.assertEqual(self.document.file_type, "txt")
        self.assertEqual(self.document.content, "This is a sample document.")
        self.assertEqual(self.document.url,
                         "http://example.com/sample-document")
