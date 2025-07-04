Little Lemon Restaurant - API Testing Guide
============================================

This file contains testable API endpoints and detailed instructions for testing the Little Lemon restaurant management system.

PREREQUISITES
============
1. Ensure the Django server is running: python manage.py runserver
2. The application should be accessible at: http://127.0.0.1:8000/
3. MySQL database should be properly configured and running

TESTABLE API ENDPOINTS
=====================

1. RESERVATIONS API
-------------------
Endpoint: GET /api/reservations/
Purpose: Retrieve booking data for a specific date
Authentication: Not required
CSRF Protection: Disabled for testing

Test Cases:

a) Valid date with existing bookings:
   URL: http://127.0.0.1:8000/api/reservations/?date=2024-01-15
   Expected Response:
   {
     "success": true,
     "date": "2024-01-15",
     "bookings": [
       {
         "id": 1,
         "first_name": "John",
         "reservation_slot": "19:00",
         "created_at": 1
       }
     ]
   }

b) Valid date with no bookings:
   URL: http://127.0.0.1:8000/api/reservations/?date=2024-12-25
   Expected Response:
   {
     "success": true,
     "date": "2024-12-25",
     "bookings": [],
     "message": "No Booking"
   }

c) Invalid date format:
   URL: http://127.0.0.1:8000/api/reservations/?date=invalid-date
   Expected Response:
   {
     "success": false,
     "message": "Invalid date format"
   }

d) Missing date parameter:
   URL: http://127.0.0.1:8000/api/reservations/
   Expected Response:
   {
     "success": false,
     "message": "Please provide a date parameter"
   }

e) Wrong HTTP method (POST):
   URL: http://127.0.0.1:8000/api/reservations/
   Method: POST
   Expected Response:
   {
     "success": false,
     "message": "Only GET requests are supported"
   }

TESTING TOOLS
============

1. Browser Testing:
   - Open browser and navigate to the API URLs above
   - Check browser's developer tools for response details

2. cURL Testing:
   ```bash
   # Test valid date
   curl "http://127.0.0.1:8000/api/reservations/?date=2024-01-15"
   
   # Test invalid date
   curl "http://127.0.0.1:8000/api/reservations/?date=invalid"
   
   # Test missing parameter
   curl "http://127.0.0.1:8000/api/reservations/"
   ```

3. Postman Testing:
   - Create new GET request
   - Set URL: http://127.0.0.1:8000/api/reservations/
   - Add query parameter: date=2024-01-15
   - Send request and verify response

4. Python Requests Testing:
   ```python
   import requests
   
   # Test API endpoint
   response = requests.get('http://127.0.0.1:8000/api/reservations/', 
                          params={'date': '2024-01-15'})
   print(response.json())
   ```

WEB PAGES FOR TESTING
====================

1. Homepage:
   URL: http://127.0.0.1:8000/
   Purpose: Main restaurant homepage

2. About Page:
   URL: http://127.0.0.1:8000/about/
   Purpose: Restaurant information

3. Menu Page:
   URL: http://127.0.0.1:8000/menu/
   Purpose: Display all menu items

4. Individual Menu Item:
   URL: http://127.0.0.1:8000/menu_item/1/
   Purpose: Display specific menu item (replace '1' with actual menu item ID)

5. Booking Page:
   URL: http://127.0.0.1:8000/book/
   Purpose: Make table reservations
   Note: This page has AJAX functionality for form submission

6. User Registration:
   URL: http://127.0.0.1:8000/register/
   Purpose: Create new user account

7. User Login:
   URL: http://127.0.0.1:8000/login/
   Purpose: Authenticate existing users

8. User Profile:
   URL: http://127.0.0.1:8000/profile/
   Purpose: View user's booking history
   Note: Requires user authentication
