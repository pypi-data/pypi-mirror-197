# pftel-client
A client library for accessing a `pftel` telemetry server, typically in the context of ChRIS workflow execution. Most use cases are POSTing log information to the remote server.

## Usage
First, create a client:

```python
from pftel_client import Client

client = Client(base_url="http//your.telemetry.server:22223")
```

Import the models:

```python
from pftel_client.models import log_structured, log_response
from pftel_client.api.logger_services import log_write_api_v1_log_post as plog
from pftel_client.types import Response
```

Create an object with the data to log:

```python
d_post:log_structured   = log_structured.LogStructured()
d_post.log_object       = 'ChRIS_LegMeasurements'
d_post.log_collection   = 'run-20230505.1630'
d_post.log_event        = 'inference'
d_post.app_name         = 'pl-lld_inference'
d_post.exec_time        = 9.4532
d_post.payload          = ''
```

And POST this log to the server:

```python
reply:log_response = plog.sync(client = client, json_body = d_post)
# or if you need more info (e.g. status_code)
reply: Response[log_response] = plog.sync.detailed(client = client, json_body = d_post)
```

Or do the same thing with an async version:

```shell
reply:log_response = await plog.asyncio(client = client, json_body = d_post)
# or if you need more info (e.g. status_code)
reply: Response[log_response] = await plog.asyncio.detailed(client = client, json_body = d_post)
```

By default, when you're calling an HTTPS API it will attempt to verify that SSL is working correctly. Using certificate verification is highly recommended most of the time, but sometimes you may need to authenticate to a server (especially an internal server) using a custom certificate bundle.

```python
client = AuthenticatedClient(
    base_url="https://internal_api.example.com",
    token="SuperSecretToken",
    verify_ssl="/path/to/certificate_bundle.pem",
)
```

You can also disable certificate validation altogether, but beware that **this is a security risk**.

```python
client = AuthenticatedClient(
    base_url="https://internal_api.example.com",
    token="SuperSecretToken",
    verify_ssl=False
)
```

There are more settings on the generated `Client` class which let you control more runtime behavior, check out the docstring on that class for more info.

Things to know:
1. Every path/method combo becomes a Python module with four functions:
    1. `sync`: Blocking request that returns parsed data (if successful) or `None`
    1. `sync_detailed`: Blocking request that always returns a `Request`, optionally with `parsed` set if the request was successful.
    1. `asyncio`: Like `sync` but async instead of blocking
    1. `asyncio_detailed`: Like `sync_detailed` but async instead of blocking

1. All path/query params, and bodies become method arguments.
1. If your endpoint had any tags on it, the first tag will be used as a module name for the function (my_tag above)
1. Any endpoint which did not have a tag will be in `pftel_client.api.default`

## Building / publishing this Client
This project uses [Poetry](https://python-poetry.org/) to manage dependencies  and packaging.  Here are the basics:
1. Update the metadata in pyproject.toml (e.g. authors, version)
1. If you're using a private repository, configure it with Poetry
    1. `poetry config repositories.<your-repository-name> <url-to-your-repository>`
    1. `poetry config http-basic.<your-repository-name> <username> <password>`
1. Publish the client with `poetry publish --build -r <your-repository-name>` or, if for public PyPI, just `poetry publish --build`

If you want to install this client into another project without publishing it (e.g. for development) then:
1. If that project **is using Poetry**, you can simply do `poetry add <path-to-this-client>` from that project
1. If that project is not using Poetry:
    1. Build a wheel with `poetry build -f wheel`
    1. Install that wheel from the other project `pip install <path-to-wheel>`
