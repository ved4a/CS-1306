#include <stdio.h>
#include <string.h>

#define MAX 100

void map_message_to_key(char *key, char *message);
void swap(char *a, char *b);
void sort_string(char str[]);
void print_sorted_key_arrays(char *key, char key_arrays[][MAX], int *array_sizes, int key_len);

int main(void){
     char key[MAX], message[MAX];

     // Input the key and message
    printf("Enter the key (e.g., HACK): ");
    scanf("%s", key);

    printf("Enter the message (e.g., HELLOWORLD): ");
    scanf("%s", message);

    // Map the message to the key arrays
    map_message_to_key(key, message);

    return 0;
}

void map_message_to_key(char *key, char *message)
{
    int key_len = strlen(key);
    int msg_len = strlen(message);

    // Create an array of arrays
    // One array for each letter in the key
    char key_arrays[key_len][MAX];
    int array_sizes[key_len];

    // Initialize arrays + size of arrays
    for (int i = 0; i < key_len; i++)
    {
        array_sizes[i] = 0;
    }

    // Map message letters into key arrays
    for (int i = 0; i < msg_len; i++)
    {
        int array_index = i % key_len;
        key_arrays[array_index][array_sizes[array_index]] = message[i];
        array_sizes[array_index]++;
    }

    // Print
    for (int i = 0; i < key_len; i++)
    {
        printf("%c : ", key[i]);
        for (int j = 0; j < array_sizes[i]; j++)
        {
            printf("%c", key_arrays[i][j]);
            if (j < array_sizes[i] - 1)
            {
                printf("");
            }
        }
        printf("\n");
    }
}

void swap(char *a, char *b)
{
    char temp = *a;
    *a = *b;
    *b = temp;
}

void sort_string(char str[])
{
    int n = strlen(str);

    // Implementing bubble sort
    for (int i = 0; i < n -1; i++)
    {
        for (int j = 0; j < n - i - 1; j++)
        {
            if (str[j] > str[j + 1])
            {
                swap(&str[j], &str[j + 1]);
            }
        }
    }
}

void print_sorted_key_arrays(char *key, char key_arrays[][MAX], int *array_sizes, int key_len)
{
    // Create an array to store the original indices of the key
    int original_indices[key_len];
    for (int i = 0; i < key_len; i++)
    {
        original_indices[i] = i;
    }

    // Key copy
    char sorted_key[MAX];
    strcpy(sorted_key, key);

    // Sort the copied key
    sort_string(sorted_key);

    // Sort original indices based on the sorted key
    for (int i = 0; i < key_len; i++)
    {
        for (int j = 0; j < key_len; j++)
        {
            if (sorted_key[i] == key[j])
            {
                original_indices[i] = j;
                break;
            }
        }
    }

    // Print the arrays according to the sorted key and original indices
    for (int i = 0; i < key_len; i++)
    {
        int original_index = original_indices[i];
        printf("%c : ", sorted_key[i]);
        for (int j = 0; j < array_sizes[original_index]; j++)
        {
            printf("%c", key_arrays[original_index][j]);
        }
        printf("\n");
    }
}