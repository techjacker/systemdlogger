# systemdlogger

- Exports systemd logs to an external service, eg cloudwatch, elasticsearch.
- Use with a cron job.
- Python 3+


-----------------------------------------------------------
## Installation

#### Install Dependencies
[python-systemd](https://github.com/systemd/python-systemd)
```
# Fedora/RHEL/CentOS
dnf install python-systemd python3-systemd
```
OR
```
# Debian/Ubuntu/Mint
apt-get install python-systemd python3-systemd
```


#### Install from pip
```pip install systemdlogger```

-----------------------------------------------------------
## Usage

```Shell
systemdlogger config.json
```

#### Recommended Usage - Cron Job Runing Every Minute

```*/1 * * * * . /etc/webserver.env; systemdlogger config.json >/logs/systemdlogger.log 2>&1```


-----------------------------------------------------------
## Config

[Full example config](tests/fixtures/config.json) that includes extra optional properties.

#### Example Cloudwatch Config - just required properties

```JavaScript
{
    "systemd": {
        "unit": "webserver"
    },
    "backends": {
        "cloudwatch": {
            "log_group_name": "log_group_name",
            "log_stream_name": "log_stream_name"
        }
    }
}
```

#### Environment Variable Interpolation

Environment variables will be interpolated when the config is loaded.

```ENV=uat FOO=bar systemdlogger config.json```

```JavaScript
// config.json
{
    "systemd": {
        "unit": "webserver"
    },
    "backends": {
        "cloudwatch": {
            "log_group_name": "$ENV-myapp",
            "log_stream_name": "$FOO-myservice"
        }
    }
}
```

Is loaded as:

```JavaScript
        ...
        "cloudwatch": {
            "log_group_name": "uat-myapp",
            "log_stream_name": "bar-myservice"
        }
```JavaScript



-----------------------------------------------------------
## Elasticseach Backend

Creates daily indexes for logs, eg:
```
16-08-25-logs
16-08-26-logs
```


-----------------------------------------------------------
## Development Setup

```
make setup
source env/bin/activate
make deps
```

-----------------------------------------------------------

## Unit Tests

```make test```

-----------------------------------------------------------

## Integration Tests

Run against elasticsearch docker container.

```
docker-compose up -d
make test-integration
```



