# SportoClub

## Description
SportoClub is a workout planning and tracking application built using Django. It allows users to create custom workouts, perform them, and view a summary and charts of their workout performance.

## Installation
1. Ensure you have Python 3.8 or later installed.
2. Clone this repository.
3. Navigate into the project directory and install the required packages using `pip install -r requirements.txt`.
4. Navigate to the sportoclub folder  `cd sportoclub`.
5. Run migration `python manage.py makemigration`, then `python manage.py migrate`
6. Run the Django server using `python manage.py runserver`.

## Usage
Navigate to `http://localhost:8000/` in your web browser to start using the application. 
- Users can create workouts by selecting from the available exercises. 
- During a workout, users can log their sets, reps, and weight for each exercise. 
- After a workout, users can view a summary of their performance and charts showing their progress over time.
