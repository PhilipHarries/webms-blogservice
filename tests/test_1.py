# import pytest
import requests

localport = 5434


def test_get_blogs():
    r = requests.get("http://localhost:{}/blog/api/v1.0/blogs".format(localport))
    assert r.status_code == 200
    assert "blogs" in r.json()
    assert len(r.json()["blogs"]) > 0
    assert "author" in r.json()["blogs"][0]
    assert "title" in r.json()["blogs"][0]
    assert "id" in r.json()["blogs"][0]
    assert "description" in r.json()["blogs"][0]
    assert "content" in r.json()["blogs"][0]
    assert "tags" in r.json()["blogs"][0]
    assert "last-update" in r.json()["blogs"][0]
    assert "created-date" in r.json()["blogs"][0]


def test_post_and_get_and_update_and_delete_blog():
    payload = {
        "description": "desc",
        "title": "title",
        "author": "author",
        "content": "content",
        "id": "test_post_blog",
        "tags": "test"
        }
    r = requests.post("http://localhost:{}/blog/api/v1.0/blogs".format(localport), json=payload)
    assert r.status_code == 201
    assert r.json()["blog"]["description"] == "desc"
    assert r.json()["blog"]["author"] == "author"
    assert r.json()["blog"]["content"] == "content"
    assert r.json()["blog"]["id"] == "test_post_blog"
    assert r.json()["blog"]["tags"] == "test"
    assert r.json()["blog"]["title"] == "title"
    assert "created-date" in r.json()["blog"]
    assert "last-update" in r.json()["blog"]
    assert "uri" in r.json()["blog"]
    r = requests.get("http://localhost:{}/blog/api/v1.0/blog/test_post_blog".format(localport))
    assert r.status_code == 200
    assert r.json()["blog"]["description"] == "desc"
    assert r.json()["blog"]["author"] == "author"
    assert r.json()["blog"]["content"] == "content"
    assert r.json()["blog"]["id"] == "test_post_blog"
    assert r.json()["blog"]["tags"] == "test"
    assert r.json()["blog"]["title"] == "title"
    assert "created-date" in r.json()["blog"]
    assert "last-update" in r.json()["blog"]
    assert "uri" in r.json()["blog"]
    payload = {
        "description": "desc",
        "title": "title",
        "author": "author",
        "content": "new content",
        "id": "test_post_blog",
        "tags": "test"
        }
    r = requests.put("http://localhost:{}/blog/api/v1.0/blog/test_post_blog".format(localport), json=payload)
    assert r.status_code == 200
    r = requests.get("http://localhost:{}/blog/api/v1.0/blog/test_post_blog".format(localport))
    assert r.status_code == 200
    assert r.json()["blog"]["content"] == "new content"
    r = requests.delete("http://localhost:{}/blog/api/v1.0/blog/test_post_blog".format(localport))
    assert r.status_code == 200
    r = requests.get("http://localhost:{}/blog/api/v1.0/blog/test_post_blog".format(localport))
    assert r.status_code == 404
