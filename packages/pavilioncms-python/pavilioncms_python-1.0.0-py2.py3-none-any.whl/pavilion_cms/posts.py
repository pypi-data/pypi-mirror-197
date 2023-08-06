from pavilion_cms.client import Client


class Posts(Client):
    def __init__(self, read_token):
        super().__init__(read_token)

    def all(self, params: dict = None) -> dict:
        url_path = f"{self.post_url}/all/"
        return self._make_list_request(url_path=url_path, params=params)

    def get(self, post_id, slug) -> dict:
        url_path = f"{self.post_url}/{post_id}/{slug}/view/"
        return self._make_single_request(url_path=url_path)

    def next(self, url_path) -> dict:
        return self._make_list_request(url_path=url_path)

    def previous(self, url_path) -> dict:
        return self._make_list_request(url_path=url_path)
