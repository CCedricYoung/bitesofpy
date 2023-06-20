import time

import typer
from rich.progress import track


app = typer.Typer()


@app.command()
def progress():
    results = 0
    for _ in track(range(10), "Processing..."):
        time.sleep(0.15)
        results += 1

    print(f"Processed {results} things.")


if __name__ == "__main__":
    app()