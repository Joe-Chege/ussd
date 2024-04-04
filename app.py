import os
from flask import Flask, request
import requests

app = Flask(__name__)

response = ""

@app.route('/', methods=['POST', 'GET'])
def ussd_callback():
  global response
  session_id = request.values.get("sessionId", None)
  service_code = request.values.get("serviceCode", None)
  phone_number = request.values.get("phoneNumber", None)
  text = request.values.get("text", "default")

  if text == '':
    response = "CON What would you want to check \n"
    response += "1. My Account \n"
    response += "2. My phone number\n"
    response += "3. Locations\n"

  elif text == '1':
    response = "CON Choose account information you want to view \n"
    response += "1. Account number \n"
    response += "2. Account balance"

  elif text == '1*1':
    accountNumber = "ACC1001"
    response = "END Your account number is " + accountNumber

  elif text == '1*2':
    balance = "KES 10,000"
    response = "END Your balance is " + balance

  elif text == '2':
    response = "END This is your phone number " + phone_number

  elif text == '3':   
    response = "CON parking location \n"
    response += "1. Nairobi CBD\n"
    response += "2. Westlands\n"
    response += "3. RIVER ROAD\n"

  elif text == '3*1':
    response = "CON Nairobi CBD parking location: \n"
    try:
      headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY2MGQ4NTI3MDk5NWUwMzRiZWJmMjIxMSIsInBob25lIjoiKzI1NDcwNTc5MTg3MSIsImlhdCI6MTcxMjIzMDI2Mn0.leDWilZutGZ0k1xYQ3yzXILisbAtQ6IndbnnqJeZXr0'
      }
      api_response = requests.get('https://mossaic.site/api/get/parking/spaces', headers=headers)
      parking_data = api_response.json()
      if len(parking_data) > 0:
        for index, parking in enumerate(parking_data):
          parking_name = parking['parkingname']
          response += f"{index}. {parking_name}\n"
      else:
        response += "No parking spaces available\n"
    except requests.exceptions.RequestException as e:
      response += "Error occurred while fetching parking spaces: " + str(e) + "\n"
    
    
    # try:
    #   headers = {
    #     'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY2MGQ4NTI3MDk5NWUwMzRiZWJmMjIxMSIsInBob25lIjoiKzI1NDcwNTc5MTg3MSIsImlhdCI6MTcxMjIzMDI2Mn0.leDWilZutGZ0k1xYQ3yzXILisbAtQ6IndbnnqJeZXr0'
    #   }
    #   api_response = requests.get('https://mossaic.site/api/get/parking/spaces', headers=headers)
    #   parking_data = api_response.json()
    #   if len(parking_data) > 2:
    #     parking_name = parking_data[2]['parkingname']
    #     response += "Parking name: " + parking_name + "\n"
    #   else:
    #     response += "No parking spaces available\n"
    # except requests.exceptions.RequestException as e:
    #   response += "Error occurred while fetching parking spaces: " + str(e) + "\n"

  return response

if __name__ == '__main__':
  app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 80)))