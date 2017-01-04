# systemdlogger


### Sooner

- bulk save
	- combine entries with same timestamp into single doctype
	- make bulk PUT call to elasticsearch API (need to move to low level es python client first)

- switch to [low level elasticsearch python lib](https://github.com/elastic/elasticsearch-py)
	- add [AWS creds option](https://github.com/elastic/elasticsearch-py/blob/1780214a194959e399450abd7a779bd71d6099af/docs/index.rst#running-on-aws-with-iam)

======================================================================

### Later

- add retries for failed attempts

- logstash
	- see their config for how to adapt payload/mappings

- add more CloudwatchLogger tests
	- integration
	- unit
		- mock methods called in __init__
			- self.setup_logs(env, project, app)
		- moto
			- mock aws SDK calls
