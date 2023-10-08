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
