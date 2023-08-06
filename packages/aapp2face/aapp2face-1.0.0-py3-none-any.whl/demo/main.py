import typer
from rich import print
from zeep import Client

app = typer.Typer()


def find_country(lista_paises, codigo_iso):
    for elemento in lista_paises:
        if elemento["sISOCode"] == codigo_iso:
            return elemento["sName"]
    return None


@app.command()
def main(
    country_iso_code: str = typer.Argument(..., help="ISO code for country to find")
):
    """Find the capital of a country"""

    client = Client(
        "http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso?WSDL"
    )
    capital = client.service.CapitalCity(country_iso_code)
    if capital == "Country not found in the database":
        print(
            f"[bold yellow]Sorry!![/bold yellow] I can't find {country_iso_code} in my countries database"
        )
        exit(1)
    country_list = client.service.ListOfCountryNamesByName()
    country = find_country(country_list, country_iso_code)
    print(f"The capital of [green]{country} is {capital}[/green]")
    print("Demo with love :purple_heart:")


if __name__ == "__main__":
    app()
