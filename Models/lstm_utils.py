import numpy as np
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt


def plot_history(history, title):
    # summarize history for accuracy

    legend = ['acc']
    legend_2 = ['loss']
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Accuracy')
    ax2.set_ylabel('Loss')
    if "acc" in history.history.keys():
        ax1.plot(history.history['acc'], color='g')
    ax2.plot(history.history['loss'], color='r')
    ax1.set_title(title)

    if "val_loss" in history.history.keys():
        ax2.plot(history.history['val_loss'], color='pink')
        legend_2.append('val_loss')

    if "val_acc" in history.history.keys():
        ax1.plot(history.history['val_acc'], color='b')
        legend.append('val_acc')

    ax1.legend(legend, loc='upper left')
    ax2.legend(legend_2, loc='upper right')

    plt.show()


def scale_column(x, column=0):
    """
    Doesn't mutate the original array
    """
    timesteps = x.shape[0]
    mms = MinMaxScaler()
    x1 = x.copy()
    # The volume column has index 0
    x1[:, column] = mms.fit_transform(
        x1[:, column].reshape(timesteps, 1)).reshape(timesteps, )
    return x1


def check_rsi(rsi): return 0 if rsi is np.nan or (
    70 > rsi > 30) else (-1 if rsi < 30 else 1)


"""
Traditionally, RSI > 70 = Overbought, RSI < 30 Oversold
We transform the column to -1, 0, 1,
"""
vectorized_check_rsi = np.vectorize(check_rsi)


def rsi_transformer(x, column):
    x2 = x.copy()
    rsi_column = x2[:, column]
    x2[:, 4] = vectorized_check_rsi(rsi_column)
    return x2


def check_dmi(x):
    """https://capital.com/average-directional-index
    According to this,
    if dmi < 20 -> 0
    dmi > 20 -> 1
    40 > dmi > 20 -> 1
    dmi > 40 -> 2
    dmi > 50 -> 3
    """

    if x is np.nan:
        return 0
    elif x > 50:  # Very Strong Trend
        return 3
    elif x > 40:  # Strong Trend
        return 2
    elif x > 20:  # Trend
        return 1
    else:  # No Trend
        return 0


vectorized_check_dmi = np.vectorize(check_dmi)


def dmi_transformer(x, column=9):
    x2 = x.copy()
    dmi_26_column = x2[:, column]
    x2[:, column] = vectorized_check_dmi(dmi_26_column)
    return x2
