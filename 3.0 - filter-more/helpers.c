#include "helpers.h"

#include <math.h>
#include <stdio.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    if (height < 0)
    {
        return;
    }

    grayscale(height - 1, width, image);

    for (int j = 0; j < width; j++)
    {
        int bw = round(((float) image[height][j].rgbtRed + (float) image[height][j].rgbtGreen + (float) image[height][j].rgbtBlue) / 3);
        image[height][j].rgbtRed = bw;
        image[height][j].rgbtGreen = bw;
        image[height][j].rgbtBlue = bw;
    }
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    if (height < 0)
    {
        return;
    }

    reflect(height - 1, width, image);
    for (int j = 0; j < width / 2; j++)
    {
        RGBTRIPLE tmppx = image[height][j];
        image[height][j] = image[height][width - (j + 1)];
        image[height][width - (j + 1)] = tmppx;
    }
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            temp[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int avg_red = 0, avg_green = 0, avg_blue = 0;

            int corner_case[] = {i == 0 && j == 0, i == 0 && j == width - 1, i == height - 1 && j == 0, i == height - 1 && j == width - 1};
            int edge_case[] = {i == 0, j == 0, i == height - 1, j == width - 1};

            if (corner_case[0])
            {
                for (int row = 0; row <= 1; row++)
                {
                    for (int col = 0; col <= 1; col++)
                    {
                        avg_red = avg_red + temp[i + row][j + col].rgbtRed;
                        avg_green = avg_green + temp[i + row][j + col].rgbtGreen;
                        avg_blue = avg_blue + temp[i + row][j + col].rgbtBlue;
                    }
                }

                avg_red = round((float) avg_red / 4);
                avg_green = round((float) avg_green / 4);
                avg_blue = round((float) avg_blue / 4);
            }
            else if (corner_case[1])
            {
                for (int row = 0; row <= 1; row++)
                {
                    for (int col = -1; col <= 0; col++)
                    {
                        avg_red = avg_red + temp[i + row][j + col].rgbtRed;
                        avg_green = avg_green + temp[i + row][j + col].rgbtGreen;
                        avg_blue = avg_blue + temp[i + row][j + col].rgbtBlue;
                    }
                }

                avg_red = round((float) avg_red / 4);
                avg_green = round((float) avg_green / 4);
                avg_blue = round((float) avg_blue / 4);
            }
            else if (corner_case[2])
            {
                for (int row = -1; row <= 0; row++)
                {
                    for (int col = 0; col <= 1; col++)
                    {
                        avg_red = avg_red + temp[i + row][j + col].rgbtRed;
                        avg_green = avg_green + temp[i + row][j + col].rgbtGreen;
                        avg_blue = avg_blue + temp[i + row][j + col].rgbtBlue;
                    }
                }

                avg_red = round((float) avg_red / 4);
                avg_green = round((float) avg_green / 4);
                avg_blue = round((float) avg_blue / 4);
            }
            else if (corner_case[3])
            {
                for (int row = -1; row <= 0; row++)
                {
                    for (int col = -1; col <= 0; col++)
                    {
                        avg_red = avg_red + temp[i + row][j + col].rgbtRed;
                        avg_green = avg_green + temp[i + row][j + col].rgbtGreen;
                        avg_blue = avg_blue + temp[i + row][j + col].rgbtBlue;
                    }
                }

                avg_red = round((float) avg_red / 4);
                avg_green = round((float) avg_green / 4);
                avg_blue = round((float) avg_blue / 4);
            }
            else if (edge_case[0])
            {
                for (int row = 0; row <= 1; row++)
                {
                    for (int col = -1; col <= 1; col++)
                    {
                        avg_red = avg_red + temp[i + row][j + col].rgbtRed;
                        avg_green = avg_green + temp[i + row][j + col].rgbtGreen;
                        avg_blue = avg_blue + temp[i + row][j + col].rgbtBlue;
                    }
                }

                avg_red = round((float) avg_red / 6);
                avg_green = round((float) avg_green / 6);
                avg_blue = round((float) avg_blue / 6);
            }
            else if (edge_case[1])
            {
                for (int row = -1; row <= 1; row++)
                {
                    for (int col = 0; col <= 1; col++)
                    {
                        avg_red = avg_red + temp[i + row][j + col].rgbtRed;
                        avg_green = avg_green + temp[i + row][j + col].rgbtGreen;
                        avg_blue = avg_blue + temp[i + row][j + col].rgbtBlue;
                    }
                }

                avg_red = round((float) avg_red / 6);
                avg_green = round((float) avg_green / 6);
                avg_blue = round((float) avg_blue / 6);
            }
            else if (edge_case[2])
            {
                for (int row = -1; row <= 0; row++)
                {
                    for (int col = -1; col <= 1; col++)
                    {
                        avg_red = avg_red + temp[i + row][j + col].rgbtRed;
                        avg_green = avg_green + temp[i + row][j + col].rgbtGreen;
                        avg_blue = avg_blue + temp[i + row][j + col].rgbtBlue;
                    }
                }

                avg_red = round((float) avg_red / 6);
                avg_green = round((float) avg_green / 6);
                avg_blue = round((float) avg_blue / 6);
            }
            else if (edge_case[3])
            {
                for (int row = -1; row <= 1; row++)
                {
                    for (int col = -1; col <= 0; col++)
                    {
                        avg_red = avg_red + temp[i + row][j + col].rgbtRed;
                        avg_green = avg_green + temp[i + row][j + col].rgbtGreen;
                        avg_blue = avg_blue + temp[i + row][j + col].rgbtBlue;
                    }
                }

                avg_red = round((float) avg_red / 6);
                avg_green = round((float) avg_green / 6);
                avg_blue = round((float) avg_blue / 6);
            }
            else
            {
                for (int row = -1; row <= 1; row++)
                {
                    for (int col = -1; col <= 1; col++)
                    {
                        avg_red = avg_red + temp[i + row][j + col].rgbtRed;
                        avg_green = avg_green + temp[i + row][j + col].rgbtGreen;
                        avg_blue = avg_blue + temp[i + row][j + col].rgbtBlue;
                    }
                }

                avg_red = round((float) avg_red / 9);
                avg_green = round((float) avg_green / 9);
                avg_blue = round((float) avg_blue / 9);
            }
            image[i][j].rgbtRed = avg_red;
            image[i][j].rgbtGreen = avg_green;
            image[i][j].rgbtBlue = avg_blue;
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{

    RGBTRIPLE temp[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            temp[i][j] = image[i][j];
        }
    }

    int gy[] = {-1, -2, -1, 0, 0, 0, 1, 2, 1};
    int gx[] = {-1, 0, 1, -2, 0, 2, -1, 0, 1};

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float gx_red = 0, gx_green = 0, gx_blue = 0, gy_red = 0, gy_green = 0, gy_blue = 0;
            int avg_red = 0, avg_green = 0, avg_blue = 0, gv = 0;

            for (int row = -1; row <= 1; row++)
            {
                for (int col = -1; col <= 1; col++)
                {
                    if (i + row < 0 || i + row >= height)
                    {
                        gv++;
                        continue;
                    }

                    if (j + col < 0 || j + col >= width)
                    {
                        gv++;
                        continue;
                    }

                    gx_red = gx_red + (gx[gv] * temp[i + row][j + col].rgbtRed);
                    gx_green = gx_green + (gx[gv] * temp[i + row][j + col].rgbtGreen);
                    gx_blue = gx_blue + (gx[gv] * temp[i + row][j + col].rgbtBlue);

                    gy_red = gy_red + (gy[gv] * temp[i + row][j + col].rgbtRed);
                    gy_green = gy_green + (gy[gv] * temp[i + row][j + col].rgbtGreen);
                    gy_blue = gy_blue + (gy[gv] * temp[i + row][j + col].rgbtBlue);

                    gv++;
                }
            }

            avg_red = round(sqrt(pow(gx_red, 2) + pow(gy_red, 2)));
            avg_green = round(sqrt(pow(gx_green, 2) + pow(gy_green, 2)));
            avg_blue = round(sqrt(pow(gx_blue, 2) + pow(gy_blue, 2)));

            if (avg_red > 255)
            {
                avg_red = 255;
            }
            if (avg_green > 255)
            {
                avg_green = 255;
            }
            if (avg_blue > 255)
            {
                avg_blue = 255;
            }
            image[i][j].rgbtRed = avg_red;
            image[i][j].rgbtGreen = avg_green;
            image[i][j].rgbtBlue = avg_blue;
        }
    }
    return;
}
