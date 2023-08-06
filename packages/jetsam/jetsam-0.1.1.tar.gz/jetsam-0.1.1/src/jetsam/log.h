#include <stdarg.h>
#include <stdbool.h>

typedef struct log_t {
    bool is_open;
    FILE *fp;
} log_t;

void info(log_t *, char const *);
void error(log_t *, char const *);
void end(log_t *);