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

HEADERS = {
    "USER_ID": "4662",  # My personal ID
    "API_KEY": ("HyL9Gepw0D6PiZMgWmUiYNskC2sK7+RwwsSuBq0Q0O8YQVAyGib+foaMnFk9"
                "T7Uq3UFclu3XHQGVgH3i")  # Given API key
}

# Location of Folder containing ranking JSON file
PATH = dirname(abspath(__file__)) + "\\"


# Section End

# Section: API Handling

# Retrieves info, group info, and people info from the API
# Returns the data from the API
def retrieveData():

    response = requests.get(URL, headers=HEADERS,
                            params={"groups": })

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
                             params={"GO": })

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
                 "Group Name",
                 "Friday",
                 "Saturday"])

    for group in signupData["groups"]:
        dateWanted = group["date_want"]
        if dateWanted == 0:
            fridayAvailable, saturdayAvailable = 1, 1
        elif dateWanted == 1:
            fridayAvailable, saturdayAvailable = 1, 0
        elif dateWanted == 2:
            fridayAvailable, saturdayAvailable = 0, 1

        rows.append([group["group_id"],
                     group["creator"],
                     group["name"],
                     fridayAvailable,
                     saturdayAvailable])

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
                     person["person"],
                     "{0} {1}".format(person["first_name"],
                                      person["surname"]),
                     person["vegetarian"],
                     person["vegan"],
                     person["gluten_free"],
                     person["no_lactose"],
                     person["dietary_reqs"]])

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
