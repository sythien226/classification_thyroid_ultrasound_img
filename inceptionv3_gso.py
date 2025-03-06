import numpy as np
import cv2
from tensorflow.keras import layers, models
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import classification_report, confusion_matrix
from tensorflow.keras.applications import InceptionV3
from tensorflow.keras.callbacks import ModelCheckpoint

# Constants
TRAIN_DIR = 'D:/python-tutorial/data_local/TDID_new1/train'  # Đường dẫn huấn luyện
TEST_DIR = 'D:/python-tutorial/data_local/TDID_new1/test'    # Đường dẫn kiểm tra
IMG_SIZE = (256, 256)
BATCH_SIZE = 15
EPOCHS = 100

def create_inceptionv3_model(dropout_rate=0.2, input_shape=(256, 256, 3)):
    """Create a model based on InceptionV3 pretrained on ImageNet, with a custom output layer."""
    # Load the InceptionV3 model pre-trained on ImageNet
    base_model = InceptionV3(weights='imagenet', include_top=False, input_shape=input_shape)

    # Freeze the base model to avoid re-training the pretrained layers
    base_model.trainable = False

    model = models.Sequential()
    model.add(base_model)

    # Add Global Average Pooling layer to reduce the dimensions
    model.add(layers.GlobalAveragePooling2D())

    # Add a Dropout layer to prevent overfitting
    model.add(layers.Dropout(dropout_rate))

    # Fully Connected Layer 1
    model.add(layers.Dense(128, activation='relu'))

    # Fully Connected Layer 2
    model.add(layers.Dense(64, activation='relu'))

    # Output layer for binary classification
    model.add(layers.Dense(2, activation='softmax'))

    return model

def get_data_generators(train_dir, test_dir, img_size, batch_size):
    """Create data generators for training and testing datasets."""
    train_datagen = ImageDataGenerator(rescale=1./255)
    test_datagen = ImageDataGenerator(rescale=1./255)

    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=img_size,
        batch_size=batch_size,
        class_mode='categorical'
    )

    test_generator = test_datagen.flow_from_directory(
        test_dir,
        target_size=img_size,
        batch_size=batch_size,
        class_mode='categorical',
        shuffle=False
    )

    return train_generator, test_generator

def classify_tnds_with_gso_inceptionv3(train_dir, test_dir):
    """Classification of TNDs using the InceptionV3 model with GSO."""
    train_generator, test_generator = get_data_generators(train_dir, test_dir, IMG_SIZE, BATCH_SIZE)

    dropout_factors = [0.1]
    learning_rates = [0.01]

    best_accuracy = 0
    best_params = {}

    for dropout in dropout_factors:
        for lr in learning_rates:
            print(f'Training model with Dropout: {dropout}, Learning Rate: {lr}')
            model = create_inceptionv3_model(dropout)
            optimizer = SGD(learning_rate=lr)
            model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

            # Callback to save the best model
            checkpoint = ModelCheckpoint(
                'best_model.keras',  # Path to save the best model
                monitor='val_accuracy',       # Monitor validation accuracy
                save_best_only=True,          # Save only the best model
                mode='max',                   # Save when val_accuracy is maximized
                verbose=1                     # Print when a model is saved
            )

            model.fit(
                train_generator,
                epochs=EPOCHS,
                validation_data=test_generator,
                callbacks=[checkpoint]  # Pass the checkpoint callback here
            )

            loss, accuracy = model.evaluate(test_generator)
            print(f'Accuracy: {accuracy:.4f}')

            if accuracy > best_accuracy:
                best_accuracy = accuracy
                best_params = {'dropout_factor': dropout, 'learning_rate': lr, 'model': model}

    print("Best Dropout Factor:", best_params['dropout_factor'])
    print("Best Learning Rate:", best_params['learning_rate'])
    print("Best Accuracy:", best_accuracy)

    # Load the best model for evaluation
    best_model = models.load_model('best_model.keras')

    predictions = best_model.predict(test_generator)
    predicted_classes = np.argmax(predictions, axis=1)

    cm = confusion_matrix(test_generator.classes, predicted_classes)
    print("Confusion Matrix:")
    print(cm)

    # Compute metrics
    accuracy = np.trace(cm) / np.sum(cm)
    sensitivity = cm[1, 1] / (cm[1, 1] + cm[1, 0]) if (cm[1, 1] + cm[1, 0]) != 0 else 0
    specificity = cm[0, 0] / (cm[0, 0] + cm[0, 1]) if (cm[0, 0] + cm[0, 1]) != 0 else 0
    precision = cm[1, 1] / (cm[1, 1] + cm[0, 1]) if (cm[1, 1] + cm[0, 1]) != 0 else 0
    f_measure = 2 * (precision * sensitivity) / (precision + sensitivity) if (precision + sensitivity) != 0 else 0

    print(f"Accuracy: {accuracy:.4f}")
    print(f"Sensitivity: {sensitivity:.4f}")
    print(f"Specificity: {specificity:.4f}")
    print(f"F-measure: {f_measure:.4f}")

    report = classification_report(test_generator.classes, predicted_classes, target_names=['BENIGN', 'MALIGNANT'])
    print(report)

# Run classification of TNDs with InceptionV3 using GSO
classify_tnds_with_gso_inceptionv3(TRAIN_DIR, TEST_DIR)
