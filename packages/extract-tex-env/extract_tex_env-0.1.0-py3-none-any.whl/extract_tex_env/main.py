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
        help="Input file path"
        )
@click.option(
        '-o',
        '--outputfile',
        type = click.Path(),
        default = "./tikz.tex",
        help = "Output file path"
        )
@click.option(
        '-e',
        '--environment',
        type=click.Choice(['tikzpicture', 'align*']),
        default="tikzpicture",
        help="Environment to be extracted"
        )
def main(inputfile, outputfile, environment):
    extract_tex_env(inputfile, outputfile, environment)












