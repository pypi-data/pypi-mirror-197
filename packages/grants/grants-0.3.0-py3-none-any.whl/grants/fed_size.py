import csv
import sys 
from grants import fieldnames

def main():

    reader = csv.reader(sys.stdin, dialect="excel")
    writer = csv.writer(sys.stdout)

    for row in reader:
        _row = [ "" for _ in range(fieldnames.FED_NUM_FIELDS)]
        for i in range(len(row)):
            _row[i] = row[i]
        
        writer.writerow(_row)

if __name__ == "__main__":
    main()
