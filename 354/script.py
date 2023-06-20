import typer


def sum_numbers(a: int, b: int):
    return a + b


def main(
    a: int = typer.Argument(..., help="The value of the first summand"),
    b: int = typer.Argument(..., help="The value of the second summand"),
    c: int = typer.Option(None, help="The value to compare against"),
):
    """CLI that allows you to add two numbers"""

    value = sum_numbers(a, b)
    message = f"The sum is {value}"
    if c is None:
        message += " and c is None"
    elif c < value: 
        message += " and c is smaller"
    else:
        message += " and c is not smaller"

    print(message)


if __name__ == "__main__":
    typer.run(main)