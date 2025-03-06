import numpy as np
import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img

# Đường dẫn đến thư mục chứa ảnh gốc và ảnh lưu sau augment
input_folder = 'D:/python-tutorial - Sao chép/dataset thyroid/dataset thyroid/train/Malignant'
output_folder = 'D:/python-tutorial - Sao chép/dataset thyroid/dataset thyroid/train/Malignant'
os.makedirs(output_folder, exist_ok=True)

# Khởi tạo ImageDataGenerator cho từng loại augment
rotation_datagen = ImageDataGenerator(rotation_range=15)  # RandRotation: Xoay ngẫu nhiên từ -15 đến +15 độ
x_translation_datagen = ImageDataGenerator(width_shift_range=0.1)  # RandXTranslation: Dịch chuyển theo trục X 10%
y_translation_datagen = ImageDataGenerator(height_shift_range=0.1)  # RandYTranslation: Dịch chuyển theo trục Y 10%
x_reflection_datagen = ImageDataGenerator(horizontal_flip=True)  # RandXReflection: Lật ngang (theo trục X)
y_reflection_datagen = ImageDataGenerator(vertical_flip=True)  # RandYReflection: Lật dọc (theo trục Y)
padding_datagen = ImageDataGenerator(fill_mode='constant', cval=0)  # Padding: Thêm padding với giá trị 0 (màu đen)

# Hàm augment và lưu ảnh
def augment_and_save(datagen, image_list, prefix, output_dir, num_augments):
    for i, img_path in enumerate(image_list):
        img = load_img(img_path)
        x = img_to_array(img)
        x = np.expand_dims(x, axis=0)

        # Tạo augment
        aug_iter = datagen.flow(x, batch_size=1, save_to_dir=output_dir, 
                                save_prefix=prefix, save_format='jpg')

        # Lưu num_augments lần augment cho mỗi ảnh
        for _ in range(num_augments):
            next(aug_iter)
            print(f"Augmenting image {i+1}/{len(image_list)}: {img_path}")

# Tải danh sách ảnh gốc
image_paths = [os.path.join(input_folder, fname) for fname in os.listdir(input_folder) if fname.endswith('.jpg')]
print(f"Found {len(image_paths)} images.")

# Augment cho từng loại
augment_and_save(rotation_datagen, image_paths, 'rotate', output_folder, num_augments=1)
augment_and_save(x_translation_datagen, image_paths, 'x_translate', output_folder, num_augments=1)
augment_and_save(y_translation_datagen, image_paths, 'y_translate', output_folder, num_augments=1)
augment_and_save(x_reflection_datagen, image_paths, 'x_reflect', output_folder, num_augments=1)
augment_and_save(y_reflection_datagen, image_paths, 'y_reflect', output_folder, num_augments=1)
augment_and_save(padding_datagen, image_paths, 'padding', output_folder, num_augments=1)

# Kiểm tra tổng số ảnh augment
augmented_images = [fname for fname in os.listdir(output_folder) if fname.endswith('.jpg')]
print(f"Total augmented images: {len(augmented_images)}")
