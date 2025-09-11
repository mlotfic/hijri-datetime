def json_files_dict():
    """Check if response file exists for a given month/year and load it"""
    json_dir = "debug_responses_month"
    dict_list = []
    # Loop through files in the directory
    for filename in os.listdir(json_dir):
        if filename.endswith(".json"):  # only process JSON
            file_path = os.path.join(json_dir, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    print(f"✅ Loaded {filename} Len: {len(data)}:")
                    # do your processing here
                    dict_list.append(process_date_data(data))
                except json.JSONDecodeError as e:
                    print(f"❌ Failed to parse {filename}: {e}")
    return pd.Dateframe(dict_list)