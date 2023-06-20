from pyowm import OWM

my_owm_secret = 'f70b2868746d0a1f0c27740e7031549a'
owm = OWM(my_owm_secret)
mgr = owm.weather_manager()


def get_weather(place):
    try:
        # Search for current weather in London (Great Britain) and get details
        observation = mgr.weather_at_place(place)
        w = observation.weather
        temp = w.temperature('celsius')["temp"]

        answer = "In " + place + ": "
        answer += str(temp)
        answer += "C " + w.detailed_status
        return answer
    except Exception:
        return 'Location is not defined. Write the name of the city...'
