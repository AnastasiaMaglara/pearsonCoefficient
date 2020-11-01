from math import sqrt
import statistics
from sklearn.metrics import mean_absolute_error
import copy
import prediction

AVERAGE_UNCOMPUTABLE = (-1000)
PEARSON_UNCOMPUTABLE_NO_COMMON = (-1001)
PEARSON_UNCOMPUTABLE_ZERO_VARIANCE = (-1002)
MEAN_ABSOLUTE_ERROR_UNCOMPUTABLE = (-1004)
ROOT_MEAN_SQUARE_ERROR_UNCOMPUTABLE = (-1005)

def pearsonSim(x, avg_x, y, avg_y):
    if ((avg_x ==  AVERAGE_UNCOMPUTABLE) or (avg_y == AVERAGE_UNCOMPUTABLE)):
      return PEARSON_UNCOMPUTABLE_NO_COMMON
    nominator = 0
    denominatorX = 0
    denominatorY = 0
    count = 0
    for key in x:
        if key in y:
            xdiff = x[key] - avg_x
            ydiff = y[key] - avg_y
            nominator += xdiff * ydiff
            denominatorX += xdiff * xdiff
            denominatorY += ydiff * ydiff
            count += 1

    if (count == 0):
      return PEARSON_UNCOMPUTABLE_NO_COMMON
    else:
      if (denominatorX * denominatorY == 0):
        return PEARSON_UNCOMPUTABLE_ZERO_VARIANCE
      else:
        return nominator / sqrt(denominatorX * denominatorY)


def avgRating(ratingDict):
  if (len(ratingDict) == 0):
    return AVERAGE_UNCOMPUTABLE
  return statistics.mean(ratingDict[k] for k in ratingDict)

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

def predictionsCalculation(ratings, numUsers, usersWithRating, hiddenItems):
    arrayOfValue = []
    ratingsUpdated = copy.deepcopy(ratings)
    for i, u in enumerate(usersWithRating):
        arrayOfValue.append(ratings[u][hiddenItems[i]])
        del ratingsUpdated[u][hiddenItems[i]]

    newAvgUserRatings = []
    for i in range(0, numUsers):
        newAvgUserRatings.insert(i, avgRating(ratingsUpdated[i]))

    newSim = [[0 for x in range(numUsers)] for y in range(numUsers)]
    for i in range(0, numUsers):
        for j in range(0, numUsers):
            newSim[i][j] = pearsonSim(ratingsUpdated[i], newAvgUserRatings[i], ratingsUpdated[j], newAvgUserRatings[j])

    arrayOfPredictions = []
    for i, u in enumerate(usersWithRating):
        arrayOfPredictions.append(prediction.predictRatingPearson(ratingsUpdated, newAvgUserRatings, newSim, numUsers, u, hiddenItems[i]))

    # computes mean absolute error
    # from sklearn.metrics:
    print(mean_absolute_error(arrayOfValue, arrayOfPredictions))

    print(mae(arrayOfValue, arrayOfPredictions))

    # computes RMS Errors
    print(RMSError(arrayOfValue, arrayOfPredictions))
