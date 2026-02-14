"""Validate existing JSON files against schemas. Run from work/ directory."""
import json
import jsonschema
import glob
import os

base = os.path.dirname(os.path.abspath(__file__))
schemas_dir = os.path.join(base, "schemas")
slides_base = os.path.join(base, "slides")


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


outline_schema = load_json(os.path.join(schemas_dir, "outline.schema.json"))
recipe_schema  = load_json(os.path.join(schemas_dir, "recipe.schema.json"))
tier2_schema   = load_json(os.path.join(schemas_dir, "tier2.schema.json"))

errors = []
passed = []


def validate(data, schema, label):
    try:
        jsonschema.validate(data, schema)
        passed.append(f"OK  {label}")
    except jsonschema.ValidationError as e:
        path_str = " > ".join(str(p) for p in e.path) or "(root)"
        errors.append(f"NG  {label}\n    {e.message}\n    at: {path_str}")


# Outlines
for path in glob.glob(os.path.join(slides_base, "*", "outline.json")):
    label = "outline: " + os.path.basename(os.path.dirname(path))
    validate(load_json(path), outline_schema, label)

# Recipes
for path in glob.glob(os.path.join(slides_base, "*", "recipes", "*.recipe.json")):
    label = "recipe:  " + os.path.basename(path)
    validate(load_json(path), recipe_schema, label)

# Tier 2
for path in glob.glob(os.path.join(slides_base, "*", "slides", "*.json")):
    label = "tier2:   " + os.path.basename(path)
    validate(load_json(path), tier2_schema, label)


print(f"\n{'='*60}")
print(f"PASSED: {len(passed)}  |  ERRORS: {len(errors)}")
print(f"{'='*60}")
if errors:
    print("\nFailed:")
    for e in errors:
        print(e)
else:
    print("\nAll files valid!")
