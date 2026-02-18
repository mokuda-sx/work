import json

data = json.loads(open('01_content.json', encoding='utf-8').read())
objects = data.get('objects', [])

arrow_count = sum(1 for obj in objects if obj.get('type') == 'arrow')
box_count = sum(1 for obj in objects if obj.get('type') in ('box', 'rect'))
text_count = sum(1 for obj in objects if obj.get('type') == 'text')

print(f'Arrow objects in JSON: {arrow_count}')
print(f'Box objects in JSON: {box_count}')
print(f'Text objects in JSON: {text_count}')
print(f'Total objects: {len(objects)}')

# List all arrow objects
print('\nArrow details:')
for i, obj in enumerate(objects):
    if obj.get('type') == 'arrow':
        print(f'  {i}: left={obj.get("left")}, top={obj.get("top")}, width={obj.get("width")}, height={obj.get("height")}')
