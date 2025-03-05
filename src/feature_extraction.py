import numpy as np
import skimage.feature as feature
import concurrent.futures

def compute_glcm_features(image, filter_name):
    """
    Computes GLCM features for the given image.
    """
    # Convert image from float to uint8
    image = (image * 255).astype(np.uint8)
    graycom = feature.graycomatrix(
        image,
        distances=[1],
        angles=[0, np.pi/4, np.pi/2, 3*np.pi/4],
        levels=256,
        symmetric=True,
        normed=True
    )
    features = {}
    for prop in ['contrast', 'dissimilarity', 'homogeneity', 'energy', 'correlation', 'ASM']:
        values = feature.graycoprops(graycom, prop).flatten()
        for i, value in enumerate(values):
            features[f'{filter_name}_{prop}_{i+1}'] = value
    return features

def process_image_features(filtered_images, tumor_presence):
    """
    Processes a single filtered image dictionary to compute GLCM features.
    Adds the 'Tumor' label.
    """
    glcm_features = {}
    for key, image in filtered_images.items():
        glcm_features.update(compute_glcm_features(image, key))
    glcm_features['Tumor'] = tumor_presence
    return glcm_features

def process_features_sequential(images_list, tumor_presence):
    """
    Processes a list of filtered images sequentially to extract GLCM features.
    """
    glcm_features_list = []
    for filtered_images in images_list:
        glcm_features_list.append(process_image_features(filtered_images, tumor_presence))
    return glcm_features_list

def process_features_parallel(images_list, tumor_presence, num_workers=6):
    """
    Processes a list of filtered images in parallel to extract GLCM features.
    """
    glcm_features_list = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = [
            executor.submit(process_image_features, filtered_images, tumor_presence)
            for filtered_images in images_list
        ]
        for future in concurrent.futures.as_completed(futures):
            glcm_features_list.append(future.result())
    return glcm_features_list
