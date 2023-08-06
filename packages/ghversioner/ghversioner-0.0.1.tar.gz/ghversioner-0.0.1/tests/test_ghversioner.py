from unittest import TestCase
import unittest
import src.ghversioner


class TestGitHubUtils(TestCase):

    def setUp(self):
        self.gh = src.ghversioner.GitHubUtils()
        self.gh.releases = [src.ghversioner.ReleaseRecord('v1.8.2', '2022-12-22T13:42:12Z')]

    def test_contains_release_version(self):
        assert self.gh.contains_release_version('v1.8.2') is True
        assert self.gh.contains_release_version('v125215.52.52') is False

    def test_get_release_timestamp(self):
        assert self.gh.get_release_timestamp('v1.8.2421') == 'Cannot determine timestamp'
        assert self.gh.get_release_timestamp('v1.8.2') == '2022-12-22T13:42:12Z'

    def test_calculate_age_in_days(self):
        assert isinstance(self.gh.calculate_age_in_days('2022-12-22T13:42:12Z'), int) is True
        assert self.gh.calculate_age_in_days('2022-12-22T13:42:12Z') > 80


if __name__ == '__main__':
    unittest.main()