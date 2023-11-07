# Importing necessary packages--------------------------------------#
import os
import time
from datetime import datetime
from threading import Thread
from weather import OpenWeatherMap

# Trying to get the termcolor package if it exists-------------------------------------#
global termcolor_enable
try:
    from termcolor import colored
    termcolor_enable = True
except:
    termcolor_enable = False

# Making the Favorite City List file--------------------------------------------#
try:
    os.mkdir("data")
    file = open("data/favorites.txt", "a+")
    file.close()
except:
    pass


# Function to print the text in color-----------------------------------#
def print_text(text="", color="white", attributes=[], ends="\n"):
    if termcolor_enable:
        print(colored(text, color, attrs=attributes), end=ends)
    else:
        print(text, end=ends)


# Reading the favority city file---------------------------------#
def read_file():
    with open("data/favorites.txt", "r") as file:
        file_data = file.read()
    return file_data.split("\n")


# Writing the data in the favority city file---------------------------------#
def write_file(data):
    with open("data/favorites.txt", "w") as file:
        for city in data:
            if city != "":
                file.write(city + "\n")


# Appending the city name in the favorite city list----------------------------------#
def append_file(data):
    with open("data/favorites.txt", "a") as file:
        file.write(data + "\n")
        file.close()


# Clearing out the screen------------------------------------#
def clear_screen():
    os.system("CLS")
    weather_app.clear_screen = True
    weather_app.print_name()


def get_current_time():
    current_time = datetime.now()
    hour, minute, second = current_time.hour, current_time.minute, current_time.second
    if hour > 12:
        time_format = 'pm'
    else:
        time_format = 'am'
    return hour, minute, second, time_format

# Weather App Class-------------------------------#


class WeatherMaster(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.name = "Weather Master"
        self.operation = None
        self.start_app = True
        self.city_name = ""
        self.clear_screen = True
        self.weather = OpenWeatherMap()
        self.city_number = 0
        self.time = None
        self.city_error = False
        # self.temp_unit = "C"


    def print_name(self):
        print()
        if self.clear_screen:
            self.clear_screen = False
            print_text(
                f"#-------------- *** {self.name} *** --------------#", "red", ["blink"], ends="\n\n")

    def search_weather(self):
        if len(self.city_name) > 0:
            self.weather.get_weather(self.city_name)
            if not self.weather.error:
                self.city_error = False
                self.time = get_current_time()
                print_text(f"Time {self.time[0]}: {self.time[1]}: {
                           self.time[2]}{self.time[3]}", 'red', ends="\n")
                if termcolor_enable:
                    print(colored(f"                 ", 'yellow',
                                  attrs=['blink'], on_color='on_red'), end=" ")
                print_text(f"{self.city_name.title()} ", 'blue',
                           attributes=['blink'], ends=" ")
                print(self.weather.weather_icon, end="")
                print_text(f"{self.weather.weather_des} and temperature is {
                    self.weather.temperature}", 'red', ends="\n\n")
            else:
                self.city_error = True

    def search_weather_all_cities(self):
        cities = read_file()
        for city in cities:
            if city != "":
                self.city_name = city
                self.search_weather()

    def search_city(self, city):
        city_names = [x.lower() for x in read_file()]
        if city.isdigit() and int(city) < len(city_names):
            city = city_names[int(city) - 1]

        self.city_name = city
        if city.lower() in city_names:
            self.city_number = city_names.index(city.lower())
            return True
        else:
            return False

    def all_city_names(self):
        print()
        print_text("#------- FAVORITE CITY LIST -------#", "cyan")
        city_names = read_file()
        for city in city_names:
            if city == "":
                break
            print_text(f"            {city_names.index(
                city) + 1}. {city}", "yellow")
        print_text("#----------------------------------#", "cyan", ends="\n\n")

    def add_city_name(self, city):
        if self.search_city(city):
            return f"{city} is already in Favorite City List."

        else:
            append_file(city.title())
            self.all_city_names()
            return f"{city} is added to Favorite City List."

    def delete_city_name(self, city):
        city_names = [x.lower() for x in read_file()]

        if self.search_city(city):
            city_names.remove(self.city_name)
            write_file([x.title() for x in city_names])
            return f"{self.city_name.title()} is removed from in Favorite City List."

        else:
            return f"{self.city_name.title()} is not exits in Favorite City List."

    def update_city_name(self, new_city):
        city_names = [x.lower() for x in read_file()]
        old_city = city_names[self.city_number]
        if self.search_city(new_city):
            return f"{old_city.title()} already exists in Favorite City List."
        city_names[self.city_number] = new_city.lower()
        write_file([x.title() for x in city_names])
        clear_screen()
        return f"{old_city.title()} is updated to {self.city_name.title()} in Favorite City List."

    def current_city_favorite_city(self):
        while True:
            print_text(
                "Do you want to enter current city to favorite city list? Yes/No.", "light_green")
            add_city = input("Enter you choice: ").lower()

            if add_city in ["yes", "y"]:
                output = self.add_city_name(self.city_name)
                print()
                print_text(output, "light_cyan", ["blink"])
                break

            elif add_city in ["no", "n"]:
                break

            else:
                print_text("Invalid Input", "light_red")


# Weather Class Object-------------#
weather_app = WeatherMaster()

# Main menu options----------------------------------#
menu_items = [
    {"text": "Choose the operation", "color": "magenta",
        "attributes": ["bold"], "ends": "\n"},
    {"text": "1. Check weather by CITY NAME.",
        "color": "blue", "attributes": [], "ends": "\n"},
    {"text": "2. Edit Favorite CITY List.",
        "color": "blue", "attributes": [], "ends": "\n"},
    {"text": "3. Search Weather for Favorite CITY List.",
        "color": "blue", "attributes": [], "ends": "\n"},
    {"text": "4. Clear Screen.", "color": "blue", "attributes": [], "ends": "\n"},
    {"text": "5. Exit", "color": "blue", "attributes": [], "ends": "\n\n"},
    {"text": "Enter your choice by typing the number given in front of the choices.",
        "color": "yellow", "attributes": [], "ends": "\n\n"},
]

# Favorite City CRUD Operations Options----------------------------------#
favority_city_operations = [
    {"text": "Choose the operation for favorite cities Weather",
        "color": "magenta", "attributes": ["bold"], "ends": "\n"},
    {"text": "1. Show names of all cities in Favorite City List.",
        "color": "blue", "attributes": [], "ends": "\n"},
    {"text": "2. Add new city in Favorite City List.",
        "color": "blue", "attributes": [], "ends": "\n"},
    {"text": "3. Delete city from Favorite City List",
        "color": "blue", "attributes": [], "ends": "\n"},
    {"text": "4. Change Name of Current city in Favorite City List",
        "color": "blue", "attributes": [], "ends": "\n"},
    {"text": "5. Return to Main Menu", "color": "blue",
        "attributes": [], "ends": "\n"},
    {"text": "Enter your choice by typing the number given in front of the choices.",
        "color": "yellow", "attributes": [], "ends": "\n\n"},
]

# Favorite City List Weather Search Operations-------------------------#
favority_city_weather_operations = [
    {"text": "Choose the operation for favorite cities Weather",
        "color": "magenta", "attributes": ["bold"], "ends": "\n"},
    {"text": "1. Weather for specific favorite city.",
        "color": "blue", "attributes": [], "ends": "\n"},
    {"text": "2. Weather for weather for all favorite cities.",
        "color": "blue", "attributes": [], "ends": "\n"},
    {"text": "3. Return to Main Menu.", "color": "blue",
        "attributes": [], "ends": "\n"},
    {"text": "Enter your choice by typing the number given in front of the choices.",
        "color": "yellow", "attributes": [], "ends": "\n\n"},
]

weather_app.print_name()

# Main Loop Section------------------------------#
if __name__ == "__main__":

    while weather_app.start_app:

        for text in menu_items:
            print_text(text['text'], color=text['color'],
                       attributes=text['attributes'], ends=text['ends'])

        weather_app.operation = input("Enter you choice: ")

        if weather_app.operation == "1":
            weather_app.city_name = input("Enter city name: ")
            clear_screen()
            weather_data = weather_app.search_weather()
            print()

            if not weather_app.weather.error and not weather_app.search_city(weather_app.city_name):
                weather_app.current_city_favorite_city()

        elif weather_app.operation == "2":
            clear_screen()

            while True:
                for text in favority_city_operations:
                    print_text(text['text'], color=text['color'],
                               attributes=text['attributes'], ends=text['ends'])

                city_operations = input("Enter you choice: ")

                if city_operations == "1":
                    clear_screen()
                    weather_app.all_city_names()

                elif city_operations == "2":
                    clear_screen()
                    weather_app.all_city_names()
                    print_text(
                        "Enter the name of city.", "yellow", ends="\n\n")
                    new_city = input("Enter city name: ")
                    output = weather_app.add_city_name(new_city)
                    clear_screen()
                    print_text(output, "light_cyan", ["blink"])

                elif city_operations == "3":
                    clear_screen()
                    weather_app.all_city_names()
                    print_text(
                        "Enter your choice by typing the name or number given in front of the choices for removing the city.", "yellow", ends="\n\n")
                    selected_city = input("Enter your choice: ")
                    output = weather_app.delete_city_name(selected_city)
                    clear_screen()
                    print_text(output, "light_cyan", ["blink"])

                elif city_operations == "4":
                    clear_screen()
                    weather_app.all_city_names()
                    favorite_city_name = input(
                        "Type City Name or City Number: ")
                    city_in_cities = weather_app.search_city(
                        favorite_city_name)

                    if not city_in_cities:
                        clear_screen()
                        print_text(
                            "City not found in Favorite City List", "light_red", ends="\n\n")
                        time.sleep(2)
                    else:
                        new_city_name = input("New City Name: ")
                        output = weather_app.update_city_name(new_city_name)
                        clear_screen()
                        print_text(output, "light_cyan", [
                                   "blink"], ends="\n\n")

                elif city_operations == "5":
                    clear_screen()
                    break

                else:
                    print_text("Unsupported Operatin",
                               "light_red", ends="\n\n")
                    clear_screen()

        elif weather_app.operation == "3":
            clear_screen()

            while True:
                for text in favority_city_weather_operations:
                    print_text(text['text'], color=text['color'],
                               attributes=text['attributes'], ends=text['ends'])

                favorite_city_search = input("Enter you choice: ")

                if favorite_city_search == "1":
                    clear_screen()
                    weather_app.all_city_names()
                    favorite_city_name = input(
                        "Type City Name or City Number: ")
                    clear_screen()
                    city_in_cities = weather_app.search_city(
                        favorite_city_name)

                    if not city_in_cities:
                        clear_screen()
                        print_text(
                            "City not found in Favorite City List", "light_red", ends="\n\n")
                        time.sleep(2)
                    else:
                        print_text(f"Weather data for {
                                   weather_app.city_name.title()}", 'yellow')
                        weather_app.search_weather()

                elif favorite_city_search == "2":
                    clear_screen()
                    print_text("Weather data for all cities", 'yellow')
                    weather_app.search_weather_all_cities()

                elif favorite_city_search == "3":
                    clear_screen()
                    break

                else:
                    print_text("Unsupported Operatin",
                               "light_red", ends="\n\n")
                    clear_screen()

        elif weather_app.operation == "4":
            clear_screen()

        elif weather_app.operation == "5":
            weather_app.start_app = False

        else:
            print_text("Unsupported Operatin", "light_red")
            time.sleep(1)
            clear_screen()
