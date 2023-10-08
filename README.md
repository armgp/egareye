# egareye

The Egareye has three folders
1. client
2. server
3. monitor_script

Setup a .env file like below
```python
AUTH_ID = ************ # plivo auth_id
AUTH_TOKEN = ********************* # plivo auth_token

# below credentials are required if you are using a virtual machine
# to run the scripts in monitor_script, else you can ignore these and run the scripts
# in your local machine
MONITOR_VM_HOST = **.**.**.** 
MONITOR_VM_PORT = **
MONITOR_VM_USERNAME = uname
MONITOR_VM_PASSWORD = password
```

### client
- Frontend is written using React
- To run frontend
```bash
cd egareye-client
npm install
npm run dev
```
- Frontend runs at http://localhost:5173/
### server
- naviagte to server folder
- Run following commands
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
- To run the backend
```bash
python3 manage.py runserver
```
- Open views.py inside the egareye folder
	- Here `monitorMovie()` function is written in two ways
	- Comment anyone -> one id for when monitoring script is run in your vm, the other is for when the script runs in your local machine. Read the comments to understand which is which
- Backend runs at` http://127.0.0.1:8000/`
- Try 
	- `http://127.0.0.1:8000/running/hyderabad`
	- `http://127.0.0.1:8000/upcoming/hyderabad`
	- `http://127.0.0.1:8000/allmovies/hyderabad`

### monitor_script
- The api calls `start.py` script for eg: `python3 start.py <movie> <city> <phnNo>`
- `start.py` handles `phoneNumbers.json` and `processId.json` to keep track of which all scripts are responsible for which all phonenumbers and movies 
- `monitor.py` is the script responsible for constantly monitoring the website to check if the movie has opened booking and if yes it forwards a call to all those who have subscribed to the movie
```text
Note: These scripts should be uploaded to your vm and the path values in monitor.py and start.py should also be changed to the vm paths if you are using a vm for running the scripts.
```

### Project Overview

This project aims to create a platform where users can receive phone call notifications for their favorite movies when booking opens. The frontend, built with React.js and styled with Tailwind CSS, provides a form where users can enter their name, phone number, city, and select a movie. The form dynamically updates the movie list based on the selected city, fetched via API calls to the Django backend.

### Backend Functionality

#### Endpoints:

1. `GET /allmovies/<cityname>`: Returns a list of all upcoming and currently running movies in a specific city.
2. `GET /running/<cityname>`: Returns a list of currently running movies in a specific city.
3. `GET /upcoming/<cityname>`: Returns a list of upcoming movies in a specific city.
4. `POST /monitor`: Accepts form data (name, phone number, selected movie, selected city) to set up phone call notifications.

#### Workflow:

- When the user submits the form, a POST request is sent to `/monitor` with the user's information.
- The backend's `monitorMovie()` function is triggered, which connects to an Azure virtual machine (VM) running Ubuntu.
- The `start.py` script is executed on the VM with movie, city, and URL arguments.
- `start.py` checks if a monitoring process for the movie in the city is already running. If yes, it updates the phone number list. If not, a new process is initiated.
- The `monitor.py` script, running infinitely, checks every 30 minutes if the bookings for the specified movie in the city are open.
- If bookings are open, `monitor.py` notifies all subscribed phone numbers using the **PLIVO** API for phone call notifications.
- After notifications are sent, data in `phoneNumbers.json` and `processId.json` is cleared, and the process is terminated.

### Key Components and Technologies

- **Frontend:** React.js, Tailwind CSS
- **Backend:** Django REST Framework
- **External Services:** **PLIVO** for phone call notifications
- **Scraping:** BeautifulSoup for scraping movie booking links from `https://ticketnew.com/`

### Design Decisions

- The frontend provides an intuitive form for user input, dynamically updating movie options based on selected city.
- Backend API endpoints allow fetching movie data for specific cities and subscribing users for notifications.
- Azure VM is used for running the monitoring scripts, ensuring the execution environment is separate and scalable.
- **PLIVO** API integration enables automated phone call notifications for users.

### Improvements and Future Work

- Implement error handling and logging for better monitoring of the system.
- Enhance frontend with additional features, such as user authentication and subscription management.
- Optimize the monitoring process to reduce the frequency of API calls for improved performance and cost efficiency.
