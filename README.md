# Description

This project is Lab 04 part 2 from the DSAI3202 - Parallel and Distributed Computing course. It aims to classify MRI brain images for tumor detection using machine learning and deep learning techniques.

It explores the use of parallel processing techniques—sequential, multithreading, and multiprocessing—in the context of image classification, showcasing how different execution strategies impact model training and feature extraction time.

---

## Breakdown

`1. Dataset Preparation:`

- Loads MRI brain scan images from a labeled dataset (`yes` = tumor, `no` = no tumor).

`2. Image Preprocessing:`

- Resizing and normalization

- Grayscale conversion

- Noise reduction

`3. Feature Extraction:`

- Extracts features from images using pre-defined techniques.

`4. Model Training & Evaluation:`

- Trains classifiers to detect brain tumors and evaluates their performance.

`5. Parallel Execution:`

- Implements the same workflow using sequential code, multithreading and multiprocessing.

---

## How to run

Open the notebbok:

<pre><code>jupyter notebook notebooks/ImageProcessingForTumorDetection.ipynb</code></pre>

Or run `.py` files via:

<pre><code>python main.py</code></pre>
