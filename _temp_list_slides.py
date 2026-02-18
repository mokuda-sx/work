import json
data = json.load(open('refs/sx/sx_ai_callcenter/analysis.json', encoding='utf-8'))
for s in data['slides']:
    print(f"Slide {s['index']}: {s.get('title', '(no title)')}")
