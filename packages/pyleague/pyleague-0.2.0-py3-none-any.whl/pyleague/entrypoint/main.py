import typer

from pyleague.use_cases.init import init_
from pyleague.use_cases.next import next_
from pyleague.use_cases.participants import participants_
from pyleague.use_cases.previous import previous_
from pyleague.use_cases.today import today_

app = typer.Typer()


@app.command()
def init():
    init_()


@app.command()
def previous():
    previous_()


@app.command()
def today():
    today_()


@app.command()
def next():
    next_()


@app.command()
def participants():
    participants_()


if __name__ == "__main__":
    app()
