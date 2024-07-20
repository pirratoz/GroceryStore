def main(n: int) -> None:
    string, length = "", 0
    for i in range(1, n + 1):
        if n < length + i:
            string += str(i) * (n - length)
            break
        string += str(i) * i
        length += i
    print(string)


if __name__ == "__main__":
    main(n=0)
