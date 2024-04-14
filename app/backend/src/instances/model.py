import os

from transformers import (AutoModelForSequenceClassification, AutoTokenizer,
                          TextClassificationPipeline)


class Classifier:
    MODEL_NAME = "./saved_model"
    absolute_path = os.path.abspath(MODEL_NAME)
    all_classes = {
        "act": 1,
        "application": 1,
        "arrangement": 1,
        "bill": 1,
        "contract": 1,
        "contract offer": 1,
        "determination": 1,
        "invoice": 1,
        "order": 1,
        "proxy": 1,
        "statute": 1,
    }

    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(self.absolute_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            self.absolute_path,
        )
        # self.pipe = TextClassificationPipeline(model=self.model, tokenizer=self.tokenizer)

    def truncate_and_encode(self, text, max_length=512):
        # Обрезаем и кодируем текст
        inputs = self.tokenizer.encode_plus(
            text,
            max_length=max_length,  # Указываем максимальную длину
            truncation=True,
            return_tensors="pt",  # Возвращаем тензор PyTorch
        )
        return inputs

    def predict(self, text):
        # кодируем текст
        inputs = self.truncate_and_encode(text)

        # делаем предикт
        outputs = self.model(**inputs)

        # возвращаем класс с наибольшей вероятностью и саму вероятность
        logits = outputs["logits"]
        predicted_class_index = int(logits.argmax())
        predicted_class_probability = logits.softmax(dim=-1)[0][
            predicted_class_index
        ].item()
        predicted_class_label = self.model.config.id2label[predicted_class_index]

        return [predicted_class_label, predicted_class_probability]

    def validate_docs(self, predictions, classes_dict=all_classes):
        class_counts = {label: predictions.count(label) for label in predictions}

        differences = {}

        # Находим ключи, которые есть только в одном из словарей
        unique_keys_dict1 = set(classes_dict.keys()) - set(class_counts.keys())
        unique_keys_dict2 = set(class_counts.keys()) - set(classes_dict.keys())

        # Добавляем уникальные ключи в словарь различий
        differences.update(
            {key: (classes_dict[key], None) for key in unique_keys_dict1}
        )
        differences.update(
            {key: (None, class_counts[key]) for key in unique_keys_dict2}
        )

        # Находим ключи, которые есть в обоих словарях, но с разными значениями
        common_keys = set(classes_dict.keys()) & set(class_counts.keys())
        different_values = {
            key: (classes_dict[key], class_counts[key])
            for key in common_keys
            if classes_dict[key] != class_counts.get(key)
        }

        # Добавляем ключи с разными значениями в словарь различий
        differences.update(different_values)

        result = []
        if differences:
            result.append("Есть ошибки в следующих классах:")
            for key, value in differences.items():
                if value[1] is None:
                    result.append(
                        str(key)
                        + ": нет ни одного файла, ожидалось получить: "
                        + str(value[0])
                    )
                elif value[0] is None:
                    result.append(
                        str(key)
                        + ": файлы данного класса не ожидались, получено: "
                        + str(value[1])
                    )
                else:
                    result.append(
                        str(key)
                        + ": файлов ожидалось: "
                        + str(value[0])
                        + ", получено: "
                        + str(value[1])
                    )
        else:
            result.append("Документы прошли валидацию и успешно загружены!")
        return result
        # return "\n".join(result)

    def predict_documents(self, texts, classes_dict=all_classes):
        predictions = []
        for text in texts:
            prediction = self.predict(text)
            predictions.append(prediction[0])
        class_counts = {label: predictions.count(label) for label in predictions}

        differences = {}

        # Находим ключи, которые есть только в одном из словарей
        unique_keys_dict1 = set(classes_dict.keys()) - set(class_counts.keys())
        unique_keys_dict2 = set(class_counts.keys()) - set(classes_dict.keys())

        # Добавляем уникальные ключи в словарь различий
        differences.update(
            {key: (classes_dict[key], None) for key in unique_keys_dict1}
        )
        differences.update(
            {key: (None, class_counts[key]) for key in unique_keys_dict2}
        )

        # Находим ключи, которые есть в обоих словарях, но с разными значениями
        common_keys = set(classes_dict.keys()) & set(class_counts.keys())
        different_values = {
            key: (classes_dict[key], class_counts[key])
            for key in common_keys
            if classes_dict[key] != class_counts.get(key)
        }

        # Добавляем ключи с разными значениями в словарь различий
        differences.update(different_values)

        result = []
        if differences:
            result.append("Есть ошибки в следующих классах:")
            for key, value in differences.items():
                if value[1] is None:
                    result.append(
                        str(key)
                        + ": нет ни одного файла, ожидалось получить: "
                        + str(value[0])
                    )
                elif value[0] is None:
                    result.append(
                        str(key)
                        + ": файлы данного класса не ожидались, получено: "
                        + str(value[1])
                    )
                else:
                    result.append(
                        str(key)
                        + ": файлов ожидалось: "
                        + str(value[0])
                        + ", получено: "
                        + str(value[1])
                    )
        else:
            result.append("Всё ОК!")

        return "\n".join(result)

    # def predict(self, text: str):
    #     prediction = self.pipe(text, return_all_scores=False)
    #     return prediction[0]['label']


classifier = Classifier()
