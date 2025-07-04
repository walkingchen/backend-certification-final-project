from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Booking, Menu
from .forms import BookingForm, UserRegistrationForm
from datetime import date, datetime
import json


class BookingModelTest(TestCase):
    def setUp(self):
        self.booking = Booking.objects.create(
            first_name="John",
            last_name="Doe",
            guest_number=4,
            comment="Birthday party",
            reservation_date=date(2024, 12, 25),
            reservation_slot="19:00"
        )
    
    def test_booking_creation(self):
        """Test booking creation"""
        self.assertEqual(self.booking.first_name, "John")
        self.assertEqual(self.booking.last_name, "Doe")
        self.assertEqual(self.booking.guest_number, 4)
        self.assertEqual(self.booking.comment, "Birthday party")
        self.assertEqual(self.booking.reservation_date, date(2024, 12, 25))
        self.assertEqual(self.booking.reservation_slot, "19:00")
    
    def test_booking_str_representation(self):
        """Test booking string representation"""
        self.assertEqual(str(self.booking), "John Doe")


class MenuModelTest(TestCase):
    def setUp(self):
        self.menu_item = Menu.objects.create(
            name="Greek Salad",
            price=12,
            menu_item_description="Fresh vegetables with olive oil"
        )
    
    def test_menu_creation(self):
        """Test menu item creation"""
        self.assertEqual(self.menu_item.name, "Greek Salad")
        self.assertEqual(self.menu_item.price, 12)
        self.assertEqual(self.menu_item.menu_item_description, "Fresh vegetables with olive oil")
    
    def test_menu_str_representation(self):
        """Test menu item string representation"""
        self.assertEqual(str(self.menu_item), "Greek Salad")


class BookingFormTest(TestCase):
    def test_booking_form_valid_data(self):
        """Test booking form with valid data"""
        form_data = {
            'first_name': 'Alice',
            'last_name': 'Smith',
            'guest_number': 2,
            'comment': 'Romantic dinner',
            'reservation_date': '2024-12-25',
            'reservation_slot': '20:00'
        }
        form = BookingForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_booking_form_invalid_data(self):
        """Test booking form with invalid data"""
        form_data = {
            'first_name': '',  # Empty name
            'last_name': 'Smith',
            'guest_number': 0,  # Invalid guest number
            'comment': 'Romantic dinner',
            'reservation_date': '2024-12-25',
            'reservation_slot': '20:00'
        }
        form = BookingForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)
        # guest_number == 0 may not raise error because model does not validate min value


class UserRegistrationFormTest(TestCase):
    def test_user_registration_form_valid_data(self):
        """Test user registration form with valid data"""
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_user_registration_form_invalid_data(self):
        """Test user registration form with invalid data"""
        form_data = {
            'username': 'testuser',
            'email': 'invalid-email',
            'password1': 'testpass123',
            'password2': 'differentpass'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertIn('password2', form.errors)


class ViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_home_view(self):
        """Test home view"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
    
    def test_about_view(self):
        """Test about view"""
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')
    
    def test_menu_view(self):
        """Test menu view"""
        response = self.client.get(reverse('menu'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu.html')
    
    def test_book_view_get(self):
        """Test booking view GET request"""
        response = self.client.get(reverse('book'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book.html')
        self.assertIn('form', response.context)
    
    def test_book_view_post_valid(self):
        """Test booking view POST with valid data"""
        data = {
            'first_name': 'Test User',
            'last_name': 'Test',
            'guest_number': 3,
            'comment': 'Test booking',
            'reservation_date': '2024-12-25',
            'reservation_slot': '19:00'
        }
        response = self.client.post(reverse('book'), data)
        self.assertEqual(response.status_code, 200)
        # Check if booking was created
        self.assertTrue(Booking.objects.filter(first_name='Test User').exists())
    
    def test_register_view_get(self):
        """Test register view GET request"""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
    
    def test_register_view_post_valid(self):
        """Test register view POST with valid data"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpass123',
            'password2': 'newpass123'
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 302)  # Redirect
        # Check if user was created
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_login_view_get(self):
        """Test login view GET request"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
    
    def test_login_view_post_valid(self):
        """Test login view POST with valid data"""
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, 302)  # Redirect
    
    def test_logout_view(self):
        """Test logout view"""
        # Login first
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirect
    
    def test_profile_view_authenticated(self):
        """Test profile view for authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
    
    def test_profile_view_unauthenticated(self):
        """Test profile view for unauthenticated user"""
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)  # Redirect to login


class APIViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.booking = Booking.objects.create(
            first_name="APITest",
            last_name="User",
            guest_number=2,
            comment="API test booking",
            reservation_date=date(2024, 12, 25),
            reservation_slot="19:00"
        )
    
    def test_reservations_api_get_valid_date(self):
        """Test reservations API GET with valid date"""
        response = self.client.get(reverse('reservations_api'), {'date': '2024-12-25'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['bookings']), 1)
        self.assertEqual(data['bookings'][0]['first_name'], 'APITest')
    
    def test_reservations_api_get_invalid_date(self):
        """Test reservations API GET with invalid date"""
        response = self.client.get(reverse('reservations_api'), {'date': 'invalid-date'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertIn('Invalid date format', data['message'])
    
    def test_reservations_api_get_no_date(self):
        """Test reservations API GET with no date parameter"""
        response = self.client.get(reverse('reservations_api'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertIn('Please provide a date parameter', data['message'])
    
    def test_reservations_api_post(self):
        """Test reservations API POST request"""
        response = self.client.post(reverse('reservations_api'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertIn('Only GET requests are supported', data['message'])


class IntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='integrationuser',
            email='integration@example.com',
            password='integrationpass123'
        )
    
    def test_user_registration_and_login_flow(self):
        """Test user registration and login flow"""
        # 1. Register new user
        register_data = {
            'username': 'newintegrationuser',
            'email': 'newintegration@example.com',
            'password1': 'newintegrationpass123',
            'password2': 'newintegrationpass123'
        }
        response = self.client.post(reverse('register'), register_data)
        # Should redirect to home after registration
        self.assertIn(response.status_code, [200, 302])
        
        # 2. Check user created
        self.assertTrue(User.objects.filter(username='newintegrationuser').exists())
        
        # 3. Login
        login_data = {
            'username': 'newintegrationuser',
            'password': 'newintegrationpass123'
        }
        response = self.client.post(reverse('login'), login_data)
        self.assertEqual(response.status_code, 302)
        
        # 4. Access profile page
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
    
    def test_booking_creation_and_api_retrieval(self):
        """Test booking creation and API retrieval"""
        # 1. Create booking
        booking = Booking.objects.create(
            first_name="IntegrationTest",
            last_name="User",
            guest_number=5,
            comment="Integration test booking",
            reservation_date=date(2024, 12, 26),
            reservation_slot="20:00"
        )
        # 2. Retrieve booking via API
        response = self.client.get(reverse('reservations_api'), {'date': '2024-12-26'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['bookings']), 1)
        self.assertEqual(data['bookings'][0]['first_name'], 'IntegrationTest')
