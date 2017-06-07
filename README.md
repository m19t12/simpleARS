# simple - API Response Search
[![Build Status](https://travis-ci.org/m19t12/simpleARS.svg?branch=master)](https://travis-ci.org/m19t12/simpleARS)
[![Coverage Status](https://coveralls.io/repos/github/m19t12/simpleARS/badge.svg?branch=master)](https://coveralls.io/github/m19t12/simpleARS?branch=master)

A simple solution for extracting fields from an API Response in Json format.

## Examples
###### Example 1
Data response from endpoint
```json
{
  "from": {
    "select_1": "value_1",
    "select_2": "value_2",
    "select_3": "value_3",
    "select_4": "value_4",
    "sub_from_1": [
      {
        "sub_select_1": "sub_value_1",
        "sub_select_2": "sub_value_2",
        "sub_select_3": "sub_value_3",
        "sub_select_4": "sub_value_4"
      }
    ],
    "sub_from_2": [
      {
        "sub_select_1": "sub_value_1",
        "sub_select_2": "sub_value_2",
        "sub_select_3": "sub_value_3",
        "sub_select_4": "sub_value_4"
      }
    ]
  }
}
```

```python
from simple_ars import core

search = {'from': ['select_1', 'select_2', {'sub_from_1': ['sub_select_1', 'sub_select_2']}]}
retrieved_data = core.ars(api_response, search)

```
Data extracted after search
```json
{
  "select_1": "value_1",
  "select_2": "value_2",
  "sub_from_1": [
    {
      "sub_select_1": "sub_value_1",
      "sub_select_2": "sub_value_2"
    }
  ]
}
```