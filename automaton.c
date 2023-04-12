#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

char* apply_rule(const char *str, const int n_columns, const int idx) {

    char *str1 = malloc((int)((ceil(log10(n_columns))+1)*sizeof(char)));
    sprintf(str1, "%d", n_columns);

    char *str2; 
    if (idx != 0) {
        str2 = malloc((int)((ceil(log10(idx))+1)*sizeof(char)));
    } else {
	str2 = malloc(2*sizeof(char));
    }
    sprintf(str2, "%d", idx);

    char *result = malloc(strlen(str) + strlen(str1) + strlen(str2) + 3);
    strcpy(result, str);
    strcat(result, " ");
    strcat(result, str1);
    strcat(result, " ");
    strcat(result, str2);
    return result;
}
