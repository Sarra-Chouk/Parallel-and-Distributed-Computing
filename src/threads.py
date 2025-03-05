import concurrent.futures
from preprocessing import process_image

def process_images_multithreading(images, num_workers=6):
    """
    Processes images using multithreading.
    
    Returns:
        list: A list of dictionaries containing filtered images.
    """
    processed_images = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(process_image, image) for image in images]
        for future in concurrent.futures.as_completed(futures):
            processed_images.append(future.result())
    return processed_images
