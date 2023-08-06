import requests


class TechZApi:
    class Gogo:
        def __init__(self, API_KEY) -> None:
            self.base = "https://api.techzbots.live"
            self.api_key = API_KEY

        def latest(self, page=1):
            data = requests.get(
                f"{self.base}/gogo/latest?api_key={self.api_key}&page={page}"
            ).json()
            return data["results"]

        def anime(self, anime):
            data = requests.get(
                f"{self.base}/gogo/anime?id={anime}&api_key={self.api_key}"
            ).json()
            return data["results"]

        def search(self, query):
            data = requests.get(
                f"{self.base}/gogo/search/?query={query}&api_key={self.api_key}"
            ).json()
            return data["results"]

        def episode(self, episode):
            data = requests.get(
                f"{self.base}/gogo/episode?id={episode}&api_key={self.api_key}&lang=both"
            ).json()["results"]
            return data

        def stream(self, url):
            url = str(requests.utils.quote(url))
            data = requests.get(
                f"{self.base}/gogo/stream?url={url}&api_key={self.api_key}"
            ).json()
            return data["results"]

    class MkvCinemas:
        def __init__(self, API_KEY) -> None:
            self.base = "https://api.techzbots.live"
            self.api_key = API_KEY

        def add_task(self, url, max=5):
            url = str(requests.utils.quote(url))
            data = requests.get(
                f"{self.base}/mkvcinemas/add_task?api_key={self.api_key}&url={url}&max={max}"
            ).json()
            return data["results"]
