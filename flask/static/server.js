document.addEventListener("DOMContentLoaded", function () {
    // Variable declarations
    let search_data = false;

    // Event listener for the submit button
    document
        .getElementById("submit-button")
        .addEventListener("click", function (event) {
            document.querySelector(".loader").style.display = "block";
            event.preventDefault();
            getTheData();
        });

    // Function to get data based on user input
    function getTheData() {
        var city = document.getElementById("city-input-search").value;
        if (city !== "") {
            search_data = true;
            getWeatherData(city);
        }
    }

    // Function to make an AJAX request to the server and update weather data
    function getWeatherData(city) {
        fetch("/get_weather_data?city=" + encodeURIComponent(city), {
            method: "GET",
        })
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Network response was not ok");
                    document.querySelector(".loader").style.display = "none";
                }
                return response.json();
            })
            .then((data) => {
                document.querySelector(".sub-result-div").style.display =
                    "block";
                document.querySelector(".loader").style.display = "none";
                // Update the weather data on the client side
                document.querySelector(".weather-icon").textContent = data.icon;
                document.querySelector(".city-div").textContent = data.city;
                document.querySelector(".description-div").textContent =
                    data.des;
                document.querySelector(".weather-temp").textContent = data.temp;
            })
            .catch((error) =>
                console.error("Error fetching weather data:", error)
            );
    }

    // Initial call to get weather data
    if (search_data) {
        // Set up interval to update weather data every 30 seconds
        setInterval(function () {
            // Get the city value from the input field
            var city = document.getElementById("city-input-search").value;
            getWeatherData(city);
        }, 30000); // Adjusted interval to 30 seconds
    }
});
