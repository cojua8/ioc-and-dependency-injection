from example.readjuster import Readjuster


if __name__ == "__main__":
    from example.container import Container

    container = Container()

    total_amount = 1000
    months = 3

    readjuster = Readjuster(total_amount, months)

    readjusted_amount = readjuster.calculate()

    print(f"El monto inicial es: {total_amount}")
    print(f"El monto reajustado es: {readjusted_amount}")
