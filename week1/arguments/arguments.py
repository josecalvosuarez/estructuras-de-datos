import sys

# sys.argv[0] is the script name
# sys.argv[1], sys.argv[2], ... are the arguments

if len(sys.argv) < 2:
    print("Please provide some arguments!")
else:
    print("Script name:", sys.argv[0])
    print("First argument:", sys.argv[1])

    if len(sys.argv) > 2:
        print("Second argument:", sys.argv[2])
