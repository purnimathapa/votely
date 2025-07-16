# Votely - Academic Institution Voting System

Votely is a Django-based web application designed to facilitate secure and efficient voting processes in academic institutions. The system allows administrators to create and manage elections while enabling users to participate in active elections.

## Features

- User Authentication System
- Election Management
  - Create, edit, and delete elections
  - Set election duration (start and end dates)
  - Add and manage candidates
- Voting System
  - Secure one-vote-per-user system
  - Real-time election results
  - Vote status tracking
- Responsive Design
  - Bootstrap 5 based UI
  - Mobile-friendly interface

## Technology Stack

- Python 3.x
- Django 5.2.1
- Bootstrap 5
- SQLite (Development) / MySQL (Production)
- Django Crispy Forms

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/votely.git
   cd votely
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```bash
   python manage.py migrate
   ```

5. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Run development server:
   ```bash
   python manage.py runserver
   ```

7. Access the application at http://127.0.0.1:8000/

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 