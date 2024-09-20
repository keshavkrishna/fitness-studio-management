# Fitness Studio Management System
## Project Overview
This Django-based Fitness Studio Management System is SaaS platform for boutiques, studios, and gyms, designed to handle user management, studio management, class scheduling, and booking operations for fitness studios. The system follows a RESTful API architecture and and the tech stack used for the project is Python and Django. The project uses SQLite as the default database, automatically generating a `db.sqlite3` file for local development. No external database connections are required. Most the code relevant to assignment resides under `/glofox` folder, other file and folders are boilerplate code to run a django project.
### Features

### Architecture
The project follows a layered architecture with the following components:
1. **URLs**: Defining API endpoints
2. **Views**: Handling HTTP requests, invoking appropriate service method and return responses
3. **Services**: the actual business logic is incapsluted here, its uses appropriate Serializers to validate data and constraints
4. **Serializers**: Validating data and constraints
4. **Models**: Representing database structure
Additionally there are enums.py  defining various enumeration typesand constants used throughout the project and a utils.py file contains utility functions that provide common functionalities.
### Key Components
#### Models
- `Users`: Represents system users(can be of two types owner and member)
- `Studio`: Represents fitness studios
- `Class`: Represents classes offered by studios
- `Booking`: Represents class bookings made by members
#### Views
The project uses class-based views (APIView) for each major entity:
- `UserView`
- `StudioView`
- `ClassView`
- `BookingView`
- `ClassAvailabilityView`
- `MemberDashboardView`
#### Services
The architecture uses service classes to encapsulate business logic:
- `UserService`
- `StudioService`
- `ClassService`
- `BookingService`
#### URLs
The `urls.py` file defines RESTful endpoints for each entity and operation.

### API Endpoints
- Users: `/users/`, `/users/<id>/`
- Studios: `/studios/`, `/studios/<id>/`
- Classes: `/classes/`, `/classes/<id>/`
- Bookings: `/bookings/`, `/bookings/<id>/`
- Class Availability: `/classes/<id>/availability/`
- Member Dashboard: `/users/<id>/dashboard/`

### Authentication
Currently, the API endpoints do not require authentication for simplicity.

### Testing
I have attached api.json. It can be imported in tools like postman for testing purpose.
### Setup and Running
```bash
# Clone the repository
git clone https://github.com/keshavkrishna/fitness-studio-management.git
cd fitness-studio-management

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start the development server
python manage.py runserver
```
