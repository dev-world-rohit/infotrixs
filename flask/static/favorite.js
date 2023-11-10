// Function to set cookie
function setCookie(name, value, days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

// Function to get cookie value by name
function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(";");
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == " ") c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

// Function to delete cookie by name
function eraseCookie(name) {
    document.cookie = name + "=; Max-Age=-99999999;";
}

// Function to add city to the list
function addCity() {
    var cityName = document.getElementById("cityName").value;
    if (cityName) {
        var citiesList = getCityList();

        if (citiesList.includes(cityName)) {
            alert(cityName + " already exists in the list!");
        } else {
            citiesList.push(cityName);
            updateCityList(citiesList);
            setCookie("favoriteCities", JSON.stringify(citiesList), 7);
            clearInputFields();
        }
    }
}

// Function to modify city name
function modifyCity() {
    var newCityNameInput = document.getElementById("newCityName");
    var newCityAddButton = document.getElementById("update-button");
    newCityNameInput.style.display = "block";
    newCityAddButton.style.display = "block";
    clearInputFields();
}

// Function to update city name
function updateCity() {
    var cityName = document.getElementById("cityName").value;
    var newCityName = document.getElementById("newCityName").value;
    if (cityName && newCityName) {
        var citiesList = getCityList();
        var index = citiesList.indexOf(cityName);
        if (index !== -1) {
            citiesList[index] = newCityName;
            updateCityList(citiesList);
            setCookie("favoriteCities", JSON.stringify(citiesList), 7);
            clearInputFields();
            // Hide the newCityName input after updating
            document.getElementById("newCityName").style.display = "none";
            document.getElementById("update-button").style.display = "none";
        }
    }
}

// Function to delete city from the list
function deleteCity() {
    var cityName = document.getElementById("cityName").value;
    if (cityName) {
        var citiesList = getCityList();
        var index = citiesList.indexOf(cityName);
        if (index !== -1) {
            citiesList.splice(index, 1);
            updateCityList(citiesList);
            setCookie("favoriteCities", JSON.stringify(citiesList), 7);
        }
        else {
            alert(cityName + " does not exist in the list.")
        } 
        clearInputFields();
    }
}

// Function to get the current city list from cookie
function getCityList() {
    var citiesListCookie = getCookie("favoriteCities");
    return citiesListCookie ? JSON.parse(citiesListCookie) : [];
}

// Function to update the city list in the UI
function updateCityList(citiesList) {
    var citiesListElement = document.getElementById("cities-list");
    citiesListElement.innerHTML = "";
    citiesList.forEach(function (city) {
        var li = document.createElement("li");
        li.textContent = city;
        citiesListElement.appendChild(li);
    });
}

// Function to clear input fields
function clearInputFields() {
    document.getElementById("cityName").value = "";
    document.getElementById("newCityName").value = "";
}

// Load and display the city list on page load
window.onload = function () {
    var citiesList = getCityList();
    updateCityList(citiesList);
};
