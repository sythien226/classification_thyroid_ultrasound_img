// Lắng nghe sự kiện thay đổi khi chọn file
//tệp javascript chứa logic phía client xử lí tương tác trên giao diện như hiển thị kq)
document.getElementById("file").addEventListener("change", function(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.querySelector(".preview").innerHTML = `<img src="${e.target.result}" alt="Xem trước ảnh" class="img-thumbnail" width="300">`;
        };
        reader.readAsDataURL(file);
    }
});

// Hàm gửi ảnh và nhận kết quả phân loại
function classifyImage() {
    const formData = new FormData();
    const fileInput = document.getElementById("file");
    
    if (!fileInput.files.length) {
        alert("Vui lòng chọn một ảnh.");
        return;
    }
    
    formData.append("file", fileInput.files[0]);

    fetch("/", {
        method: "POST",
        body: formData
    })
    .then(response => response.json()) 
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            // Hiển thị kết quả phân loại
            document.querySelector(".result").style.display = "block";
            document.getElementById("resultLabel").textContent = data.result;
            document.querySelector(".preview").innerHTML = `<img src="/${data.image_path}" alt="Ảnh tuyến giáp" class="img-thumbnail" width="300">`;
        }
    })
    .catch(error => {
        console.error("Lỗi:", error);
        alert("Có lỗi xảy ra khi phân loại ảnh.");
    });
}
