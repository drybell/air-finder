# AirTraffic Finder Application
Track Airplane Location and find distances between two airplanes.
I am using OpenSky API, and linked its Git page to this repo. I do recommend 
taking a look at their repo as well as their website linked here: 
https://opensky-network.org/apidoc/index.html

Program Name: test.py (main driver)  <br /> 
Files Required: countries.py (dictionary of bounding boxes for all countries)

## January 2nd 
This project will use OpenSky API in order to pull relevant information about 
current airplanes in the air and find the distance between them. 

Currently, I have made a working prototype labelled "test.py" which can be used
with "countries.py" in order to track current airplane information. 

This is an in shell program that has a couple of current uses. 
After running python3 test.py, the usages are: 
### country:  
            Lets you see what planes are flying from a country of origin. First
            input a country that you want to track and the program will fetch
            data for all planes flying from that country.
            After the program prints out all of the current planes, it gives you
            an option to see what planes are currently flying within the given 
            country's borders. (This is quite finicky because I use a bounding box
            with only 4 coordinates, but it is still accurate within the box)
  
### callsign: 
            Lets you append an airplane to a list for tracking purposes. You
            MUST input the correct callsign of the plane, which is simple if you
            have called <country> once and viewed the planes
  
### list: 
            View all planes you are tracking using the <callsign> input
  
### distance: 
            Lets you use your tracking list to find the distance between two planes.
            Uses the Haversine formula to calculate distances given Earth is a perfect sphere.
            Also incorporates altitude of each plane for a better distance estimation
  
### clear: 
            Currently just clears your tracking list



## Next Steps:
I will be using Processing to begin visualizing this data on a 2D map of the world. This 
application will track all planes visible by the OpenSky API and map them in real-time 
to their respective locations within the map. 

I will also be polishing test.py by removing global variables, creating a Tracker Object,
and simplifying some parts of the code. 

