


# Ticket Website

## Overview
Ticket Website is a web-based ticketing platform designed to streamline event ticket management. This project provides a user-friendly interface for ticket booking, event organization, and transaction management.
Working Deployment Found Here: https://eoviosa.pythonanywhere.com/ticket/login
Username: "Guest123"
Password: "TestUser#"
The student ID is "1234567"

## Features
- **User Authentication** – Secure login and registration system.
- **Event Management** – Create, update, and manage events.
- **Ticket Booking** – Users can browse events and purchase tickets.
- **Admin Dashboard** – Allows event organizers to track sales and manage attendees.
- **Responsive Design** – Works seamlessly on desktop and mobile devices.

## Technologies Used
- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite/PostgreSQL
- **Version Control:** Git/GitHub

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/eeoviosa/Ticket-Website.git
   ```
2. Navigate to the project directory:
   ```sh
   cd Ticket-Website
   ```
3. Create a virtual environment:
   ```sh
   python -m venv env
   ```
4. Activate the virtual environment:
   - **Windows:**
     ```sh
     env\Scripts\activate
     ```
   - **Mac/Linux:**
     ```sh
     source env/bin/activate
     ```
5. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
6. Apply database migrations:
   ```sh
   python manage.py migrate
   ```
7. Run the development server:
   ```sh
   python manage.py runserver
   ```
8. Open the browser and go to:
   ```
   http://127.0.0.1:8000/
   ```

## Usage
- Sign up or log in to access the dashboard.
- Browse available events and purchase tickets.
- Organizers can create and manage their events from the admin panel.

## Contributing
If you'd like to contribute, please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License.

## Contact
For any inquiries or issues, please reach out via GitHub or email.


