import concurrent.futures
from preprocessing import process_image

def process_images_multiprocessing(images, num_workers=6):
    """
    Processes images using multiprocessing.
    
    Returns:
        list: A list of dictionaries containing filtered images.
    """
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
        processed_images = list(executor.map(process_image, images))
    return processed_images

