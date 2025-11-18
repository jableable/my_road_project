# Road Overpass Detection in Satellite Imagery

## What This Does

This project uses a CNN to detect road overpasses in satellite imagery. Feed it a satellite image and it tells you whether there's an overpass in it or not.

I trained the model on thousands of satellite images that I automatically labeled using OpenStreetMap data. It hits around 92% accuracy on the validation set.

## Live Demo

There's a demo running on Hugging Face Spaces: [Road Overpass Detector Demo](https://huggingface.co/spaces/jableable/road_project)

You can drop in coordinates and see what the model thinks. No setup required.

<p align="center">
  <img src="./assets/images/demo_screenshot.png" width="700" />
</p>
<p align="center">
  <em>Screenshot: The live Streamlit app running on Hugging Face Spaces</em>
</p>

## How It Works

**Data Collection:** I used the Google Maps Static API to grab satellite images from different regions (North America, Europe, Asia). Instead of manually labeling thousands of images, I wrote a script that queries OpenStreetMap via OSMnx to count how many overpass crossings are in each image. This gave me labels automatically.

<p align="center">
  <img src="./assets/images/la_sat_map.png" width="400" />
  <img src="./assets/images/la_combined_map.png" width="400" />
</p>
<p align="center">
  <em>Left: Raw satellite image • Right: Same tile with OpenStreetMap road graph overlay used for labeling</em>
</p>

**The Model:** It's a straightforward CNN built in TensorFlow/Keras. I added some data augmentation (random flips, brightness tweaks) to make it more robust. The model outputs a probability - like "95% confident there's an overpass here."

**The Demo:** Built a simple Streamlit app where you can enter lat/long coordinates, fetch the satellite tile, and get an instant prediction. It's deployed on Hugging Face Spaces so anyone can try it.

## Installation

Clone the repo:
```bash
git clone https://github.com/yourusername/road-overpass-detector.git
cd road-overpass-detector
```

Install dependencies (use a virtualenv if you want):
```bash
pip install osmnx shapely pyproj utm imutils opencv-python matplotlib numpy pandas scikit-learn tensorflow pillow streamlit
```

If you're going to fetch new images or run the demo locally, you'll need a Google Static Maps API key. Set it as an environment variable:
```bash
export goog_api="YOUR_API_KEY"  # Linux/Mac
set goog_api=YOUR_API_KEY       # Windows
```

## Usage

**Easiest option:** Just use the [web demo](https://huggingface.co/spaces/jableable/road_project). 

**Run locally:** If you have the trained model file, you can run the Streamlit app:
```bash
streamlit run new_app.py
```

**Use in your own code:**
```python
from keras.models import load_model
import numpy as np
from PIL import Image

model = load_model("best_model.keras")
img = Image.open("your_image.png").resize((640, 640))
img_array = np.array(img)[None, ...] / 255.0

pred = model.predict(img_array)
prob_overpass = pred[0][1] * 100  # second value is overpass probability

print(f"Overpass probability: {prob_overpass:.2f}%")
```

The model expects 640x640 RGB images and outputs `[P(no overpass), P(overpass)]`.

> **Note:** The trained model file (~118 MB) isn't in this repo. You can grab it from the Hugging Face Space or retrain it yourself.

**Retrain from scratch:**

1. Generate a dataset using the scripts in `dataset_generation/` (fetch images, label them with OSM data)
2. Preprocess using `dataset_processing/`
3. Train: `python model/binary_classification_model.py`

Fair warning: training from scratch needs a decent GPU and a lot of images (I used ~12,000).

## Example Results




**With overpass:** Highway interchange with a curved ramp passing over the main road. The model correctly gives this very high confidence.

**No overpass:** Suburban streets intersecting at ground level. Model correctly predicts no overpass with high confidence.

## Credits

- **OpenStreetMap & OSMnx** - for the road network data that made automatic labeling possible
- **Google Static Maps API** - for the satellite imagery
- **TensorFlow/Keras** - for the deep learning framework
- **Streamlit & Hugging Face Spaces** - for making the demo dead simple to deploy

## License

MIT License - use it however you want. See LICENSE file.


