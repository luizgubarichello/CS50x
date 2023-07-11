#include <cs50.h>
#include <stdio.h>

int checksum(long number);
int card_length(long number);
int dig1(long number);
int dig2(long number);

int main(void)
{
    long number = get_long("Number: ");
    int length = card_length(number);
    if (checksum(number) == 0 && (length == 13 || length == 15 || length == 16))
    {
        if (dig1(number) == 4)
        {
            printf("VISA\n");
        }
        else
        {
            int first_two = dig1(number) * 10 + dig2(number);
            if (first_two == 34 || first_two == 37)
            {
                printf("AMEX\n");
            }
            else if (first_two == 51 || first_two == 52 || first_two == 53 || first_two == 54 || first_two == 55)
            {
                printf("MASTERCARD\n");
            }
            else
            {
                printf("INVALID\n");
            }
        }
    }
    else
    {
        printf("INVALID\n");
    }
}

int dig1(long number)
{
    long card_number = number;
    int length = card_length(number);
    int i = 0;
    int digit;
    while (card_number != 0)
    {
        digit = card_number % 10;
        card_number = card_number / 10;
        i++;
        if (i == length)
        {
            break;
        }
    }
    return digit;
}

int dig2(long number)
{
    long card_number = number;
    int length = card_length(number);
    int i = 0;
    int digit;
    while (card_number != 0)
    {
        digit = card_number % 10;
        card_number = card_number / 10;
        i++;
        if (i == length - 1)
        {
            break;
        }
    }
    return digit;
}

int card_length(long number)
{
    long card_number = number;
    int i = 0;
    while (card_number != 0)
    {
        card_number = card_number / 10;
        i++;
    }
    return i;
}

int checksum(long number)
{
    long card_number = number;
    int i = 0;
    int sum_digit = 0;

    while (card_number != 0)
    {
        int digit = card_number % 10;
        if (i % 2 == 0)
        {
            sum_digit = sum_digit + digit;
        }
        else
        {
            digit = digit * 2;
            while (digit != 0)
            {
                sum_digit = sum_digit + digit % 10;
                digit = digit / 10;
            }
        }
        card_number = card_number / 10;
        i++;
    }

    return sum_digit % 10;
}