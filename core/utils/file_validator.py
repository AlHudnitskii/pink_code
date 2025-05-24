def file_is_valid(file, file_name) -> bool:
    if not file_name.lower().endswith(".txt"):
        return False

    file.seek(0)
    fst_line = file.readline().decode('utf-8')
    if "|" not in fst_line:
        return False
    return True