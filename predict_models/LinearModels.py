from predict_models.core import PredictModel
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer

from .utils import Normalizer
import numpy as np


class LinearModel(PredictModel):
    def __init__(self, model, normalize=False):
        self.model = model
        self.normalize = normalize
        self._normalizer = Normalizer()
        self.vectorizer = TfidfVectorizer(max_features=5000)

    def fit(self, X, y):
        self.model.fit(X, y)

    def fit_extractor(self, texts):
        if self.normalize:
            texts = self._normalizer.normalize(texts)
        self.vectorizer.fit(texts)

    def predict(self, X):
        predictions = self.model.predict_proba(X)
        return list(enumerate(predictions[0]))

    def predict_features(self, text):
        if self.normalize:
            texts = self._normalizer.normalize([text])
        else:
            texts = [text]
        return self.vectorizer.transform(texts)

    def prepare_features(self, texts):
        if self.normalize:
            texts = self._normalizer.normalize(texts)
        for f in self.vectorizer.transform(texts):
            yield np.array(f.todense())


