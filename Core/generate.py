import json
from jinja2 import Environment, FileSystemLoader
import click

@click.command()
@click.option('--template', required=True, help='Path to the Jinja2 template file.')
@click.option('--data', required=True, help='Path to the JSON data file.')
@click.option('--output', required=True, help='Path where the rendered output will be saved.')
def render_template(template, data, output):
    """
    Render a Jinja2 template using data from a JSON file and output the result to a specified file.
    """

    # Load the template file
    template_dir = template.rsplit('/', 1)[0]  # Extract directory path
    template_name = template.rsplit('/', 1)[-1]  # Extract template file name
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(template_name)

    # Load the data from JSON file
    with open(data, 'r') as data_file:
        data = json.load(data_file)

    # Render the template with the data
    rendered_content = template.render(data)

    # Write the rendered content to the output file
    with open(output, 'w') as output_file:
        output_file.write(rendered_content)

    click.echo(f"Rendered content written to {output}")

if __name__ == "__main__":
    render_template()
