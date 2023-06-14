# link-this

A small web service that provides a simple way to create links to specific information on web pages.

It supports:
* XPath to extract a specific element of a web page.
* Both GET and POST requests, i.e. if a web service you want to link to send data as POST,
using this service you can generate unique links as if the service was using GET.
* In theory, the URLs are persistent, in a sense that if the URL of the web service you provide links to changes,
or if the XPath to the element changes, change the config and the URL will stay the same.

## Installation

Basic deployment (not recommended for production)
```
pip install -r requirements.py
python linker.py
```

For advanced options on how to deploy,
please refer to the [Flask documentation](https://flask.palletsprojects.com/en/latest/deploying/).

## Setting up the list of services

The list of services is provided in `services.json`.
Each entry has a key which will be a part of the URL.
Possible keys in the entry are:
* `url`: mandatory. The base URL of the service for requests.
* `xpath`: XPath expression that leads to the specific portion of the web page which contains the part you want to link to. If omitted, the full response is returned.
* `method`: `GET` or `POST`
* `params`: a list of names that will be used (in order) as argument names for the request.
