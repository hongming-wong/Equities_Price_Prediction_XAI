import numpy as np
import typing
import numpy.typing as npt
from sklearn.pipeline import Pipeline
import sklearn.tree
import random
"""
The core idea:
We want to explain which features are the most important in determining the outcome of the model.

Given a data point with N features and T timesteps:
- We pertube a combination of features
- For a given feature, we pertubate a range that has length that is > 50% of T

We can pertube in the following ways:
- Setting the range to the sample mean
- Setting the range to 0
- Setting the range to random noises


After obtaining the samples, we feed them into the black box models and get the labels. 

We reshapre the samples from shape (N, T) to (N x T, 1) and feed into a decision tree. 
We use the decision tree to interpret our model
"""


class Explainer:
    def __init__(self, model,
                 data_point: np.array,
                 surrogate_model):
        self.model = model
        self.data_point = data_point
        # self.output = model.predict(np.array([data_point]))
        self.all_datapoints = None
        self.surrogate_model = surrogate_model

    def explain(self, pipeline):
        data_points = np.array(self.all_datapoints)
        labels = self.model.predict(data_points)

        data = None
        for f in pipeline:
            data = f(data_points)
        self.surrogate_model.fit(data, labels)

    def generate_neigbouring_datapoints(self):
        functions = [self._turn_off, self._add_noise, self._mean]
        generated_datapoints = []

        cols = self.data_point.shape[1]

        for col in range(cols):
            for f in functions:
                generated_datapoints.extend(f(col))
        self.all_datapoints = generated_datapoints

    def _turn_off(self, column, threshold=0.5):
        timesteps = self.data_point.shape[0]
        results = []
        for i in range(0, timesteps):
            bound = i + int(timesteps * threshold)
            if bound > timesteps:
                break

            p = self.data_point.copy()
            p[i: bound, column] = 0
            results.append(p)

        return results

    def _add_noise(self, column, threshold=0.5):
        timesteps = self.data_point.shape[0]
        results = []
        col_mean = np.mean(self.data_point[:, column])
        for i in range(0, timesteps):
            bound = i + int(timesteps * 0.5)
            if bound > timesteps:
                break

            p = self.data_point.copy()
            p[i: bound, column] = [np.random.normal(
                loc=col_mean) for _ in range(i, bound)]
            results.append(p)

        return results

    def _mean(self, column, threshold=0.5):
        timesteps = self.data_point.shape[0]
        results = []
        col_mean = np.mean(self.data_point[:, column])
        for i in range(0, timesteps):
            bound = i + int(timesteps * 0.5)
            if bound > timesteps:
                break
            p = self.data_point.copy()
            p[i: bound, column] = col_mean
            results.append(p)

        return results


def shuffle(array):
    x = np.random.shuffle(array)
    return x


def flatten(array):
    result = []
    for i in array:
        result.append(i.flatten())
    return np.array(result)


if __name__ == '__main__':
    f11 = [0, 1, 2, 3, 4, 5, 6]
    f12 = [100, 200, 300, 400, 500, 600, 700]
    f13 = [100, 90, 80, 70, 60, 50, 40]

    f21 = [10, 9, 8, 7, 6]
    f22 = [400, 500, 600, 700, 800]
    f23 = [100, 110, 120, 130, 140]
    f24 = [0, 1, 0, 0, 0]

    sample_1 = np.transpose(np.array([f11, f12, f13]))
    sample_2 = np.transpose(np.array([f21, f22, f23, f24]))

    print(sample_1.shape)
    print(sample_2.shape)

    class Sample_Model:

        def predict(self, x):
            return [random.sample([0, 1], 1)[0] for i in range(len(x))]

    pipeline = [shuffle, flatten]

    exp = Explainer(model=Sample_Model(),
                    surrogate_model=sklearn.tree.DecisionTreeClassifier(
                        max_depth=3),
                    data_point=sample_1)
    exp.generate_neigbouring_datapoints()
    exp.explain(pipeline)

    print("sasas")
