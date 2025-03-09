import sys
import numpy

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    with open(filename, "r") as f:
        input_data = f.read()

    print(f"Reading file: {filename}")
    print(f"Contents:\n{input_data}")

if __name__ == "__main__":
    main()