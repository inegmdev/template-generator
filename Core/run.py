import subprocess
import json
import click
import os

def run_template_generation(template_path, data_path, output_path):
    """
    Run the render_template.py script with the specified parameters.
    """
    command = [
        'python3', 'generate.py',  # The script to run
        template_path,                   # The template file path
        data_path,                       # The JSON data file path
        output_path                      # The output file path
    ]

    # Run the command
    result = subprocess.run(command, capture_output=True, text=True)

    # Check if the command was successful
    if result.returncode == 0:
        print(f"Command executed successfully:\n{result.stdout}")
    else:
        print(f"Command failed with error:\n{result.stderr}")

def load_data_from_json(json_file_path, key):
    """
    Load commands from a JSON file.
    """
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    return data.get(key, [])

def load_commands_from_json(json_file_path):
    return load_data_from_json(json_file_path, 'commands')

def load_main_dev_path_from_json(json_file_path):
    return load_data_from_json(json_file_path, 'main_dev_path')

def load_template_generation_script_from_json(json_file_path):
    return load_data_from_json(json_file_path, 'script')

@click.command()
@click.option('--config', required=True, help='Path to the JSON configuration file.')
def run(config):
    """
    Run template generation commands based on a configuration file.
    """
    # Load commands from the JSON file specified by --config
    main_dev_rel_path = load_main_dev_path_from_json(config)
    main_dev_path = os.path.abspath(os.path.join(config, main_dev_rel_path))
    script_path = load_template_generation_script_from_json(config)
    commands = load_commands_from_json(config)

    # Execute each command in the JSON file
    for command in commands:
        template_path = command.get('template')
        data_path = command.get('data')
        output_path = command.get('output')

        print(f"Running command with template: {template_path}, data: {data_path}, output: {output_path}")
        run_template_generation(template_path, data_path, output_path)

if __name__ == "__main__":
    run()
