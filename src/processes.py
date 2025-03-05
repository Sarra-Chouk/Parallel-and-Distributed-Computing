import concurrent.futures
import numpy as np
from skimage.filters.rank import entropy
from skimage.morphology import disk
from scipy import ndimage as nd
from skimage.filters import sobel, gabor, hessian, prewitt

def apply_hessian_filter(chunk):
    """
    Applies the Hessian filter to a single chunk of the image.
    """
    return hessian(chunk, sigmas=range(1, 100, 1))

def parallel_hessian_filter(image, num_workers=6):
    """
    Applies the Hessian filter in parallel by splitting the image into chunks.
    """
    # Split the image into smaller chunks for parallel processing
    chunks = np.array_split(image, num_workers)
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
        # Apply the Hessian filter to each chunk in parallel
        hessian_chunks = list(executor.map(apply_hessian_filter, chunks))
    # Combine the filtered chunks back into a single image
    hessian_img = np.concatenate(hessian_chunks)
    return hessian_img

def process_image(image, num_workers=6):
    """
    Applies the specified filters to a single image and returns a dictionary with
    the original and filtered images. The Hessian filter is applied in parallel.
    """
    # Apply the Hessian filter in parallel
    hessian_img = parallel_hessian_filter(image, num_workers)
    
    # Apply the remaining filters sequentially
    return {
        'Original': image,
        'Entropy': entropy(image, disk(2)),
        'Gaussian': nd.gaussian_filter(image, sigma=1),
        'Sobel': sobel(image),
        'Gabor': gabor(image, frequency=0.9)[1],
        'Hessian': hessian_img,
        'Prewitt': prewitt(image)
    }

def process_image_wrapper(image, num_workers):
    """
    Wrapper function to make process_image picklable for multiprocessing.
    """
    return process_image(image, num_workers)

def process_images_multiprocessing(images, num_workers=6):
    """
    Processes all images in parallel using multiprocessing.
    """
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
        processed_images = list(
            executor.map(process_image_wrapper, images, [num_workers] * len(images))
        )
    return processed_images