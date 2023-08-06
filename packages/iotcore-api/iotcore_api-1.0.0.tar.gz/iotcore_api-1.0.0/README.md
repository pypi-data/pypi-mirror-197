# IoTCoreAPI

Class to interact with IoT Core API. Reference (Docs) is still _WIP_

# Table Of Contents

1. [Installation](#installation)
2. [Use](#Use)
3. [Explanation](#explanation)

# Installation

This library requieres Python 3.8 or higher. 
IoTCore API can be installed with ```pip```. Dependencies will be installed along with the library.

**PIP**

```bash
pip install iotcore-api
```

# Use

In this section we will cover basic usage of the methods.

First, import IoTCoreAPI class from module

```python
from iotcoreapi import IoTCoreAPI
```

To keep it simple, start
by initializing IoTCoreAPI class

```
API_Host = '[base-url]'
API_Port = 56000
token = 'xxxxxxxxxxxxxxxxx'
version = 'v3'
logger = [logging.Logger object. Can be None or ignored]

iot_api = IoTCoreAPI(API_Host, API_Port, token, version, logger)
```

Ask about base endpoint url and token to your provider. API Port will be (almost) always 56000.
Logger support is enabled in this class, so if a logger object is provided, will print out information
to the loggerfile.

Output format can be specified for most of catalogue and reading methods.

Basic usages of this library cover three types of methods:
- Catalogue: methods related to schema information in the IoTCore (tag info, documents, alarms...)
- Reading operations: read real time or historic data from tags. Obtain alarm status
- Write operations: insert data into real time or historic. Also edit alarm information
- Operation: write directly into PLC tags

Once the class is created methods will be accesible from it. Let's start reading catalogue info.
We will ask for all the tags available in the token

```python
tags = iot_api.catalogue_tags()
```

Information will be retrieved in dataframe format. If json is prefered, can be specified
in the "output_format" parameter. Let's read again tags in the token, but this time, we will filter the result
by tag names and driver and specify json format.

```python
driver = ['Test']
names = 'api_test'
tags_filtered = iot_api.catalogue_tags(drivers=drivers, tags=names, output_format='json')
```

One of the most basic usages of the library is to retrieve data from historic. For example, to read a day data from a tagview:
```python
import datetime

UID_TAGVIEW = 'xxxxxxxxxxxx'

end_ts = datetime.now()
start_ts = end_ts - datetime.timedelta(days=1)


data = iotcore_api.read_tagview_historic(UID_TAGVIEW, end_ts, start_ts)
```

It is also possible filter data by tag uid or even use text filters by using corresponding methods:
```python
import datetime

UID_TAGVIEW = 'xxxxxxxxxxxx'
filters_txt = ['Random_Int1', 'Random_Int2']

end_ts = datetime.now()
start_ts = end_ts - datetime.timedelta(days=1)


data = iotcore_api.read_tagview_historic_text_filters(UID_TAGVIEW, end_ts, start_ts, filters_txt)
```

To write data into the IoT Core use the corresponding writing methods. Tags must exist before trying to insert data.

To create a tag with writing permissions, use this method:

```python
tags_to_create = ['api_test', 'api_test20', 'api_test33', 'api_test']
iotcore_api.write_tags_insert(tags_to_create)
```

For writing data operations, a dataframe must be passed.
Dataframe must have the following columns:
- timeStamp: time data
- name: name of the tag
- value: value (int or float)

```python
import pandas as pd

test_df = pd.DataFrame([{'timeStamp': time.time(), 'name': 'api_test', 'value': 1},
                        {'timeStamp': time.time(), 'name': 'api_test_20', 'value': 1}])
data = iotcore_api.write_tags_historic_insert(test_df)
```

Some recommendations to use reading methods:
- Time data can be passed in datetime or unix format
- Usually uid tagview is required. This can be read by using catalogue methods
- Tag filtering by uid is faster than text filters. Text filters methods call uid methods before to retrieve tag name data.

See Docs (_WIP_) for more information

# Explanation

This library was created to simplify the use of the available GET and POST methods available in the IoTCore API.
To understand better the intention behind this library, ask about API reference to your provider.

Instead of dealing with complex and repetitive requests, all functions are written inside IoTCoreAPI class,
allowing easier use and avoiding code repetition.

For example, to set up a basic request to get all tags available in the token, you should:
```python
import requests

#1. Configure specific endpoint for this request
endpoint = 'iotcoreurl:PORT/api/Tags'
#2. Provide token and version in the headers
headers = {'token': 'xxxxxx', 'version': '3.0'}
#3. Parameter data
parameters = {'IncludeAttributes': True}

# Set up request using requests library
response = requests.get(endpoint, params=parameters, headers=headers)

# Deal with request format
data = response.json()
```

This is required for each one of the endpoints listed in the API. Instead, you could use this library as follows:
```python
API_Host = '[base-url]'
API_Port = 56000
token = 'xxxxxxxxxxxxxxxxx'
version = 'v3'

iot_api = IoTCoreAPI(API_Host, API_Port, token, version)

tags = iot_api.catalogue_tags(include_attributes=True)
```

