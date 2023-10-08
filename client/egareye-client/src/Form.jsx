import React from "react";
import { useState, useEffect } from "react";

const Form = () => {

    const [upcomingMovies, setUpcomingMovies] = useState([]);
    const cities = ["hyderabad", "chennai"]

    const [name, setName] = useState("");
    const [countryCode, setCountryCode] = useState("");
    const [phoneNumber, setPhoneNumber] = useState("");
    const [selectedMovie, setSelectedMovie] = useState("");
    const [selectedCity, setSelectedCity] = useState("hyderabad");
    const [submittedText, setSubmittedText] = useState("")
    // const [frequency, setFrequency] = useState("");

    const handleNameChange = (event) => {
        setName(event.target.value);
    };

    const handleCountryCode = (event) => {
        setCountryCode(event.target.value);
    };

    const handlePhoneNumberChange = (event) => {
        setPhoneNumber(event.target.value);
    };

    const handleMovieChange = (event) => {
        setSelectedMovie(event.target.value);
    };

    const handleCityChange = (event) => {
        setSelectedCity(event.target.value);
    };

    // const handleFrequencyChange = (event) => {
    //     setFrequency(event.target.value);
    // };

    const handleSubmit = async (event) => {
        event.preventDefault();
        if (!(name && countryCode && phoneNumber && selectedMovie && selectedCity)) return
        console.log(`${name} ${countryCode + phoneNumber} ${selectedMovie} ${selectedCity}`)
        try {
            const response = await fetch("http://127.0.0.1:8000/monitor", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    name: name,
                    phoneNumber: countryCode+phoneNumber,
                    movie: selectedMovie,
                    city: selectedCity,
                    // frequency: frequency,
                }),
            });

            if (response.ok) {
                console.log("Data submitted successfully!");
                setSubmittedText(`${phoneNumber} notification for ${selectedMovie} at ${selectedCity} setup`);
                setName("");
                setPhoneNumber("");
                setSelectedMovie("");
                // setFrequency("");
            } else {
                console.error("Failed to submit data");
            }
        } catch (error) {
            console.error("Error submitting data:", error);
        }
    };

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch("http://127.0.0.1:8000/allmovies/"+selectedCity);
                if (response.ok) {
                    const data = await response.json();
                    setUpcomingMovies(data["all_movies"]); 
                } else {
                    console.error("Failed to fetch data");
                }
            } catch (error) {
                console.error("Error fetching data:", error);
            }
        };
        fetchData();
    }, [selectedCity]);


    return (
        <div className="container mx-auto mt-32 border border-2 border-black pb-32 bg-gray-300">
            <div className="flex text-4xl font-extrabold justify-center items-center p-5 my-5">
                <h1>
                    Egareye
                </h1>
            </div>
      <form className="max-w-lg mx-auto bg-white p-8 shadow-lg rounded-lg" onSubmit={handleSubmit}>
        <div className="mb-4">
          <label htmlFor="name" className="block text-gray-700 text-sm font-bold mb-2">
            Name:
          </label>
          <input
            type="text"
            id="name"
            name="name"
            className="border border-gray-300 p-2 rounded w-full"
            placeholder="Enter your name"
            onChange={handleNameChange}
          />
        </div>
        <div className="mb-4">
          <label htmlFor="phoneNumber" className="block text-gray-700 text-sm font-bold mb-2">
            Phone Number:
          </label>
          <div className="flex items-center">
            <select className="border border-gray-300 p-2 rounded mr-2" onChange={handleCountryCode}>
              <option value="+1">+1</option>
              <option value="+91">+91</option>
            </select>
            <input
              type="tel"
              id="phoneNumber"
              name="phoneNumber"
              className="border border-gray-300 p-2 rounded w-full"
              placeholder="Enter your phone number"
              onChange={handlePhoneNumberChange}
            />
          </div>
              </div>
                  <div className="mb-4">
          <label htmlFor="city" className="block text-gray-700 text-sm font-bold mb-2">
            Select City:
          </label>
            <select id="city" name="city" className="border border-gray-300 p-2 rounded w-full" onChange={handleCityChange}>
                <option value="">Select a city</option>
                {cities.map((city, index) => (
                    <option key={index} value={city}>
                        {city}
                    </option>
                ))}
          </select>
        </div>
        <div className="mb-4">
          <label htmlFor="movie" className="block text-gray-700 text-sm font-bold mb-2">
            Select Movie:
          </label>
            <select id="movie" name="movie" className="border border-gray-300 p-2 rounded w-full" onChange={handleMovieChange}>
                <option value="">Select a movie</option>
                {upcomingMovies.map((movie, index) => (
                    <option key={index} value={movie}>
                        {movie}
                    </option>
                ))}
          </select>
        </div>
        
        {/* <div className="mb-4">
          <label htmlFor="frequency" className="block text-gray-700 text-sm font-bold mb-2">
            Select Frequency:
          </label>
          <input
            type="number"
            id="frequency"
            name="frequency"
            className="border border-gray-300 p-2 rounded w-full"
            placeholder="Enter frequency"
            min="1"
            onChange={handleFrequencyChange}
          />
        </div> */}
        <button type="submit" className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
          Submit
          </button>
          <div className="text-green-700">
            {submittedText && submittedText}
          </div>
      </form>
    </div>
  );
};

export default Form;
