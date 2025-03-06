import os

# Đường dẫn tới folder chứa các file
folder_path = "D:/python-tutorial/dataset thyroid/train/Malignant/Tiroides4"

# Duyệt qua các file trong folder
for filename in os.listdir(folder_path):
    if "tiroides" in filename:  # Kiểm tra nếu tên file chứa từ "tiroides"
        new_filename = filename.replace("tiroides", "malignant")  # Thay "tiroides" bằng "benign"
        old_file_path = os.path.join(folder_path, filename)
        new_file_path = os.path.join(folder_path, new_filename)
        os.rename(old_file_path, new_file_path)  # Đổi tên file
        print(f"Đã đổi tên: {old_file_path} thành {new_file_path}")

