import click
from .functions_tex import extract_tex_env


@click.command(
        help="Extracts tex environments from tex files"
        )
@click.option(
        '-i',
        '--inputfile',
        type=click.Path(),
        default="./main.tex",
        show_default=True,
        help="Input file path"
        )
@click.option(
        '-o',
        '--outputfile',
        type = click.Path(),
        default = "./tikz.tex",
        show_default=True,
        help = "Output file path"
        )
@click.option(
        '-e',
        '--environment',
        type=click.Choice(['tikzpicture', 'align*']),
        default="tikzpicture",
        show_default=True,
        help="Environment to be extracted"
        )
def main(inputfile, outputfile, environment):
    extract_tex_env(inputfile, outputfile, environment)












