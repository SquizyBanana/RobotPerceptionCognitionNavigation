

file = open("Assignment 1A data\MT_037004D1_001-000.txt","r")

raw_strings = file.readlines()

for i in range(12):
    raw_strings.pop(0)

print(raw_strings[0])
raw_strings.pop(0)
strings = []
data = []
for i in range(len(raw_strings)):
    strings.append(raw_strings[i].split("\t"))
    
print(strings[0])