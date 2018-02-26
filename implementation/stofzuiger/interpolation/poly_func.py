import numpy as np
import matplotlib.pyplot as plt


t = np.array([7.307692,8.923077,9.923077,10.923077,11.923077,13,14,15,16,16.923077,18,19,21,22,23.384615,24.384615,25.461538,28.461538])
y = np.array([-994,-1004,-988,-1072,-928,-572,-1164,-1226,-740,-1080,-1130,-1040,-1080,-1050,-1025,-1080,-960,-1050])
t = (t - np.min(t))/(np.max(t)-np.min(t)) * 2 - 1

def cheb(n,x):
    if (n==0):return 1;
    if (n==1):return x;
    return 2*x*cheb(n-1,x) - cheb(n-2,x)


n=30

coefs = np.empty([n])

for k in range(0, n):
    ratio = (2./(n+1.))
    sum = 0;
    for l in range(0, n +1):
        tl = np.cos((l+(1./2.)) * (np.pi/(n+1.)))
        sum += np.interp(tl, t, y) * cheb(k,tl)
    coefs[k] = ratio * sum

print coefs

yHat = np.empty([21])
i = 0;
for tx in np.arange(-1.0, 1.1, 0.1):
    sum = 0
    for k in range(0, n):
        sum += .5 * coefs[k] * cheb(k,tx)
    yHat[i] = sum
    i+=1

print yHat

plt.plot(np.arange(-1.0, 1.1, 0.1),yHat)
plt.plot(t,y)
plt.show()

