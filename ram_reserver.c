#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main()
{
    // Define the size to be allocated: 1GB
    size_t size = 1024 * 1024 * 1024; // 1GB in bytes

    // Allocate the memory
    char *buffer = (char *)malloc(size);
    if (buffer == NULL)
    {
        fprintf(stderr, "Memory allocation failed\n");
        return 1;
    }

    // Touch each byte to ensure the memory is committed
    memset(buffer, 0, size);

    // Do something with the memory
    printf("1GB of memory has been successfully allocated and initialized.\n");

    // Free the memory
    free(buffer);

    return 0;
}