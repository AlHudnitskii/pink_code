import subprocess
import json
#import custom_json_serializer
import logging

from celery import shared_task


logging.basicConfig(level=logging.INFO)

@shared_task
def run_user_code(user_id: str, user_code, test_cases_json):
    network_name = "leetcode_network"
    command = [
        'docker', 'run', '--rm', '--network', network_name,
        'code_interpreter_image', 'python', 'executor.py',
        user_id, user_code, json.dumps(test_cases_json)
    ]
    # command = [
    #     'docker', 'run', '--rm', '--network', network_name,
    #     'code_interpreter_image', 'python', 'executor.py',
    #     user_id, user_code, custom_json_serializer.serialize(test_cases_json)
    # ]
    

    logging.debug(f"{type(user_code)}, {type(test_cases_json)}")
    logging.info(f"Running command: {' '.join(command)}")

    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        logging.error(f"Command error: {result.stderr}")
        return {'error': result.stderr}
    else:
        logging.info(f"Command output: {result.stdout}")
        try:
            # Попробуем найти строку JSON в выводе
            output_lines = result.stdout.splitlines()
            json_output = None
            for line in output_lines:
                try:
                    json_output = json.loads(line)
                    break
                except json.JSONDecodeError:
                    continue

            if json_output is not None:
                logging.info(f"JSON output: {json_output}")
                return json_output
            else:
                raise json.JSONDecodeError("No valid JSON found", result.stdout, 0)

        except json.JSONDecodeError as e:
            logging.error(f"JSON decode error: {e} {result.stdout}")
            return {'error': f"JSON decode error: {e}", 'output': result.stdout}
        
        # output_lines = result.stdout.splitlines()
        # json_output = None
        # for line in output_lines:
        #     json_output = custom_json_serializer.deserialize(line)
        # if json_output is not None:
        #         logging.info(f"JSON output: {json_output}")
        #         return json_output        
