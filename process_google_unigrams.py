import sqlite3, glob
from collections import defaultdict
db_location = "./db/google_unigrams.db"

files = glob.glob("/Users/benicorp/Downloads/google*")[1:]

def count_ngrams(in_file, year_start=1998, year_end=2008):
    counts = defaultdict(int)
    with open(in_file) as f:
        for line in f:
            parts = line.strip().split("\t")
            if parts:
                word = parts[0].lower()
                year = int(parts[1])
                count = int(parts[2])
                if year >=year_start and year <= year_end and word.isalpha():
                    counts[word] += count
    with sqlite3.connect(db_location) as con:
        cur = con.cursor()
        cur.executemany("insert into google_unigrams values(?,?)", counts.iteritems())
            
            
for infile in files:
    count_ngrams(infile)