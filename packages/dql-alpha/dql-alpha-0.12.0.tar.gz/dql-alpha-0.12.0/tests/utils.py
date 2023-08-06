import asyncio


def insert_entries(data_storage, entries):
    """
    Takes a list of entries and inserts them synchronously.

    This assumes that, for every entry in entries, all of its parent
    directories also have an entry.
    """
    entries_by_path = [(tuple(e["path"].split("/")), e) for e in entries]
    entries_by_path.sort(key=lambda e: (len(e[0]), not e[1]["is_dir"]))

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        dir_ids = {(): asyncio.run(data_storage.insert_root())}
        for path_parts, entry in entries_by_path:
            entry = {
                **entry,
                "parent_id": dir_ids[path_parts[:-1]],
            }
            node_id = loop.run_until_complete(data_storage.insert_entry(entry))
            if entry["is_dir"]:
                dir_ids[path_parts] = node_id
    finally:
        asyncio.set_event_loop(None)
        loop.close()
