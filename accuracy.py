from math import sqrt

MEAN_ABSOLUTE_ERROR_UNCOMPUTABLE = (-1004)
ROOT_MEAN_SQUARE_ERROR_UNCOMPUTABLE = (-1005)
# Mean Absolute Error (MAE)
def mae(x, y):
    sum = 0
    for key, value in enumerate(x):
        sum = sum + (y[key]-x[key])

    if len(x) != 0:
        return sum / len(x)
    else:
        return MEAN_ABSOLUTE_ERROR_UNCOMPUTABLE

# Root-Mean-Square Error (RMS Error)
def RMSError(x, y):
    sum = 0
    for key, value in enumerate(x):
        sum = sum + (y[key] - x[key])**2

    if len(x) != 0:
        # print(mean_absolute_error(x, y))
        return sqrt(sum / len(x))
    else:
        return ROOT_MEAN_SQUARE_ERROR_UNCOMPUTABLE