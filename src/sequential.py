from tqdm import tqdm
from preprocessing import process_image

def process_images_sequential(images):
    """
    Processes a list of images sequentially by applying the filters.
    
    Returns:
        list: A list of dictionaries containing filtered images.
    """
    processed_images = []
    for image in tqdm(images, desc="Processing images sequentially"):
        processed_images.append(process_image(image))
    return processed_images
