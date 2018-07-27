# Table of contents

* [Description](#Description)
* [Request and response details](#Request-and-response-details)
  * [JSON Format](#JSON-Format)
  * [CSV Format](#CSV-Format)
* [Service configuration](#Service-configuration)
  * [Deployment](#Deployment)
* [Examples](#Examples)

## Description

pip install -b python3 -t src/lib/IP2Location IP2Location

IP2Location is used to get location by IP.

Datastore is [ip2location](https://lite.ip2location.com/database/ip-country-region-city) binary DB file.

Service is running in AWS Lambda and receiving requests via AWS API Gateway.

AWS API Gateway allows HTTPS only requests.

IP2Location service can provide JSON and CSV responses.

Service accepts only GET request with query strings.

[IP2Location Python lib](https://github.com/ip2location/IP2Location-Python) was used

## Request and response details

### JSON Format

Query strings:

* `ip` - Any IPv4 address
* `format` - json

Fields returned:

* `city_name`
* `country_code`
* `country_name`
* `region_name`

### CSV Format

Query strings:

* `ip` - Any IPv4 address
* `format` - csv

Value order:

1. `country_code`
2. `country_name`
3. `region_name`
4. `city_name`

## Service configuration

IP2Location is configured via environment variables.

**Next environment variables are required:**

* `DEBUG` - set debug mode. In debug additional logging applied
* `DB_FILE` - ip2location binary file path related to main func file
* `CSV_DELIMITER` - Delimiter used for CSV format

For service to operate [ip2location](https://lite.ip2location.com/database/ip-country-region-city) DB file must be present in `src/db`.

## Deployment

_Python version 3.6+ tested only_

1. Create AWS Lambda with IAM User that have CloudWatch write permissions.
2. Set AWS Lambda environment variables ([Service configuration](#Service-configuration))

    Recommended AWS Lambda resource limits:
    * memory_size - 128 mb
    * timeout - 2 seconds

3. Create AWS API Gateway with only root resource.
4. Create `GET` method AWS API Gateway console with AWS Lambda integration request.
5. Set up propper AWS Lambda permissions to allow API Gateway invocations.
6. Test with examples provided in [Examples](#Examples)

## Examples

Sample JSON request:

```uri
https://example.com/somepath/?ip=113.53.111.32&format=json
```

Sample JSON response:

```json
{
  "city_name": "Ko Samui",
  "country_code": "TH",
  "country_name": "Thailand",
  "region_name": "Surat Thani"
}
```

Sample JSON request:

```uri
https://example.com/somepath/?ip=113.53.111.32&format=csv
```

Sample JSON response:

```csv
TH;Thailand;Surat Thani;Ko Samui
```

## Local testing

```shell
# source env_local
# cd src/
# python3 main.py
```