import statistics
from sklearn.metrics import mean_absolute_error
import copy
from math import sqrt
import prediction
import accuracy

NUM_OF_USERS = 100
AVERAGE_UNCOMPUTABLE = (-1000)
PEARSON_UNCOMPUTABLE_NO_COMMON = (-1001)
PEARSON_UNCOMPUTABLE_ZERO_VARIANCE = (-1002)

def predictionsCalculation(usersWithRating, hiddenItems):
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
    # from sklearn.metrics: print(mean_absolute_error(arrayOfValue, arrayOfPredictions))
    print(accuracy.mae(arrayOfValue, arrayOfPredictions))

    # computes RMS Errors
    print(accuracy.RMSError(arrayOfValue, arrayOfPredictions))

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


numUsers = NUM_OF_USERS
ratings = [dict() for x in range(numUsers)]

# read <userid, itemid, rating> triples from dataset
ratings[1][1] = 3;
ratings[1][2] = 5;
ratings[1][3] = 5;
ratings[1][4] = 1;
ratings[1][5] = 1;
ratings[2][1] = 4;
ratings[2][2] = 5;
ratings[2][3] = 5;
ratings[2][4] = 2;
ratings[2][5] = 3;
ratings[3][1] = 2;
ratings[3][2] = 5;
ratings[3][3] = 4;
ratings[3][4] = 1;
ratings[3][5] = 2;

avgUserRatings = []
for i in range(0, numUsers):
  avgUserRatings.insert(i, avgRating(ratings[i]))
#print(avgUserRatings)

sim=[[0 for x in range(numUsers)]for y in range(numUsers)]
for i in range(0, numUsers):
    for j in range(0, numUsers):
       sim[i][j] = pearsonSim(ratings[i], avgUserRatings[i], ratings[j], avgUserRatings[j])
#print(sim)

print(prediction.predictRatingPearson(ratings, avgUserRatings, sim , numUsers, 2, 2))
predictionsCalculation([2, 1, 3], [2, 4, 3])
