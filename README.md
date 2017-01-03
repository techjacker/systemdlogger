# systemdlogger

Exports systemd logs to an external service, eg cloudwatch, elasticsearch.
Use with a cron job.

Python3+.


-----------------------------------------------------------

## Installation

#### Install Dependencies
[python-systemd](https://github.com/systemd/python-systemd)
Fedora/RHEL/CentOS
```
dnf install python-systemd python3-systemd
```
Debian/Ubuntu/Mint
```
apt-get install python-systemd python3-systemd
```


#### Install
```
pip install systemdlogger
```



-----------------------------------------------------------


## Usage

```Shell
```


Creates logs in the following format:
```
log_group_name = <project>-<env>
log_stream_name = <systemdunit>-<ec2instanceid>
```



## Example Usage - Cloudwatch Backend

#### Create Cron Job
```Shell
*/1 * * * * . /etc/webserver.env; systemdlogger >/logs/systemdlogger.log 2>&1
```

Creates the following logs in cloudformation that get updated every minute:
```
myapp-staging/webserver-i045458d
```


-----------------------------------------------------------

## Development

### Setup

```
make setup
source env/bin/activate
make deps

make test
```

-----------------------------------------------------------

## Tests

```
py.test tests -q
```


-----------------------------------------------------------


