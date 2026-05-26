from datasets import load_dataset

ds = load_dataset("Abirate/english_quotes")

# Parse the dataset (train split)
train = ds["train"]

# List all available tags
all_tags = sorted(set(tag for example in train for tag in example["tags"]))
print(f"Number of unique tags: {len(all_tags)}")
print("All available tags:")
for tag in all_tags:
    print(f"  {tag}")

with open("tags.txt", "w") as f:
    f.write("\n".join(all_tags))
print("Tags written to tags.txt")

# Filter by tag and print the first three quotes
tag = "humor"
humor_quotes = [example for example in train if tag in example["tags"]]
print(f"\nFirst 3 quotes tagged '{tag}':")
for example in humor_quotes[:3]:
    print(f"  {example['quote']} — {example['author']}")
