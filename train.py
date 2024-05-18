import cv2
import os
from PIL import Image
import numpy as np

def train_face_recognizer(dataset_path, output_path):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier("/Users/lvc/PycharmProjects/pythonProject6/haarcascade_frontalface_default.xml")

    def get_images_and_labels(path):
        image_paths = [os.path.join(path, f) for f in os.listdir(path)]
        face_samples = []
        ids = []
        for image_path in image_paths:
            PIL_img = Image.open(image_path).convert('L')  # Chuyển đổi thành ảnh grayscale
            img_numpy = np.array(PIL_img, 'uint8')
            id = int(os.path.split(image_path)[-1].split(".")[1])
            faces = detector.detectMultiScale(img_numpy)
            for (x, y, w, h) in faces:
                face_samples.append(img_numpy[y:y + h, x:x + w])
                ids.append(id)
        return face_samples, ids

    print("\n[INFO] Đang huấn luyện mặt. Hãy chờ một vài giây...")
    faces, ids = get_images_and_labels(dataset_path)
    recognizer.train(faces, np.array(ids))

    recognizer.write(output_path)  # recognizer.save() hoạt động trên Mac, nhưng không trên Pi
    print("\n[INFO] Đã huấn luyện thành công {0} khuôn mặt. Kết thúc chương trình.".format(len(np.unique(ids))))

if __name__ == "__main__":
    # Gọi hàm để huấn luyện và lưu mô hình nhận dạng khuôn mặt
    dataset_path = '/Users/lvc/PycharmProjects/pythonProject6/dataset'
    output_path = 'trainer/trainer.yml'
    train_face_recognizer(dataset_path, output_path)
