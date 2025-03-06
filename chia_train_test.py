import os
import shutil
from sklearn.model_selection import train_test_split

# Đường dẫn đến thư mục chứa dataset
dataset_dir = 'D:/python-tutorial/TDID_dataset_split'

# Đường dẫn đến thư mục output cho train và test
train_dir = 'D:/python-tutorial/TDID_new1/train'
test_dir = 'D:/python-tutorial/TDID_new1/test'

# Tạo các thư mục output nếu chưa tồn tại
os.makedirs(train_dir, exist_ok=True)
os.makedirs(test_dir, exist_ok=True)

# Lấy danh sách các class (benign, malignant)
classes = ['Benign', 'Malignant']

for class_name in classes:
    # Lấy đường dẫn đến các file hình ảnh cho từng class
    class_dir = os.path.join(dataset_dir, class_name)
    images = os.listdir(class_dir)
    
    # Chia dữ liệu với tỷ lệ 8:2
    train_images, test_images = train_test_split(images, test_size=0.2, random_state=42)
    
    # Tạo thư mục cho từng class trong tập train và test
    os.makedirs(os.path.join(train_dir, class_name), exist_ok=True)
    os.makedirs(os.path.join(test_dir, class_name), exist_ok=True)
    
    # Sao chép ảnh vào thư mục train
    for img in train_images:
        src = os.path.join(class_dir, img)
        dst = os.path.join(train_dir, class_name, img)
        shutil.copy(src, dst)
    
    # Sao chép ảnh vào thư mục test
    for img in test_images:
        src = os.path.join(class_dir, img)
        dst = os.path.join(test_dir, class_name, img)
        shutil.copy(src, dst)

print("Chia dữ liệu thành công!")
