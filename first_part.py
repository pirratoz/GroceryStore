def main(n: int) -> None:
    string = ""
    for i in range(1, n + 1):
        string += str(i) * i
    print(string)


if __name__ == "__main__":
    main(n=5)
