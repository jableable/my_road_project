# Dataset
The plan is to train our model on 10,000+ images (likely .png) of satellite data of various parts of cities involving some number of roads/highways, such as this:

<p align = "center">
<img src="./assets/images/la_sat_map.png" width="400" />
</p>

We'll initially limit ourselves to images with at most 10 crossings (upgrading to more crossings if time allows). Here are things that need doing/exploring:

1. Use Google Maps API to download satellite images of a fixed size based on GPS coordinates
    * Not sure what fixed size/resolution/zoom should be
2. Get map bounding box of "crossing_counter_cleaned.py" to agree with bounding box of OpenStreetMap API
    * These should also agree with Google Maps API images

&nbsp;

# Labeling the Dataset

I've already coded "crossing_counter_cleaned.py" to help us automate crossing counts based on the underlying graph representation from OpenStreetMaps. You can see the crossings from the satellite map above as black vertices here:

<p align = "center">
<img src="./assets/images/la_combined_map.png" width="400" />
</p>

Here are things that need doing/exploring:

1. Rewrite "crossing_counter_cleaned.py" as a function that another Python file can call
2. Verify count from "crossing_counter_cleaned.py" on several hundred pictures (we should each take a portion of these)
    * Can anyone easily make a GUI to make this process smoother? I.e. click a "correct" (or "incorrect") button for an image, automatically save that image in a special folder, then automatically load the next image? 
3. Get map bounding box of "crossing_counter_cleaned.py" to agree with bounding box of API

&nbsp;

# Dataset Processing

[This](https://rock-feller.github.io/intro.html) is a great place to start when considering how our images should be modified. The fundamental philosophy is to create as diverse a dataset as possible while not occupying an inordinate amount of memory. We'll initially consider black-and-white images for space-saving, and then perhaps upgrade to color if that gives better results (color has 3x the data as black-and-white).

Here are things that need doing/exploring:

1. Find an automated way to crop/blur out irrelevant features surrounding the road systems (i.e. greenery and water)
2. Experiment with SVD decomposition to compress our data set in a smart way while maintaining predictive success

&nbsp;

# Training the Model

If you go to "Filter by Topic" on the Data Science Boot Camp course page on Erdős Institute, you can skip to "12 Week: Neural Networks." There's about 2 hours worth of videos to watch on neural networks. After all of us have watched the videos, we should work on the group problem session together sometime soon.

To experiment, I built a model based on the Erdős Institute model, and I trained it on randomly generated "X" images with a high level of success. I shared some results in our Slack channel. To train a model on 10,000+ images of decent resolution may need some serious computational power. I seem to have access to my university's supercomputer, though I've never used it before.

Here are things that need doing/exploring:

1. Determine how layers for CNN will work (seems to be a lot of guess-and-check)
2. To remove guess-and-check, visualize images after passing through each filter
    * Are the correct features being retained between layers?
3. Learn how to make calls to supercomputer


&nbsp;

# Some Reach Goals

Once we've accomplished all of the above, here are some next steps that would be very cool to do:

1. Isotope roads to decrease artificial complexity to get rid of unnecessary crossings
    * Knowledge of graph theory/knot theory/algebraic topology would be useful
2. Take direction of traffic (orientation) into account
3. Indicate <i>where</i> in the image crossings occur by boxing each crossing
    * These boxes can be programmed to show up in our training data
4. Explore how low our satellite image resolution can go while maintaining predictive success
    * This would widely increase our range of application
5. Is there a correlation between number of crossings and elevation? Or number of crossings and country? Population?
    * These kinds of statistics can help plan roads according to the area they're in
6. Can we train our model on satellite images with roads _being hidden_? Namely, can the terrain alone predict the number of road crossings that were built later on?


