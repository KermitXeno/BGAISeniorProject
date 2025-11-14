import os
import tensorflow as tf
import keras
import PySide6
import numpy as np

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox

MRImodel = keras.saving.load_model("./AMRI/weights/AMRIGENETV1.keras")
optimizer = tf.keras.optimizers.SGD(learning_rate=0.00015)
MRImodel.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy', 'mse'])
BIOModel = keras.saving.load_model("./BIOFM/weights/BIOFMGENETV1.keras")
optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
BIOModel.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])


class ModelApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Model Prediction UI")
        self.setGeometry(100, 100, 500, 500)

        layout = QVBoxLayout()

        self.label = QLabel("Select an option to make a prediction:")
        layout.addWidget(self.label)

        self.mri_button = QPushButton("Predict MRI Image")
        self.mri_button.clicked.connect(self.predict_mri)
        layout.addWidget(self.mri_button)

        self.bio_button = QPushButton("Predict Biological Features")
        self.bio_button.clicked.connect(self.predict_bio)
        layout.addWidget(self.bio_button)

        self.setLayout(layout)

    def predict_mri(self):
        file_dialog = QFileDialog()
        image_path, _ = file_dialog.getOpenFileName(self, "Select MRI Image", "", "Image Files (*.png *.jpg *.jpeg)")

        if image_path:
            from keras.preprocessing import image
            import numpy as np

            img = image.load_img(image_path, target_size=(128, 128))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            predictions = MRImodel.predict(img_array)

            classes = ['Mild Impairment', 'Moderate Impairment', 'No Impairment', 'Very Mild Impairment']
            predicted_class = classes[np.argmax(predictions[0])]

            QMessageBox.information(self, "Prediction Result", f"Predicted Class: {predicted_class}")

    def predict_bio(self):
        from PySide6.QtWidgets import QInputDialog

        features_str, ok = QInputDialog.getText(self, "Input Biological Features",
                                                "Enter features separated by commas:")

        if ok and features_str:
            features = list(map(float, features_str.split(',')))
            features_array = np.array(features).reshape(1, -1)
            predictions = BIOModel.predict(features_array)

            classes = ['Mild Impairment', 'Moderate Impairment', 'No Impairment', 'Very Mild Impairment']
            predicted_class = classes[np.argmax(predictions[0])]

            QMessageBox.information(self, "Prediction Result", f"Predicted Class: {predicted_class}")


# render the UI
if __name__ == "__main__":
    app = QApplication([])
    window = ModelApp()
    window.show()
    app.exec()
