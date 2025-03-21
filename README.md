# Description
This project is a simple, modular implementation of a machine learning pipeline developed for the course DSAI3202 - Parallel and Distributed Computing.

It demonstrates how to structure an ML project into clearly defined stages using separate modules. 

The focus is not just on building a working model, but also on organizing code in a way that supports scalability, readability, and parallel development.

### Breakdown

The program performs the following steps:

`1. Loads the dataset:`
The data_loader module handles reading in data from a defined source.

`2. Preprocesses and splits the data:`
Using the preprocessing module, the data is cleaned and split into training and testing sets.

`3. Trains a machine learning model:`
The model module defines and trains a model (such as a decision tree or similar classifier).

`4. Evaluates the model's performance:`
Finally, the evaluation module runs the trained model on the test set and prints out an evaluation report (e.g., accuracy, precision, recall).

---

### How to run

<pre><code>pip install -r requirements.txt 
  python main.py</code></pre>
