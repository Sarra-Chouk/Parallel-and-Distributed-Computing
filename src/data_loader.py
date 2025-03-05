import glob
import cv2

def read_images(file_paths):
    """
    Reads all images from the list of file paths using OpenCV in grayscale mode.
    """
    images = []
    for file_path in file_paths:
        image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        if image is not None:
            images.append(image)
    return images

def load_dataset(dataset_path):
    """
    Loads the dataset from the given path. Assumes the dataset contains two subdirectories: 'yes' and 'no'.
    
    Returns:
        tuple: (yes_images, no_images)
    """
    yes_paths = glob.glob(dataset_path + 'yes/*.jpg')
    no_paths = glob.glob(dataset_path + 'no/*.jpg')
    yes_images = read_images(yes_paths)
    no_images = read_images(no_paths)
    return yes_images, no_images
