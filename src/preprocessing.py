from skimage.filters.rank import entropy
from skimage.morphology import disk
from scipy import ndimage as nd
from skimage.filters import sobel, gabor, hessian, prewitt
import matplotlib.pyplot as plt

def process_image(image):
    """
    Applies several filters to the image and returns a dictionary of filtered images.
    """
    return {
        'Original': image,
        'Entropy': entropy(image, disk(2)),
        'Gaussian': nd.gaussian_filter(image, sigma=1),
        'Sobel': sobel(image),
        'Gabor': gabor(image, frequency=0.9)[1],
        'Hessian': hessian(image, sigmas=range(1, 100, 1)),
        'Prewitt': prewitt(image)
    }

def show_filtered_images(filtered_images):
    """
    Displays a dictionary of images using matplotlib.
    """
    plt.figure(figsize=(18, 3))
    num_filters = len(filtered_images)
    for i, (filter_name, image) in enumerate(filtered_images.items()):
        plt.subplot(1, num_filters, i + 1)
        plt.imshow(image, cmap='gray')
        plt.title(filter_name)
        plt.axis('off')
    plt.show()
