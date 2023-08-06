#include <stdio.h>
#include "log.h"

static void _open(log_t *lg) {
    lg->fp = fopen("daemonizer_error.log", "w");
    lg->is_open = true;
}

void info(log_t *lg, char const *arg_str) {
    if (!lg->is_open) {
        _open(lg);
    }
    fprintf(lg->fp, "%s\n", arg_str); // pulls from errno
    fflush(lg->fp); // to force write to disk
}

void error(log_t *lg, char const *arg_str) {
    if (!lg->is_open) {
        _open(lg);
    }
    fprintf(lg->fp, "%s\n", arg_str); 
    fflush(lg->fp);
    end(lg);
}

void end(log_t *lg) {
    fclose(lg->fp);
}