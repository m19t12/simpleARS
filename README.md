# simple - API Response Search
[![Build Status](https://travis-ci.org/m19t12/simpleARS.svg?branch=master)](https://travis-ci.org/m19t12/simpleARS)
[![Coverage Status](https://coveralls.io/repos/github/m19t12/simpleARS/badge.svg?branch=master)](https://coveralls.io/github/m19t12/simpleARS?branch=master)

A simple solution for extracting fields from an API Response in Json format.

## Prerequisites

* [Requests: HTTP for Humans](http://docs.python-requests.org/en/master/) - For the get requests

## Examples

```python
from simpleARS import core

search = {'from': ['select_1', 'select_2', {'sub_from': ['sub_select_1', 'sub_select_2']}]}
retrieved_data = core.retrieve_data('https://test-url.api.com/endpoint', search, {"username":"user", "password":"pass"}, 'csv', "test_file")
```
