import csv

with open("members.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    print(f"{'First Name':<20} {'Last Name':<20}")
    print("-" * 40)
    for row in reader:
        print(f"{row['first_name']:<20} {row['last_name']:<20}")
