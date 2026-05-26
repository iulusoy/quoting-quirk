import argparse
import random
from pathlib import Path

from datasets import load_dataset


def load_train_split():
    ds = load_dataset("Abirate/english_quotes")
    return ds["train"]


def all_tags_from_train(train):
    return sorted({tag for example in train for tag in example["tags"]})


def tags_from_workspace_files():
    candidates = [Path("tags.txt"), Path("src/tags.txt")]
    for path in candidates:
        if path.exists():
            with path.open("r", encoding="utf-8") as f:
                tags = [line.strip() for line in f if line.strip()]
            if tags:
                return sorted(set(tags))
    return []


def filtered_quotes_by_tag(train, tag):
    normalized = tag.strip().lower()
    return [
        example
        for example in train
        if normalized in {item.lower() for item in example["tags"]}
    ]


def main():
    parser = argparse.ArgumentParser(
        description="Return a random quote from Abirate/english_quotes for a given tag."
    )
    parser.add_argument("tag", nargs="?", help="Tag to filter by, e.g. humor")
    parser.add_argument(
        "--list-tags",
        action="store_true",
        help="Print all available tags and exit.",
    )
    args = parser.parse_args()

    train = load_train_split()
    dataset_tags = all_tags_from_train(train)

    if args.list_tags:
        print("Available tags:")
        for tag in dataset_tags:
            print(tag)
        return

    if not args.tag:
        print("Missing tag. Provide one, for example: humor")
        print("Tip: run with --list-tags to see all options.")
        raise SystemExit(1)

    matches = filtered_quotes_by_tag(train, args.tag)
    if not matches:
        suggestion_source = tags_from_workspace_files() or dataset_tags
        suggestions = ", ".join(suggestion_source[:10])
        print(f"No quotes found for tag '{args.tag}'.")
        print(f"Try one of: {suggestions}")
        raise SystemExit(2)

    pick = random.choice(matches)
    print(f"[{args.tag}] {pick['quote']} — {pick['author']}")


if __name__ == "__main__":
    main()
