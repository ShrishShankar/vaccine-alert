import requests
import datetime
import smtplib, ssl

msg = ''

user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
states = requests.get("https://cdn-api.co-vin.in/api/v2/admin/location/states", headers={'User-Agent': user_agent})
if states.status_code != 200:
    msg += 'Lorem Ipsum\n\nGET admin/location/states {}'.format(states.status_code)

state = "KarnatakA"
state_id = -1
for sd in states.json()['states']:
    if sd['state_name'].lower() == state.lower():
        state_id = sd['state_id']

districts = requests.get("https://cdn-api.co-vin.in/api/v2/admin/location/districts/{}".format(state_id),
                         headers={'User-Agent': user_agent})
if districts.status_code != 200:
    msg += 'Lorem Ipsum\n\nGET admin/location/states {}'.format(districts.status_code)

district = 'BBMP'
district_id = -1
for dd in districts.json()['districts']:
    if dd['district_name'].lower() == district.lower():
        district_id = dd['district_id']

# numdays = 1
age = 21

base = datetime.datetime.today()
base_in_words = base.strftime("%d %b")
base = base.strftime("%d-%m-%Y")
time = datetime.datetime.now().strftime("%-H:%-M:%-S")
# date_list = [base + datetime.timedelta(days=x) for x in range(numdays)]
# date_str = [x.strftime("%d-%m-%Y") for x in date_list]

url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}".format(
    district_id, base)
appointments = requests.get(url, headers={'User-Agent': user_agent})
if appointments.status_code != 200:
    msg += 'Lorem Ipsum\n\nGET appointments {}'.format(appointments.status_code)
for center in appointments.json()['centers']:
    for session in center['sessions']:
        if session["min_age_limit"] <= age and session["available_capacity"] > 0:
            msg += "Center Name: {}".format(center['name'])
            msg += "\nPincode: {}".format(center['pincode'])
            msg += "\nDate: {}".format(session['date'])
            msg += "\nAvailable Capacity: {}".format(session['available_capacity'])
            msg += "\nVaccine: {}".format(session['vaccine'])
            msg += "\nFee Type: {}".format(center['fee_type'])
            msg += "\nAddress: {}".format(center['address'])
            # maps_link = "https://www.google.com/maps/place/{}".format(center['address'].replace(" ", "+"))
            # msg += "\nGoogle Maps (approximate location): {}".format(maps_link)
            msg += "\n\n"

if msg != '':
    port = 465  # For SSL
    password = "Weirdmaggedon11"
    sender_email = "pythonscripts10@gmail.com"
    receiver_email = "shrishshankar11@gmail.com"

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, password)
        msg = "Subject: Available Covid Vaccine Centres [Found at {} on {}]\n\n{} ".format(time, base_in_words, msg)
        server.sendmail(sender_email, receiver_email, msg)
        server.sendmail(sender_email, "kaustubhshan@gmail.com", msg)
else:
    msg = "No available centers found"
    print(msg)

# port = 465  # For SSL
# password = "Weirdmaggedon11"
# sender_email = "pythonscripts10@gmail.com"
# receiver_email = "shrishshankar11@gmail.com"

# # Create a secure SSL context
# context = ssl.create_default_context()

# with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
#     server.login(sender_email, password)
#     server.sendmail(sender_email, receiver_email, msg)
# /v2/appointment/sessions/public/calendarByPin