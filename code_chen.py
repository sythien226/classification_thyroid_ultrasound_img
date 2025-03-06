import os

# Đường dẫn đến thư mục chứa các file
folder_path = 'D:/python-tutorial/output_data7/normal'

# Duyệt qua từng file trong thư mục
for filename in os.listdir(folder_path):
    # Tạo đường dẫn đầy đủ cho file
    old_file_path = os.path.join(folder_path, filename)

    # Kiểm tra nếu là file (bỏ qua thư mục con)
    if os.path.isfile(old_file_path):
        # Chèn thêm "TDID" vào trước tên file (trước phần mở rộng)
        new_filename = "TDID_" + filename
        new_file_path = os.path.join(folder_path, new_filename)

        # Đổi tên file
        os.rename(old_file_path, new_file_path)

print("Đã đổi tên các file thành công!")
