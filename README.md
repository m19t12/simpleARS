# simple - API Response Search

A simple solution for extracting fields from an API Response in Json format.

## Prerequisites

* [Requests: HTTP for Humans](http://docs.python-requests.org/en/master/) - For the get requests

## Examples

```python
from simpleARS import core

search = {'from': ['select_1', 'select_2', {'sub_from': ['sub_select_1', 'sub_select_2']}]}
retrieved_data = core.retrieve_data('https://test-url.api.com/endpoint', search, 'csv')
```
