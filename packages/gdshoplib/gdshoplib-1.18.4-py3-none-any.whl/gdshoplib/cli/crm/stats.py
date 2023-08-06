import typer

from gdshoplib.apps.crm.stats import Statistic

app = typer.Typer()


@app.command()
def price(price_type="average"):
    if price_type == "average":
        print(Statistic().avg_price())
