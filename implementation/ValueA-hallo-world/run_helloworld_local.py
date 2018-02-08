#!/usr/bin/env python
# tell python we want to use "helloworld"
import services.valuea.samples.helloworld

# construct a new object from the helloworld service
srv = services.valuea.samples.helloworld.Service()

x = [1,2,3,4,5,6,7,8,9,10,11,12,13];
k = 3;

# execute the service and return the result to a variable named result
srv.set_message({'dataset':'wine','k': k, 'x': x})
result = srv.execute()

# put our data on screen as text
print (result)