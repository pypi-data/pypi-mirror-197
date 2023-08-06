## QUADx88

Configurable dynamical model of quadcopter

## Brief documentation

First, we need to construct a quadcopter object providing all parameters 


``python
import quadx88 as qx

copter = qx.Quadcopter(mass=1.15, 
                       ts=0.0083,
                       prop_mass=0.01)
```
