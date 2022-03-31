import json
   # Opening JSON file
f = open('sample.json',)   
# returns JSON object as a dictionary
new_review = json.load(f)

author = new_review["author"]
project = new_review["project"]
subject = new_review["subject"]
files = []
for file in new_review["files"]:
    files.append(file["path"])

print(author)
print(project)
print(subject)
print(files)
# Closing file
f.close()