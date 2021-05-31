import requests

def Dose_availability_District(district_id,date):
    api = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={}&date={}".format(district_id,date)

    return main_task(api)

def Dose_availability_pincode(pincode,date):
    api = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={}&date={}".format(pincode,date)

    return main_task(api)

def main_task(api):
    response = requests.get(api)
    data = response.json()['sessions']
    output="*"*30

    for area in data:
        if area['available_capacity']>0:
            output+= "Hospital Name:"+area['name'] + "*"*30 +"\n"
            output+='''\
Address:{}
Pincode: {}
available_capacity_dose1 : {}
available_capacity_dose2 : {}
available_capacity : {}
min_age_limit: {}
Time Slots: {}

'''.format(area['address'],area['pincode'],area['available_capacity_dose1'],area['available_capacity_dose2'],
                             area['available_capacity'],area['min_age_limit'],str(area['slots'])[1:-1])
            output+="*"*30
    return output

print(Dose_availability_pincode(110001,"01-06-2021"))
