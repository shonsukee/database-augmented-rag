"""Fetch REST API specification pages and store them in the databases."""
import logging
import re
from typing import List, Optional, Tuple

import html2text
import requests
from bs4 import BeautifulSoup, Tag
from llama_index.core import Document
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from rag.store.pinecone_index import PineconeIndex

# Both GitHub (SwitchBot README) and the Fitbit developer reference put the
# specification body in an <article> element.
BODY_TAG = "article"


def fetch_body(url: str) -> Optional[Tag]:
    """Return the <article> element of a specification page, or None."""
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    body = soup.find(BODY_TAG)
    if isinstance(body, Tag):
        return body

    # Pages rendered by JavaScript have no <article> in the raw HTML.
    logging.warning("%s: <%s> not found in the raw HTML, retrying with a browser", url, BODY_TAG)
    html = fetch_body_with_browser(url)
    return BeautifulSoup(html, "html.parser") if html else None


def fetch_body_with_browser(url: str) -> str:
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        return driver.find_element(By.TAG_NAME, BODY_TAG).get_attribute("innerHTML") or ""
    except Exception as error:
        logging.warning("%s: could not extract with a browser: %s", url, error)
        return ""
    finally:
        driver.quit()


def to_markdown(body: Tag) -> str:
    converter = html2text.HTML2Text()
    converter.ignore_links = False
    text = converter.handle(str(body))
    while " \n" in text:
        text = re.sub(r" \n", "\n", text)
    return re.sub(r"\n\n", "\n", text).strip()


def split_code_and_text(body: Tag) -> Tuple[List[str], str]:
    """Take the <pre> blocks out of a page as code snippets; the rest is natural-language text."""
    snippets = []
    for pre in body.find_all("pre"):
        snippets.append(pre.get_text())
        pre.extract()
    return snippets, to_markdown(body)


def store_whole(service: str, urls: List[str], index_name: str) -> None:
    """Store each page as one document (configurations D, L, DL, DLm)."""
    pages = []
    for url in urls:
        body = fetch_body(url)
        if body is None:
            logging.error("%s: skipped", url)
            continue
        pages.append(to_markdown(body))
    PineconeIndex(service).store([Document(text=page) for page in pages], index_name)


def store_separated(service: str, urls: List[str], version: str) -> None:
    """Store code snippets and natural-language text in separate databases (the `s`, `c`, `t` configurations)."""
    snippets: List[str] = []
    texts: List[str] = []
    for url in urls:
        body = fetch_body(url)
        if body is None:
            logging.error("%s: skipped", url)
            continue
        page_snippets, text = split_code_and_text(body)
        snippets.extend(page_snippets)
        texts.append(text)

    index = PineconeIndex(service)
    index.store([Document(text=text) for text in texts], f"{version}-natural-language")
    index.store([Document(text=snippet) for snippet in snippets], f"{version}-code")
