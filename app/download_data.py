import requests

def download_data(dataset:str, municipality:str, year:str):
    dataset = str(dataset).lower().replace(' ', '-')
    url = f"https://www.wegweiser-kommune.de/data-api/rest/export/{dataset}+{municipality}+{year}+table.csv?charset-UTF-8"

    response = requests.get(url)

    return response.text
