from flask import Flask, render_template, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import numpy as np
import os

#khởi tạo ứng dụng flask
app = Flask(__name__)
#tải mô hình đã huấn luyện
model = load_model("D:/python-tutorial/web_thyroid_classification/models/best_model.keras")  # Tải mô hình tốt nhất đã lưu
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Danh sách nhãn lớp
CLASS_LABELS = ['BENIGN', 'MALIGNANT']

@app.route('/', methods=['GET', 'POST'])
def index():#hàm xử lí cho url/
    if request.method == 'POST':
        # Kiểm tra xem người dùng có tải ảnh lên không
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files['file']
        
        if file.filename == '':
            return jsonify({"error": "Empty filename"}), 400

        # Lưu ảnh và xử lý
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            # Xử lý và phân loại ảnh
            img = load_img(filepath, target_size=(256, 256))#load ảnh và resize về kích thước 256
            img_array = img_to_array(img) / 255.0#chuẩn hóa pixel (0-255) thành (0-1).
            img_array = np.expand_dims(img_array, axis=0)

            # Dự đoán
            prediction = model.predict(img_array)
            class_index = np.argmax(prediction)
            class_label = CLASS_LABELS[class_index]

            # Trả về JSON chứa kết quả phân loại và đường dẫn ảnh
            return jsonify({"result": class_label, "image_path": filepath})

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
