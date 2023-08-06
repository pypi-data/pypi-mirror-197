from datetime import timedelta

import requests
from bs4 import BeautifulSoup
import datetime


class GitHubUtils:

    def __init__(self, releases=None, url=None, pages=1):
        if releases is None:
            releases = []
        self.releases = releases
        if url is not None:
            for page in range(1, pages):
                self.get_github_release_page(f'{url}?page={page}')

    def get_github_release_page(self, url):
        response = requests.get(url=url)
        html = response.text
        soup = BeautifulSoup(html, features="html.parser")
        sections = soup.find_all("section")

        for section in sections:
            release_version = section.find("h2").text
            release_timestamp = section.find("relative-time").get("datetime")
            self.releases.append(ReleaseRecord(release_version, release_timestamp))

    def __str__(self) -> str:
        return f"releases: {[str(r) for r in self.releases]}"

    def contains_release_version(self, version) -> bool:
        release_version_list = [r.release_version for r in self.releases]
        if version in release_version_list:
            return True
        else:
            return False

    def get_release_timestamp(self, version) -> str:
        if self.contains_release_version(version):
            for release in self.releases:
                if version in release.release_version:
                    return release.release_timestamp
        else:
            return "Cannot determine timestamp"

    def calculate_age_in_days(self, timestamp) -> int:
        age = datetime.datetime.now() - datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
        return age.days


class ReleaseRecord:
    def __init__(self, release_version, release_timestamp):
        self.release_version = release_version
        self.release_timestamp = release_timestamp

    def __str__(self) -> str:
        return f"release_version: {self.release_version}, release_timestamp: {self.release_timestamp}"







