import glob
import cv2


# initialize the index dictionary to store the image name
# and corresponding histograms and the images dictionary
# to store the images themselves
index = {}
images = {}


# loop over the image paths
for imagePath in glob.glob("uploads" + "/*"):
    # extract the image filename (assumed to be unique) and
    # load the image, updating the images dictionary
    filename = imagePath[imagePath.rfind("/") + 1:]
    image = cv2.imread(imagePath)
    images[filename] = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # extract a 3D RGB color histogram from the image,
    # using 8 bins per channel, normalize, and update
    # the index
    hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8],
                        [0, 256, 0, 256, 0, 256])
    hist = cv2.normalize(hist).flatten()
    index[filename] = hist


methodName = "Chi-Squared"
method = cv2.cv.CV_COMP_CHISQR


def getMatches():
    results = {}
    reverse = False

    # # if we are using the correlation or intersection
    # # method, then sort the results in reverse order
    # if methodName in ("Correlation", "Intersection"):
    #     reverse = True

    # loop over the index
    for (k, hist) in index.items():
        # compute the distance between the two histograms
        # using the method and update the results dictionary
        d = cv2.compareHist(index["doge.png"], hist, method)
        results[k] = d

    # sort the results
    results = sorted([(v, k) for (k, v) in results.items()], reverse=reverse)

    print("the method is :----" + methodName)

    sorted_list = []
    # loop over the results
    for (i, (v, k)) in enumerate(results):
        # show the result
        sorted_list.append(str(k))
        # print sorted_list(i)
        print "name : " + str(k) + " value :" + str(v)
    return sorted_list[1:]
