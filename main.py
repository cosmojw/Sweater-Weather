### Input is weather data, output is what you should wear, at what times
import requests
from datetime import datetime

api_key = "14a7c39c67d640ad876213055262301"
base_url = "http://api.weatherapi.com/v1"
zipcode = ""


## CONSTANTS
# Define all clothing types in a list (or dictionary, giving them a value)
clothing = [
    {
        # TOPS
        "tank top": 0.06,
        "athletic shirt": 0.08,
        "t-shirt": 0.09,
        "long-sleeve shirt": 0.25
    },
    {
        # BOTTOMS
        "athletic shorts": 0.06,
        "cargo shorts": 0.11,
        "sweats": 0.28,
        "jeans": 0.25,
        "cargo": 0.26
    },
    {
        # UNDER JACKETS
        "sweatshirt": 0.36,
        "hoodie": 0.38,
        "turtleneck": 0.30,
        "light jacket": 0.22,
        "softshell jacket": 0.42,
        "windbreaker": 0.15,
        "light vest": 0.13
    },
    {
        # OVERCOATS
        "heavyweight windbreaker": 0.55,
        "puffer": 0.65, 
        "raincoat": 0.12,
        "vest": 0.30
    }
]

## INPUT
# Ask user where they are right now (city, state)
while True:
    try:
        zipcode = input("Where are you right now? (zipcode) ")
        int(zipcode)
    except ValueError:
        continue
    break

# Make the request
params = {
    "key": api_key,
    "q": zipcode
}

response = requests.get(f"{base_url}/forecast.json", params=params)

if response.status_code == 200:
    data = response.json()
    max_temp = data['forecast']['forecastday'][0]['day']['maxtemp_f']
    min_temp = data['forecast']['forecastday'][0]['day']['mintemp_f']
    print(f"Weather in {data['location']['name']}: {data['current']['condition']['text']}, {data['current']['temp_f']}°F")
else:
    print(f"Error: {response.status_code}. Check your API key or city name.")

# # Ask user where they are from (to calibrate) (city, state)
# while True: # Likely remove this and replace with a guess of user what temp they get cold at
#     try:
#         home_zipcode = input("Where have you spent most of you life? (zipcode) ").lower().split(", ")
#     except ValueError:
#         continue
#     break

# ALT: Ask user what temperature (in F) they would consider cold
while True:
    try:
        cold_temp = input("What is the highest temperature (in F) you would consider cold? ")
        int(cold_temp)
    except ValueError:
        print("Please provide an integer.")
        continue
    break
# Ask user for their sex, age, height, and weight
sex = input("What is your sex? (m/f) ").lower().strip()
age = int(input("What is your age? "))
height = int(input("What is your height (in inches)? "))
weight = int(input("What is your weight (in pounds)? "))


bmi = 703 * (weight / height ** 2)

if sex in ["male", "m"]:
    if age < 18:
        body_fat = 1.51 * bmi - 0.70 * age - 2.2
    else:
        body_fat = 1.20 * bmi + 0.23 * age - 16.2
elif sex in ["female", "f"]:
    if age < 18:
        body_fat = 1.51 * bmi - 0.70 * age - 1.4
    else:
        body_fat = 1.20 * bmi + 0.23 * age - 5.4
else:
    body_fat = 1.20 * bmi + 0.23 * age - 16.2

if body_fat > 5 and body_fat < 12:
    fat_value = 0.10
elif body_fat >= 12 and body_fat < 18:
    fat_value = 0.155
elif body_fat >= 18 and body_fat < 25:
    fat_value = 0.22
elif body_fat >= 25 and body_fat < 32:
    fat_value = 0.29
elif body_fat >= 33 and body_fat < 40:
    fat_value = 0.365
else:
    fat_value = 0.40

outfits = []
insulation_values = [] 
# FIXME: Break down this complicated loop into functions. I see a lot of repeating code here.
for top, i in clothing[0].items(): # creates list of lists of all outfit combinations, as well as insulation values
    for bottom, j in clothing[1].items(): 
        outfit = [top, bottom]
        outfits.append(outfit)
        insulation_value = 0.161 + 0.835 * (i + j + fat_value)
        insulation_values.append(insulation_value)
        for jacket, k in clothing[2].items():
            outfit = [top,bottom,jacket]
            outfits.append(outfit)
            insulation_value = 0.161 + 0.835 * (i + j + k + fat_value)
            insulation_values.append(insulation_value)
            for overcoat, l in clothing[3].items():
                outfit = [top,bottom,jacket,overcoat]
                outfits.append(outfit)
                insulation_value = 0.161 + 0.835 * (i + j + k + l + fat_value)
                insulation_values.append(insulation_value)
                
                outfit = [top,bottom,overcoat]
                outfits.append(outfit)
                insulation_value = 0.161 + 0.835 * (i + j + l + fat_value)
                insulation_values.append(insulation_value)

#FIXME: Make this into a function please...PLEASE
current_datetime = data['current']['last_updated']
format_string = '%Y-%m-%d %H:%M'
current_datetime_object = datetime.strptime(current_datetime, format_string)
total_temp = 0
count = 0
for hour in data['forecast']['forecastday'][0]['hour']: # calculates the average temp within the next 5 hours
    datetime_object = datetime.strptime(hour['time'], format_string)
    if datetime_object < current_datetime_object:
        count += 1
        continue
    for i in range(count, count + 5):
        temp = data['forecast']['forecastday'][0]['hour'][i]['temp_f']
        print(temp) # TEST
        total_temp += temp
    break

avg_temp_five_hours = total_temp / 5

print(avg_temp_five_hours)

if avg_temp_five_hours >= 86:
    range = [0, 0.3]
elif avg_temp_five_hours >= 77:
    range = [0.3, 0.5]
elif avg_temp_five_hours >= 74:
    range = [0.5, 0.7]
elif avg_temp_five_hours >= 70:
    range = [0.7, 0.9]
elif avg_temp_five_hours >= 66:
    range = [0.9, 1.2]
elif avg_temp_five_hours >= 60:
    range = [1.2, 1.5]
elif avg_temp_five_hours >= 45:
    range = [1.5, 2.0]
elif avg_temp_five_hours >= 30:
    range = [2.0, 2.9]
else:
    range = [2.9, 100]

valid_outfits = []
for i, value in enumerate(insulation_values):
    if value >= range[0] and value < range[1]:
        valid_outfits.append(outfits[i])

print(valid_outfits)
print(len(valid_outfits))

# FIXME: At common temperatures, there are simply too many options to choose from. Ex. ~60 degrees gives ~500 options to choose from...


# CREATE TABLE OF CLO VALUES RANGES AND THEIR ASSOCIATED TEMPERATURE (F) RANGES
# SEE WHERE THE AVG TEMP FOR FIVE HOURS IS ON THAT TABLE (TABLES ARE IN SCREENSHOTS FOLDER)
# GET THAT CLO VALUE RANGE
# ITERATE THROUGH OUTFITS AND FIND ALL WITH VALUES IN THAT RANGE, PUT INTO ANOTHER LIST
# PRINT OUTFITS



    


## COMPUTATION (make these into functions chat)
# Get weather data from API, store it somewhere (of where they are now and where they are from)
# Calculate their BMI
# Calculate their body fat percentage (using BMI)

## OUTPUT
# Type of jacket should wear (controlled by variable boolean that answers Should wear jacket?)
# Type of top should wear
# Type of bottom should wear
# If should wear another jacket (max top + max jacket does not cover)