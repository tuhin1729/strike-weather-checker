from flask import Flask, render_template, request, make_response
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

app = Flask(__name__)

ip = "127.0.0.1"

@app.route('/')
def home():
	location = request.args.get('location', 'Goa')
	weather = [
    {"location": "Karnataka", "weather": "Sunny"},
    {"location": "West Bengal", "weather": "Cloudy"},
    {"location": "Maharashtra", "weather": "Partly Cloudy"},
    {"location": "Tamil Nadu", "weather": "Overcast"},
    {"location": "Kerala", "weather": "Rainy"},
    {"location": "Rajasthan", "weather": "Showers"},
    {"location": "Uttar Pradesh", "weather": "Thunderstorms"},
    {"location": "Himachal Pradesh", "weather": "Snowy"},
    {"location": "Jammu and Kashmir", "weather": "Blizzard"},
    {"location": "Punjab", "weather": "Hail"},
    {"location": "Bihar", "weather": "Sleet"},
    {"location": "Gujarat", "weather": "Windy"},
    {"location": "Assam", "weather": "Foggy"},
    {"location": "Odisha", "weather": "Misty"},
    {"location": "Telangana", "weather": "Humid"},
    {"location": "Madhya Pradesh", "weather": "Dry"},
    {"location": "Andhra Pradesh", "weather": "Hot"},
    {"location": "Haryana", "weather": "Cold"},
    {"location": "Chhattisgarh", "weather": "Breezy"},
    {"location": "Goa", "weather": "Calm"}
]

	if any(entry["location"] == location for entry in weather):
		message = f"Weather of {location} is {next((entry['weather'] for entry in weather if entry['location'] == location), None)}"
	else:
		message = f"Weather of {location} hasn't been updated yet!"

	html = render_template('welcome.html', message=message)
	resp = make_response(html)
	resp.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' https://api.mixpanel.com/; style-src 'self'"
	return resp

@app.route('/submit', methods=('GET', 'POST'))
def bugs():
	if request.method == 'GET':
		html = render_template('report.html')
		resp = make_response(html)
		return resp
	else:
		endpoint = request.form['endpoint']
		url = f"http://{ip}:9000/"+endpoint.replace("'", "")
		url = url.replace('"', '')
		url = url.replace('`','')
		url = url.replace('$','')
		chrome_options = Options()
		chrome_options.add_argument('--headless')
		chrome_options.add_argument('--no-sandbox')
		browser = webdriver.Chrome(options=chrome_options)
		browser.get(url)
		time.sleep(1)
		browser.quit()
		return "Thank you for your request. An admin will visit this endpoint to check if the location already exists in our database. If not, we will add it in our database within 7 working days."

@app.route('/flag')
def flag():
	if request.remote_addr != ip:
		return "CloudSEK{d0n7_$ubm!7_7h!$_fl4g}"
	else:
		return f"{open('flag.txt','r').read()}"

if __name__ == '__main__':
	app.run('0.0.0.0', 9000, debug=True)
