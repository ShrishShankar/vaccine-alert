import requests
import datetime
import smtplib, ssl

info = [{
    "sname":
    "Karnataka",
    "sid":
    -1,
    "districts": [{
        "dname": "BBMP",
        "did": -1,
        "min_age": [{
            "value": 18,
            "emails": ["shrishshankar11@gmail.com", "kaustubhshan@gmail.com"],
            "msg": ""
        }]
    }]
}, {
    "sname":
    "Telangana",
    "sid":
    -1,
    "districts": [{
        "dname": "Rangareddy",
        "did": -1,
        "min_age": [{
            "value": 18,
            "emails": ["shrishshankar11@gmail.com"],
            "msg": ""
        }]
    }]
}]

user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"

error_msg = ""

states_response = requests.get("https://cdn-api.co-vin.in/api/v2/admin/location/states", headers={'User-Agent': user_agent})
if states_response.status_code != 200:
    error_msg += 'Lorem Ipsum\n\nGET admin/location/states {}'.format(states_response.status_code)

for states in info:
    for sd in states_response.json()['states']:
        if sd['state_name'].lower() == states["sname"].lower():
            states["sid"] = sd['state_id']

    districts_response = requests.get("https://cdn-api.co-vin.in/api/v2/admin/location/districts/{}".format(states["sid"]),
                                      headers={'User-Agent': user_agent})
    if districts_response.status_code != 200:
        error_msg += 'Lorem Ipsum\n\nGET admin/location/states {}'.format(districts_response.status_code)

    for districts in states["districts"]:
        for dd in districts_response.json()['districts']:
            if dd['district_name'].lower() == districts["dname"].lower():
                districts["did"] = dd['district_id']

base = datetime.datetime.today()
base_in_words = base.strftime("%d %b")
base = base.strftime("%d-%m-%Y")
time = datetime.datetime.now().strftime("%-H:%-M:%-S")

for states in info:
    for districts in states["districts"]:
        # print(type(districts["min_age"]))
        url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}".format(
            districts["did"], base)
        appointments = requests.get(url, headers={'User-Agent': user_agent})
        if appointments.status_code != 200:
            error_msg += 'Lorem Ipsum\n\nGET appointments {}'.format(appointments.status_code)

        for center in appointments.json()['centers']:
            i = 0
            for session in center['sessions']:
                i += 1
                for ages_dict in districts["min_age"]:
                    if session["min_age_limit"] == ages_dict["value"] and session["available_capacity"] > 0:
                        ages_dict["msg"] += "Center Name: {}".format(center['name'])
                        ages_dict["msg"] += "\nPincode: {}".format(center['pincode'])
                        ages_dict["msg"] += "\nDate: {}".format(session['date'])
                        ages_dict["msg"] += "\nAvailable Capacity: {}".format(session['available_capacity'])
                        ages_dict["msg"] += "\nVaccine: {}".format(session['vaccine'])
                        ages_dict["msg"] += "\nFee Type: {}".format(center['fee_type'])
                        ages_dict["msg"] += "\nAddress: {}".format(center['address'])
                        # maps_link = "https://www.google.com/maps/place/{}".format(center['address'].replace(" ", "+"))
                        # msg += "\nGoogle Maps (approximate location): {}".format(maps_link)
                        ages_dict["msg"] += "\n\n"

port = 465  # For SSL
password = "Weirdmaggedon11"
sender_email = "pythonscripts10@gmail.com"

# Create a secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login(sender_email, password)
    for states in info:
        for districts in states["districts"]:
            for ages_dict in districts["min_age"]:
                if ages_dict["msg"] != "":
                    msg = "Subject: Available Covid Vaccine Centres [Found at {} on {}]\n\n{} ".format(
                        time, base_in_words, ages_dict["msg"])
                    for email in ages_dict["emails"]:
                        server.sendmail(sender_email, email, msg)
                else:
                    msg = "No available centers found"
                    print(msg)

    if error_msg != "":
        server.sendmail(sender_email, "shrishshankar11@gmail.com", msg)