import datetime
from dataclasses import dataclass
from typing import Iterable
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup

META_TITLE_SELECTORS = (
    'meta[name="twitter:title"]',
    'meta[property="og:title"]',
    "title",
)
META_DESC_SELECTORS = (
    'meta[name="twitter:description"]',
    'meta[property="og:description"]',
    'meta[name="description"]',
)
META_IMAGE_SELECTORS = (
    'meta[name="twitter:image"]',
    'meta[property="og:image"]',
)
META_TYPE_SELECTORS = ('meta[property="og:type"]',)


@dataclass
class PageMeta:
    """Extract generic website metadata based on a url fetched on a certain date.

    All of the fields, except the date, default to `None`.

    Field | Type | Description
    :--:|:--:|:--
    id | str | Generated id based on the url's path
    etag | str | ETag header on `date` fetched
    netloc | str | URL domain
    path | str | URL path
    title | str | First matching title parsed from `<meta>` CSS selectors (and the `<title>` tag)
    description | str | First matching description Parsed from `<meta>` CSS selectors
    og_img_url | str | An [open graph](https://ogp.me/) (OG) image url detected
    og_type | str | A type detected from OG values
    soup | BeautifulSoup | See bs4 [docs](https://www.crummy.com/software/BeautifulSoup)
    date | str | The date metadata was fetched in ISO Format
    """  # noqa: E501

    url: str
    id: str | None = None
    etag: str | None = None
    netloc: str | None = None
    path: str | None = None
    title: str | None = None
    description: str | None = None
    og_img_url: str | None = None
    og_type: str | None = None
    date: str = datetime.datetime.now().isoformat()
    soup: BeautifulSoup | None = None

    def __post_init__(self):
        parsed = urlparse(self.url)
        r = httpx.get(self.url)
        self.soup = BeautifulSoup(r.content, "html.parser")
        self.id = parsed.path.removeprefix("/").removesuffix("/")
        self.netloc = parsed.netloc
        self.path = parsed.path
        self.etag = r.headers.get("etag")
        self.title = self.select(self.soup, META_TITLE_SELECTORS)
        self.description = self.select(self.soup, META_DESC_SELECTORS)
        self.og_img_url = self.select(self.soup, META_IMAGE_SELECTORS)
        self.og_type = self.select(self.soup, META_TYPE_SELECTORS)

    def __repr__(self) -> str:
        return f"PageMeta: {self.netloc}/{self.path}"

    @classmethod
    def select(
        cls, soup: BeautifulSoup, selectors: Iterable[str]
    ) -> str | None:
        """The order of CSS selectors. The first one
        matched, retrieves the content, if found.

        See present list of selectors used to extract content:

        ```py
        META_TITLE_SELECTORS = (
            'meta[name="twitter:title"]',
            'meta[property="og:title"]',
            "title",
        )
        META_DESC_SELECTORS = (
            'meta[name="twitter:description"]',
            'meta[property="og:description"]',
            'meta[name="description"]',
        )
        META_IMAGE_SELECTORS = (
            'meta[name="twitter:image"]',
            'meta[property="og:image"]',
        )
        META_TYPE_SELECTORS = ('meta[property="og:type"]',)
        ```

        Note the special rule on `title` as a selector.

        Examples:
            >>> from pathlib import Path
            >>> html = Path(__file__).parent.parent / "tests" / "data" / "test.html"
            >>> soup = BeautifulSoup(html.read_text(), "html.parser")
            >>> PageMeta.select(soup, META_TITLE_SELECTORS)
            'Hello World From Twitter Title!'
            >>> PageMeta.select(soup, META_DESC_SELECTORS)
            'this is a description from twitter:desc'

        Args:
            soup (BeautifulSoup): Converted html content into a soup object
            selectors (Iterable[str]): CSS selectors as a tuple

        Returns:
            str | None: If found, return the text value.
        """
        for selector in selectors:
            if selector.startswith("meta"):
                if desc := soup.select(selector):
                    if content := desc[0].get("content"):
                        if content and isinstance(content, str):
                            return content
            elif selector == "title":
                return soup("title")[0].get_text()
        return None
