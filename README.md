# Little Lemon Restaurant

A Django-based restaurant management system for Little Lemon restaurant, featuring online booking, menu management, and user authentication.

## Features

- **Online Booking System**: Customers can make table reservations with date and time slot selection
- **Menu Management**: Display restaurant menu items with descriptions and pricing
- **User Authentication**: Registration, login, logout, and user profile management
- **Booking Management**: View and manage user reservations
- **API Endpoints**: RESTful API for retrieving booking data
- **Responsive Design**: Modern UI with CSS styling and restaurant branding

## Technology Stack

- **Backend**: Django 4.1.1
- **Database**: MySQL
- **Frontend**: HTML, CSS, JavaScript
- **Package Management**: Pipenv
- **Python Version**: 3.13.5

## Project Structure

```
meta-littlelemon/
├── littlelemon/          # Django project settings
├── restaurant/           # Main application
│   ├── models.py        # Database models (Booking, Menu)
│   ├── views.py         # View functions and API endpoints
│   ├── urls.py          # URL routing
│   ├── forms.py         # Form definitions
│   ├── templates/       # HTML templates
│   └── static/          # CSS, images, and static files
├── manage.py            # Django management script
└── Pipfile              # Python dependencies
```

## Installation & Setup

### Prerequisites
- Python 3.13.5
- MySQL server
- Pipenv

### Database Setup
1. Create MySQL database:
```sql
CREATE DATABASE littlelemon_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'littlelemon_user'@'localhost' IDENTIFIED BY 'littlelemon_password';
GRANT ALL PRIVILEGES ON littlelemon_db.* TO 'littlelemon_user'@'localhost';
FLUSH PRIVILEGES;
```

### Installation Steps
1. Clone the repository
2. Navigate to the project directory:
   ```bash
   cd meta-littlelemon
   ```
3. Install dependencies:
   ```bash
   pipenv install
   ```
4. Activate virtual environment:
   ```bash
   pipenv shell
   ```
5. Run database migrations:
   ```bash
   python manage.py migrate
   ```
6. Create superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```
7. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Usage

- **Home**: `/` - Restaurant homepage
- **About**: `/about/` - About page
- **Menu**: `/menu/` - Restaurant menu
- **Booking**: `/book/` - Make table reservations
- **Register**: `/register/` - User registration
- **Login**: `/login/` - User login
- **Profile**: `/profile/` - User profile and bookings
- **API**: `/api/reservations/?date=YYYY-MM-DD` - Get bookings for specific date

## API Endpoints

### GET /api/reservations/
Returns booking data for a specific date.

**Parameters:**
- `date` (required): Date in YYYY-MM-DD format

**Response:**
```json
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
```

## Models

### Booking
- `first_name`: Customer's first name
- `last_name`: Customer's last name
- `guest_number`: Number of guests
- `comment`: Additional comments
- `reservation_date`: Booking date
- `reservation_slot`: Time slot

### Menu
- `name`: Menu item name
- `price`: Item price
- `menu_item_description`: Item description

## Development

The project uses Django's built-in development server and MySQL database. Static files are served from the `restaurant/static/` directory, and templates are located in `restaurant/templates/`.

## License

This project is part of a Coursera backend certification final project. 