import numpy as np

# [[Q or R message],[time of reception],[incoming node]]
def prune_feed(feedList, indNode, timeNow, tauMax):

    # find and remove all the old (stale) feeds 
    lenFeedList = len(feedList[indNode][0])
    for indFeed in range(0, lenFeedList):
        # check if old feed
        if (timeNow-feedList[indNode][1][lenFeedList-indFeed-1])>tauMax:
            # remove all the record of lenFeedList-indFeed
            del feedList[indNode][0][lenFeedList-indFeed-1]
            del feedList[indNode][1][lenFeedList-indFeed-1]
            del feedList[indNode][2][lenFeedList-indFeed-1]
            del feedList[indNode][3][lenFeedList-indFeed-1]

    return feedList
