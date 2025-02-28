from src.preprocessing import 

# Define the path to the dataset
dataset_path = '../datasets/brain_tumor_dataset/'

# List all image files in the 'yes' and 'no' directories
yes_images = glob.glob(dataset_path + 'yes/*.jpg')
no_images = glob.glob(dataset_path + 'no/*.jpg')

yes_images = read_images(yes_images)
no_images = read_images(no_images)

print(f"Number of 'yes' images: {len(yes_images)}")
print(f"Number of 'no' images: {len(no_images)}")

# Display each filtered image
plt.figure(figsize=(18, 3))
for i, (filter_name, filtered_image) in enumerate(filtered_images.items()):
        plt.subplot(1, len(filtered_images), i + 1)
        plt.imshow(filtered_image, cmap='gray')
        plt.title(filter_name)
        plt.axis('off')
plt.show()