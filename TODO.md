# systemdlogger




make test-integration
	py.test skip normally
	./tests/test_runner_integration.py

-----------------------------------------------------------
-----------------------------------------------------------

make aws creds params optional (cloudwatch)
	- switch to **kwargs style?

-----------------------------------------------------------
-----------------------------------------------------------

bulk save
	combine entries with same timestamp into single doctype


=====================================================================================
=====================================================================================

logstash - how to configure
	- see cloudwatch -> how to adapt payload
	- retries?

cloudwatch
	- mock methods called in __init__
	self.setup_logs(env, project, app)


moto
	- mock aws SDK calls
