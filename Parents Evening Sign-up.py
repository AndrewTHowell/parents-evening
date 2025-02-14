# Section: Importing Modules

# Used to retrieve/send sign-up info to the website's API
import requests

# Used to find local path
from os.path import dirname, abspath

# Used to create Table plan
import csv

# Used to handle data from website
import json


# Section End

# Section: Constants

URL = "https://mildert.co.uk/resources/API/ParentEvent.php"

# Location of Folder containing ranking JSON file
PATH = dirname(abspath(__file__)) + "\\"


# Section End

# Section: API Handling

# Retrieves info, group info, and people info from the API
# Returns the data from the API
def retrieveData():

    response = requests.get(URL, headers=HEADERS,
                            params={"groups": ""})

    if response.status_code == 404:
        print("The API was not found, speak to the webmaster")

    elif response.status_code == 403:
        print("You do not have permission to access the API,"
              " speak to the webmaster")

    elif response.status_code == 200:
        data = response.json()

        return data

    else:
        print("Error Code: {0}".format(response.status_code))


# Sends a list of Group IDs to the API
# Returns True if successful
def sendGo():

    response = requests.post(URL, headers=HEADERS,
                             params={"GO": ""})

    print(response.status_code)

    if response.status_code == 404:
        print("The API was not found, speak to the webmaster")

    elif response.status_code == 400:
        print("Bad request, speak to the webmaster")

    elif response.status_code == 403:
        print("You do not have permission to access the API,"
              " speak to the webmaster")

    elif response.status_code == 409:
        print("The signup is still open")

    elif response.status_code == 200:
        print("Sent successfully")

        return True

    else:
        print("Error Code: {0}".format(response.status_code))

    return False


# Section End

# Section: Main Program

print("*** MENU ***")
print("1. Retrieve Data and print")
print("2. Retrieve Data and save to file")
print("3. Send Go for payment")
choice = int(input("Enter choice: "))

if choice == 1 or choice == 2:
    signupData = retrieveData()

    rows = []

    rows.append(["Group ID",
                 "Group Creator",
                 "Friday Can",
                 "Saturday Can",
                 "Friday Want",
                 "Saturday Want"])

    """
    for key in signupData.keys():
        print(key)

    print()

    for key in signupData["groups"][0].keys():
        print(key)

    print()

    for key in signupData["people"][0].keys():
        print(key)
    """

    for group in signupData["groups"]:
        dateWant = int(group["date_want"])
        fridayWant = 0
        saturdayWant = 0
        if dateWant == 0:
            fridayWant, saturdayWant = 1, 1
        elif dateWant == 1:
            fridayWant = 1
        elif dateWant == 2:
            saturdayWant = 1

        dateCan = int(group["date_can"])
        fridayCan = 0
        saturdayCan = 0
        if dateCan == 3:
            fridayCan, saturdayCan = 1, 1
        elif dateCan == 1:
            fridayCan = 1
        elif dateCan == 2:
            saturdayCan = 1

        rows.append([group["group_id"],
                     group["creator"],
                     fridayCan,
                     saturdayCan,
                     fridayWant,
                     saturdayWant])

    rows.append(["Group ID",
                 "Person ID",
                 "Name",
                 "Vegetarian",
                 "Vegan",
                 "Gluten Free",
                 "No Lactose",
                 "Other Dietary Reqs"])

    for person in signupData["people"]:
        rows.append([person["group"],
                     person["user_id"],
                     "{0} {1}".format(person["first_names"],
                                      person["surname"]),
                     person["vegetarian"],
                     person["vegan"],
                     person["gluten_free"],
                     person["no_lactose"],
                     person["dietary_reqs"]])

    # print(len(rows))

if choice == 1:
    for row in rows:
        print(row)

if choice == 2:
    with open(PATH + "Data.csv", "w") as file:
        writer = csv.writer(file, lineterminator="\n")

        writer.writerows(rows)

if choice == 3:
    definitelySend = input("Are you sure you want to send the go ahead for"
                           " payments? (Y or N): ")

    if definitelySend.upper() == "Y":
        sendGo()

# Section End
