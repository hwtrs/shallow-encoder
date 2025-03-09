def main():
    infile = open("test.txt", "r")
    lines = infile.readlines()
    for i in lines:
        print(f"{i}", end='')

if __name__ == "__main__":
    main()