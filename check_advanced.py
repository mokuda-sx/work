#!/usr/bin/env python3
import json

with open('test_output/advanced_swimlane.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print('Swimlane Layout:')
print(f'  Title: {data.get("title")}')
print(f'  Objects: {len(data.get("objects", []))}')
print()
print('色分け:')
colors = {}
for obj in data.get('objects', []):
    color = obj.get('fill_color', 'unknown')
    colors[color] = colors.get(color, 0) + 1

for color, count in sorted(colors.items()):
    print(f'  {color}: {count} 個')
