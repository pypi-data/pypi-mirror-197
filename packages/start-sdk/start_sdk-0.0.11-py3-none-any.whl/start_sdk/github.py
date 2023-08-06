import httpx
from pydantic import BaseSettings, Field

BASE = "https://api.github.com/repos"
OG = "https://opengraph.githubassets.com"


class Github(BaseSettings):
    """
    # Github API v2022-11-28

    Add secrets to .env file:

    Field in .env | Github Credentials | Where credential found
    :--|:--:|:--
    `GH_TOKEN` | Github Personal Access Token | Ensure _fine-grained_ Personal Access Token [Github Developer Settings](https://github.com/settings/tokens?type=beta) can access the repository represented in the url.
    `GH_TOKEN_VERSION` | Default: `2022-11-28` | See [docs](https://docs.github.com/en/rest/repos/contents?apiVersion=2022-11-28)
    """  # noqa: E501

    token: str = Field(
        default=...,
        repr=False,
        env="GH_TOKEN",
    )
    version: str = Field(
        default="2022-11-28",
        repr=False,
        env="GH_TOKEN_VERSION",
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def get(
        self,
        url: str,
        media_type: str | None = ".raw",
        params: dict = {},
    ) -> httpx.Response:
        """See requisite [headers](https://docs.github.com/en/rest/repos/contents?apiVersion=2022-11-28#get-repository-content--code-samples)

        Args:
            url (str): _description_
            media_type (str | None, optional): _description_. Defaults to ".raw".
            params (dict, optional): _description_. Defaults to {}.

        Returns:
            httpx.Response: _description_
        """  # noqa: E501
        with httpx.Client(timeout=120) as client:
            return client.get(
                url,
                params=params,
                headers={
                    "Accept": f"application/vnd.github{media_type}",
                    "Authorization": f"token {self.token}",
                    "X-GitHub-Api-Version": self.version,
                },
            )

    def get_repo(self, author: str, repo: str) -> httpx.Response:
        """See Github API [docs](https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#get-a-repository)"""  # noqa: E501
        return self.get(f"{BASE}/{author}/{repo}")

    def get_repo_commits(self, author: str, repo: str) -> httpx.Response:
        """See Github API [docs](https://docs.github.com/en/rest/commits/commits?apiVersion=2022-11-28)"""  # noqa: E501
        return self.get(f"{BASE}/{author}/{repo}/commits")

    def get_latest_sha(self, author: str, repo: str) -> str:
        """See Github API [docs](https://docs.github.com/en/rest/commits/commits?apiVersion=2022-11-28#get-a-commit)"""  # noqa: E501
        commits_response = self.get_repo_commits(author, repo)
        return commits_response.json()[0]["sha"]

    def get_latest_og_img_url(self, author: str, repo: str) -> str:
        """See [Stackoverflow](https://stackoverflow.com/a/71454181)"""
        return f"{OG}/{self.get_latest_sha(author, repo)}/{author}/{repo}"
