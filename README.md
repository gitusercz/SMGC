# SMGC - Shelly Measurement Graph Creator
I recently bought a Shelly Power meter. It is a smart plug with remote control feature. I bought it for its capability to measure power. 
![Image of a Shelly plug and its box](/resources/Shelly_img.png)

## 1. Setting up the plug
Setting up the plug is easy. If you are also interested only to use it as a power meter, connecting to the cloud service is not necessary. In your router admin site, find out what is its MAC address, and I recommend to set a rule to give a static IP for the power meter. That way the power meter shows up on the same IP address after a router / Shelly reboot. 
If you know the IP address, you can query meter status in the browser: 
![Image of a Shelly plug's built in webserver content](/resources/meter.png)

**SMGC** relies on fields: 
- power
- total
> **Note:** "total" field is the aggregated power use in rounded watt / minutes since the plug is plugged in. It restarts from 0 after a power cycle. 
> the "timestamp" field could be used, but each timestamp is querried from the machine on which the python script runs on instead. 

### 1.1 Setting up the script
Take a look to the config.ini file. Lines, beginning with # are ignored, so you can have your own comments here too. Set absolute paths for the graph images to be saved, and you can set a naming prefix too (like: Washing_machine_power_use_log_). **Do not use spaces here!**

### 1.2 Use 'streak' mode
There are two working modes for **SMGC**. 

**Streak:** Graph's first measurement point will be the first value, that is more than 0.00 Watt. Graph's last measurement point is when the power value drops to 0.00 Watts. When this happens, streak is finished and graph is created. 

**24h:** 24 Hour mode. Each day at midnight a new measurement starts. Each measurement point is recorded. A 23:59:59 graph is closed and drawed. In this mode power values do not trigger graph creation, everything is logged, graph is created daily. Therefore the x axis always spans from 0 to 24 hour. 

## 2 Using the plug
To set it up, enter the correct IP address to the config file. With a browser on the same subnet, navigate to [ipaddress]/meter/0 to make sure that Shelly works. 

Then open the config.ini file, set '24h' or 'streak' as workmode. Add a prefix for the graph file to be named. Then run the main.py on your computer. I personally run SMGC on a RaspberryPi, but it does not matter if it is a PC or something else. 

When streak is over or midnight passes, the graph file is ready. And saved into a subfolder. 

## 4. Some example graphs depicting the possibilities with the script
### 4.1 Dishwasher
With streak mode I was able to see, how long a dishwashing cycle runs. These graphs highlight the differences between different washing cycles. On my dishwashing machine there is a (default) 50C ECO mode, which is supposed to use the minimal required electricity and water: 
![Graph created during 50C ECO run](/resources/50CECO.png)

Other programs run faster but use more electricity (65C): 

![Graph created during 50C ECO run](/resources/65C.png)

70C: 
![Graph created during 50C ECO run](/resources/70C.png)

### 4.2 Drying machine
The following graph was also created in streak mode, but this time connected to a drying machine. To prevent wrinkled clothes after a cycle it periodicaly starts again. On this graph it is nicely demonstrated how the preiodicity changes over time and at last it stops. 

![Graph created during drying cycle](/resources/Drying_machine.png)

### 4.3 Fridge
I was interested in how much does it cost to run just the fridge daily. These values are measured in summer, when room temperature was ~24C in 24h mode of SMGC. I was expecting more frequent turn on / off periods of the compressor. Note the 15Watt spikes, which indicate a door opening event. 


![24h_fridge run](/resources/Fridge.png)

Or if you take a look at this graph, you can tell that someone opened the fridge at ~5:00 in the morning. 
![24h_fridge run](/resources/Fridge2.png)


## 3. Disclaimer
Use with caution and for your own responsibility. Use this SW as you wish. 


Best regards, 
Attila Czibere
2023-06

