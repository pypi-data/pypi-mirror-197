import sys
import csv

def main():
    reader = csv.reader(sys.stdin)
    writer = csv.writer(sys.stdout)

    for row in reader:
        # Easier to use the del operator, but in case pivot decides to add more columns, or changes whatever
        new_row = []
        for i, val in enumerate(row):
            if i == 2 or i == 9:
                continue

            new_row.append(val)
        writer.writerow(new_row)


if __name__ == "__main__":
    main()

