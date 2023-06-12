import sys
import getCsv
import compare_csv

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Usage: python createNCompare.py <path to image> <is image scanned>")
        sys.exit(1)
    else:
        print("Running...")
        csv = getCsv.getCsv(sys.argv[1], sys.argv[2])
        compare_csv.compare("outputs/" + sys.argv[1][7:-4] + ".csv", sys.argv[1][:-4] + ".csv")
        print("Done!")