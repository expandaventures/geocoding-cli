import sys
import click
from geocli_driver import process_file, get_location_by_address


@click.group()
@click.version_option("1.0.0")
def main():
    """A Geocoding CLI"""
    pass


@main.command()
@click.argument('input_file', required=True, type=click.Path(exists=True))
@click.argument('output_path', required=True)
@click.option('--dry_run', is_flag=True)
def batch(**kwargs):
    """Process a file and output the results to a file"""
    results = process_file(kwargs.get("input_file"),
                           kwargs.get("output_path"),
                           kwargs.get("dry_run", False),
                           )
    click.echo(f'Processed {results} results')


@main.command()
@click.argument('address', required=True)
@click.argument('state', required=False, default='')
@click.argument('city', required=False, default='')
@click.option('--dry_run', is_flag=True)
def geocode(**kwargs):
    """process a single address"""
    lat, lon = get_location_by_address(kwargs.get("state", ""),
                                       kwargs.get("city", ""),
                                       address_string=kwargs.get("address"),
                                       dry_run=kwargs.get("dry_run", False),
                                       )
    click.echo(f'Lat, Lon: {lat}, {lon}')


if __name__ == '__main__':
    args = sys.argv
    if "--help" in args or len(args) == 1:
        print("GEOCLI")
    main()
