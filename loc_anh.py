import os

# Đường dẫn tới folder chứa dữ liệu của bạn
folder_path = "D:/python-tutorial/dataset thyroid/train/benign"

# Duyệt qua các file trong folder
for filename in os.listdir(folder_path):
    if "Copy" in filename:  # Kiểm tra nếu tên file chứa chữ "Copy"
        file_path = os.path.join(folder_path, filename)
        os.remove(file_path)  # Xóa file
        print(f"Đã xóa: {file_path}")
