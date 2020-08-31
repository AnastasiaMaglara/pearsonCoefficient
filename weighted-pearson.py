import statistics
from math import sqrt
import prediction

NUM_OF_PARAMETERS = 6
AVERAGE_UNCOMPUTABLE = (-1000)
PEARSON_UNCOMPUTABLE_NO_COMMON = (-1001)
PEARSON_UNCOMPUTABLE_ZERO_VARIANCE = (-1002)

def pearsonSim(x, avg_x, y, avg_y, w):
    if ((avg_x ==  AVERAGE_UNCOMPUTABLE) or (avg_y == AVERAGE_UNCOMPUTABLE)):
      return PEARSON_UNCOMPUTABLE_NO_COMMON
    nominator = 0
    denominatorX = 0
    denominatorY = 0
    count = 0
    for i,key in enumerate(x):
        if i > NUM_OF_PARAMETERS:
            i = i / NUM_OF_PARAMETERS
        if key in y:
           xdiff = x[key] - avg_x
           ydiff = y[key] - avg_y
           nominator += w[i] * xdiff * ydiff
           denominatorX += w[i] * xdiff * xdiff
           denominatorY += w[i] * ydiff * ydiff
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

weights= [0.2, 0.2, 0.1, 0.1, 0.2, 0.2]
numUsers = 10
ratings = [dict() for x in range(numUsers)]

# read <userid, itemid, rating> triples from dataset
ratings[1][10] = 4;
ratings[1][20] = 5;
ratings[1][30] = 4;
ratings[1][40] = 4;
ratings[1][50] = 5;
ratings[1][60] = 5;
ratings[2][10] = 3;
ratings[2][20] = 5;
ratings[2][30] = 4;
ratings[2][40] = 3;
ratings[2][50] = 5;
ratings[2][60] = 5;

avgUserRatings = []
for i in range(0, numUsers):
  avgUserRatings.insert(i, avgRating(ratings[i]))
print(avgUserRatings)
print(pearsonSim(ratings[1], avgUserRatings[1], ratings[2], avgUserRatings[2],weights))

sim=[[0 for x in range(numUsers)]for y in range(numUsers)]
for i in range(0, numUsers):
    for j in range(0, numUsers):
       sim[i][j] = pearsonSim(ratings[i], avgUserRatings[i], ratings[j], avgUserRatings[j], weights)

print(prediction.predictRatingPearson(ratings, avgUserRatings, sim , numUsers, 2, 20))

