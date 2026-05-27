import argparse
import json
import random
from pathlib import Path

from datasets import load_dataset


LOCAL_CACHE_PATH = Path(".cache/english_quotes_train.json")


def load_train_from_local_cache(cache_path=LOCAL_CACHE_PATH):
    with cache_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def maybe_write_local_cache(train, cache_path=LOCAL_CACHE_PATH):
    if cache_path.exists():
        return
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    rows = [
        {"quote": row["quote"], "author": row["author"], "tags": row["tags"]}
        for row in train
    ]
    with cache_path.open("w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False)


def load_train_split(offline=False):
    if offline:
        if not LOCAL_CACHE_PATH.exists():
            raise FileNotFoundError(LOCAL_CACHE_PATH)
        return load_train_from_local_cache(LOCAL_CACHE_PATH)

    ds = load_dataset("Abirate/english_quotes")
    train = ds["train"]
    maybe_write_local_cache(train)
    return train


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
    matches = []
    for example in train:
        if any(normalized == item.lower() for item in example["tags"]):
            matches.append(example)
    return matches


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
    parser.add_argument(
        "--offline",
        action="store_true",
        help="Use local quote cache only (no network calls).",
    )
    args = parser.parse_args()

    try:
        train = load_train_split(offline=args.offline)
    except Exception as exc:
        if args.offline:
            print(
                "Offline mode failed: local cache not available. "
                "Run once without --offline to populate .cache/english_quotes_train.json."
            )
            raise SystemExit(3) from exc
        raise

    if args.list_tags:
        dataset_tags = all_tags_from_train(train)
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
        dataset_tags = all_tags_from_train(train)
        suggestion_source = tags_from_workspace_files() or dataset_tags
        suggestions = ", ".join(suggestion_source[:10])
        print(f"No quotes found for tag '{args.tag}'.")
        print(f"Try one of: {suggestions}")
        raise SystemExit(2)

    pick = random.choice(matches)
    print(f"[{args.tag}] {pick['quote']} — {pick['author']}")


if __name__ == "__main__":
    main()
