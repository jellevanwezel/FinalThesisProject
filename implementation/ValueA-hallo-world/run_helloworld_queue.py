#!/usr/bin/env python
from valuea_framework.connectors.rabbitmq.Simple import SimpleRpcClient

rpcclient = SimpleRpcClient(hostname='localhost',
                            exchange='default_exchange',
                            username='admin',
                            password='admin')


remote_procedure = 'services.valuea.samples.helloworld'

x = [1,2,3,4,5,6,7,8,9,10,11,12,13];
k = 3;

print(" [x] Requesting %s" % remote_procedure)
response = rpcclient.call(remote_procedure, {'k': k, 'x': x})
print(" [.] Got %r" % response)