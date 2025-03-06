import os
import cv2
import tensorflow as tf
import numpy as np

# Function to process and save images
def process_images(input_folder, output_folder, img_size):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):  # Specify image formats
            # Load the image
            img_path = os.path.join(input_folder, filename)
            image = cv2.imread(img_path)

            # Resize the image to specified size (IMG_SIZE x IMG_SIZE) using tf.keras.layers.Resizing
            resize_layer = tf.keras.Sequential([tf.keras.layers.Resizing(img_size, img_size)])
            image = resize_layer(np.array([image]))[0].numpy().astype(np.uint8) #chuyển tensor ve dang mang np và kieu dl ảnh uint8uint8

            # Convert image to grayscale using tf.image.rgb_to_grayscale
            gray_image = tf.image.rgb_to_grayscale(image).numpy()

            # Apply median filter for noise removal using cv2.medianBlur
            denoised_image = cv2.medianBlur(gray_image, 5)

            # Save the processed image to the output folder
            output_path = os.path.join(output_folder, filename)
            cv2.imwrite(output_path, denoised_image)
            print(f"Processed and saved: {output_path}")

# Define input and output folders
input_folder = 'D:/python-tutorial/TDID_dataset_split/Benign'  # Replace with the path to your input folder
output_folder = 'D:/python-tutorial/TDID_dataset_split/Benign'  # Replace with the path to your output folder
IMG_SIZE = 256  # Set desired image size

# Call the function to process images
process_images(input_folder, output_folder, IMG_SIZE)
