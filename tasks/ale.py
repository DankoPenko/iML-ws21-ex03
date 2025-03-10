import sys
sys.path.insert(0, ".")

import pandas as pd
import numpy as np

from utils.dataset import Dataset
from utils.styled_plot import plt


def get_bounds(X, s, n_intervals=100):
    """
    Calculates interval bounds given a X's min and max values.
    Only values in the s-th column are considered.
    
    Parameters:
        X (np.array with shape (num_instances, num_features)): Input data.
        s (int): Index of the feature x_s.
        n_intervals (int): Number of intervals.
        
    Returns:
        bounds (list): Values of bounds with `n_intervals`+1 entries.
    """

    bounds = []

    values = (X[:,s])

    min_val = np.min(values)
    max_val = np.max(values)

    return np.linspace(min_val, max_val, n_intervals+1)

def calculate_ale(model, X, s, n_intervals=100, centered=False):
    """
    Compute the accumulated local effect of a numeric continuous feature.
    
    Parameters:
        model: Classifier which has a predict method.
        X (np.array with shape (num_instances, num_features)): Input data.
        s (int): Index of the feature x_s.
        n_intervals (int): How many intervals should be used.
        centered (bool): Whether to return uncentered or centered ALE.
        
    Returns:
        bounds (list): See function `get_bounds`.
        ale (list with `n_intervals` entries): Values of ALE.
    """
    bounds = get_bounds(X, s, n_intervals)
    ale = []
    i = 0
    for low, high in zip(bounds, bounds[1:]):
        observations = [value for value in X[:,s] if (high >= value >= low)]
        z_k_minus_one = np.min(observations, initial=0)
        z_k = np.max(observations, initial=0)
        X_min = X.copy()
        X_min[:,s] = z_k_minus_one
        # X_min[:, s] = low
        X_max = X.copy()
        X_max[:,s] = z_k
        # X_max[:, s] = high

        max_pred = model.predict(X_max)
        min_pred = model.predict(X_min)

        diff = max_pred - min_pred
        diff = np.sum(diff)
        diff /= len(observations)

        ale.append(diff)
    # print(ale[-1])
    return bounds, ale


def prepare_ale(model, X, s, n_intervals=100, centered=False):
    """
    Uses `calculate_ale` to prepare x and y data, which can be used
    by matplotlib directly.
    
    Parameters:
        model: Classifier which has a predict method.
        X (np.array with shape (num_instances, num_features)): Input data.
        s (int): Index of the feature x_s.
        n_intervals (int): How many intervals should be used.
        centered (bool): Whether to return uncentered or centered ALE.  
        
    Returns:
        x (list or 1D np.ndarray): Centers of two bounds. `n_intervals` entries.
        y (list or 1D np.ndarray): ALE values. `n_intervals` entries.
    """

    return None, None
        
        
if __name__ == "__main__":
    dataset = Dataset("wheat_seeds.csv", [5,6,7], [2], normalize=True, categorical=False)
    (X_train, y_train), (X_test, y_test) = dataset.get_data()
    
    from sklearn import ensemble
    model = ensemble.RandomForestRegressor()
    model.fit(X_train, y_train)
    X = dataset.X
    s = 1

    # len_X =

    # print(X[:,1][-3:])

    print("Run `get_bounds` ...")
    print(get_bounds(X, 0, n_intervals=4))

    # print("Plot ...")
    # plt.subplots(cols=len(n_intervals), rows=2, sharey=True)
    # for row_id, centered in enumerate([False, True]):
    #     for col_id, k in enumerate(n_intervals):
    #
    #         plt.subplot(2, len(n_intervals), col_id+1+len(n_intervals)*row_id)
    #         plt.title(f"{k} bins")
    #         plt.xlabel(dataset.get_input_labels(s))
    #         if col_id == 0:
    #             centered_text = ""
    #             if not centered:
    #                 centered_text = "Uncentered"
    #
    #             plt.ylabel(f"{centered_text} ALE [{dataset.get_output_label()}]")
    #
    #         x, y = prepare_ale(model, X, s, n_intervals=k, centered=centered)
    #         plt.plot(x, y, linewidth=0.5)
    #
    # plt.tight_layout(pad=0.75)
    # plt.show()