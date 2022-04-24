#ifndef __01_H__
#define __01_H__

#include <unistd.h>
#include <sys/stat.h>

typedef char * t_string;
//@func
/*
** < 01.c > */

int			lib_write(int fd, const t_string str);
int			lib_writes(int fd, t_string arr[]);
t_string	str_new(const t_string src);
struct stat	*lib_stat(const t_string path);
#endif // __01_H__