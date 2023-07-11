#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;

    do
    {
        height = get_int("height: ");
    }
    while (height < 1 || height > 8);

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < (2 * height + 2); j++)
        {
            if (j < height - 1 - i)
            {
                printf(" ");
            }
            else if (j >= height - 1 - i && j < height)
            {
                printf("#");
            }
            else if (j >= height && j < height + 2)
            {
                printf(" ");
            }
            else if (j >= height + 2 && j <= height + 2 + i)
            {
                printf("#");
            }
        }
        printf("\n");
    }

}