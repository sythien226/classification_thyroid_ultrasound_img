import xml.etree.ElementTree as ET
import os

# Đọc file XML và trích xuất thông tin
def parse_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Giả sử trường tirads dùng để phân loại
    tirads = root.find('.//tirads').text if root.find('.//tirads') is not None else None
    
    # Phân loại nhãn dựa trên tirads
    if tirads is None or tirads.strip().lower() == 'none':
        label = 'normal'
    elif tirads.strip().lower() in ['1', '2', '3']:
        label = 'benign'
    elif tirads.strip().lower() in ['4', '4a', '4b', '4c', '5']:
        label = 'malignant'
    else:
        label = 'normal'  # Mặc định nếu không rơi vào trường hợp nào

    return label

# Tìm file ảnh tương ứng với ID từ XML
def find_images(image_dir, image_id):
    matched_images = []
    for file_name in os.listdir(image_dir):
        if file_name.startswith(image_id + "_") and file_name.endswith(".jpg"):  # Tìm các file bắt đầu bằng image_id và kết thúc bằng .jpg
            matched_images.append(os.path.join(image_dir, file_name))
    return matched_images

# Xử lý dữ liệu cho tất cả các ảnh và file XML
def process_dataset(image_dir, xml_dir, output_dir):
    for xml_file in os.listdir(xml_dir):
        if not xml_file.endswith('.xml'):
            continue
        image_id = xml_file.replace('.xml', '')  # Lấy ID từ tên file XML
        image_paths = find_images(image_dir, image_id)  # Tìm các file ảnh tương ứng (1_1.jpg, 1_2.jpg, ...)
        if not image_paths:
            print(f"Không tìm thấy file ảnh nào cho {xml_file}")
            continue
        
        xml_path = os.path.join(xml_dir, xml_file)
        label = parse_xml(xml_path)
        
        for image_path in image_paths:
            label_dir = os.path.join(output_dir, label)
            os.makedirs(label_dir, exist_ok=True)
            filename = os.path.basename(image_path)
            os.rename(image_path, os.path.join(label_dir, filename))  # Chuyển file vào thư mục tương ứng với nhãn

# Đường dẫn thư mục
image_dir = 'D:/python-tutorial/archive/file_anh'  # Đường dẫn tới thư mục chứa ảnh JPG
xml_dir = 'D:/python-tutorial/archive/file.XML'   # Đường dẫn tới thư mục chứa file XML
output_dir = 'D:/python-tutorial/output_data7'     # Đường dẫn tới thư mục lưu ảnh đã xử lý

# Thực hiện xử lý
process_dataset(image_dir, xml_dir, output_dir)
