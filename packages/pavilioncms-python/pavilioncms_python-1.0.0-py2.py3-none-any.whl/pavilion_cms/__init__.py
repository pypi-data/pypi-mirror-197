"""Top-level package for PavilionCMS ."""

from pavilion_cms.category import Category
from pavilion_cms.tag import Tags
from pavilion_cms.posts import Posts

# from pavilion_cms.client import PavilionCMS  # noqa: F401

__author__ = """Oluwole Majiyagbe"""
__email__ = "info@firstpavitech.com"


class PavilionCMS:
    def __init__(self, read_token: str) -> None:
        self.tags = Tags(read_token)
        self.category = Category(read_token)
        self.posts = Posts(read_token)
