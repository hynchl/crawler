import json
import re
import csv

data = None
with open('ridibooks.json', 'r', encoding='UTF-8-sig') as f:
    data = json.load(f)

texts = [datum['content'] for datum in data]

result = []
for text in texts:
    seperated = re.split('[\n"]', text)
    result += seperated

keyword_to_filter = ["펼쳐보기", "작품소개", "책 속에서", ""]
result = [r for r in result if not (r in keyword_to_filter)]

print("문장 수 : {}".format(len(result)))

with open('output.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for r in result:
        print(r)
        writer.writerow([r])