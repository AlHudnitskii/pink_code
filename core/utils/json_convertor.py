def read_and_convert_file_to_json(file, problem_id):
    testcases = []
    try:
        file.seek(0)
        for line in file:
            row = line.decode('utf-8').strip().split("|")
            if len(row) != 2:
                return False
            input_data, output_data = row
            if not input_data or not output_data:
                return False
            if output_data == "''":
                output_data = ""
                
            testcases.append({
                "problem_id": problem_id,
                "input_data": input_data,
                "expected_output": output_data
            })
    except Exception:
        return False
    return testcases