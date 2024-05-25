from traffic import load_data
import sys

if len(sys.argv) not in [2, 3]:
    sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
load_data(sys.argv[1])
