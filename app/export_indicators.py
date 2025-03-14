import requests

i_url = "https://www.wegweiser-kommune.de/data-api/rest/indicator/list?max=100000"
response = requests.get(i_url)
indicators = response.json()
forecast_indicators = []
normal_indicators = []
for i in indicators:
    if i["type"] == "POPULATION_FORECAST" or i["type"] == "CARE_FORECAST" or "prognose" in str(i).lower():
        forecast_indicators.append(i)
    else:
        normal_indicators.append(i)

with open("normal_indicators.txt", "w") as f:
    for n in normal_indicators:
        f.write(n["name"] + "\n")

with open("forecast_indicators.txt", "w") as f:
    for n in forecast_indicators:
        f.write(n["name"] + "\n")
