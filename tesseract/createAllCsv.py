import os
import getCsv
import compare_csv

def readFile(dir, file):
    if file.endswith(".jpg"):
        print("Get csv of " + dir + "/" + file + "...")
        csv = getCsv.getCsv("images/" + dir + "/" + file)
        print("Done!")
        print("Compare csv of " + dir + "/" + file + "...")
        print("Done!")
        print("Compare csv of " + "outputs/" + dir + "/" + file[:-4] + ".csv", "images/" + dir + "/" + file[:-4] + ".csv")
        return compare_csv.compare("outputs/" + dir + "/" + file[:-4] + ".csv", "images/" + dir + "/" + file[:-4] + ".csv")
        # break
    return 0


def createAllCsv():
    nbFiles = 0
    totalPercentage = 0
    for dir in os.listdir("images/"):
        print("dir : ", dir)
        for sub in os.listdir("images/" + dir):
            if os.path.isdir(sub):
                for file in os.listdir("images/" + dir + "/" + sub):
                    nbFiles += 1
                    totalPercentage += readFile(dir + "/" + sub, file)
            else:
                nbFiles += 1
                totalPercentage += readFile(dir, sub)

    print("Total percentage: " + str(totalPercentage/nbFiles))


createAllCsv()