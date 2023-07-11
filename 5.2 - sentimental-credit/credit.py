from cs50 import get_string


def main():
    number = get_string("Number: ").strip()
    length = len(number)
    if checksum(number) == 0 and (length == 13 or length == 15 or length == 16):
        if number[0] == "4":
            print("VISA")
        else:
            first_two = int(number[0:2])
            if first_two == 34 or first_two == 37:
                print("AMEX")
            elif first_two == 51 or first_two == 52 or first_two == 53 or first_two == 54 or first_two == 55:
                print("MASTERCARD")
            else:
                print("INVALID")
    else:
        print("INVALID")


def checksum(number):
    l = len(number)
    sum = 0

    for n, i in enumerate(reversed(range(l))):
        dig = int(number[n])
        if i % 2 == 1:
            dig *= 2
            while dig != 0:
                sum += dig % 10
                dig //= 10
        else:
            sum += dig

    return sum % 10


main()