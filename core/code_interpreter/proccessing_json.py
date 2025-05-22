import ast
import json

def proccess_result(result: str):
    print(f"proccess_result received: {result}")
    try:
        user_code = result[result.index("def"):result.index('[{\"')]
        json_start = result.rindex('"}}]') + 4
        json_part = result[json_start:].strip()
        result_dict = ast.literal_eval(json_part)
        result_dict["user_code"] = user_code.strip()
        print(f"proccess_result returning: {result_dict}") 
        return result_dict
    except (ValueError, SyntaxError) as e:
        print(f"proccess_result error: {e}") 
        return None