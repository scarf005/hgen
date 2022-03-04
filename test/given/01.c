#include "01.h"

int	lib_write(int fd, const t_string str)
{
	return (write(fd, str, str_len(str)));
}

//	write multiple strings
int	lib_writes(
	int fd, t_string arr[])
{
	int	i;
	int	res;

	i = -1;
	res = 0;
	while (arr[++i])
		res += lib_write(fd, arr[i]);
	return (res);
}

t_string	str_new(
	const t_string src){
	int			i;
	t_string	new;

	i = str_len(src);
	new = lib_calloc(sizeof(char), i);
	while (--i >= 0)
		new[i] = src[i];
	return (new);
}

struct stat	*lib_stat(
	const t_string path)
{
	struct stat	*res;

	res = lib_calloc(sizeof(struct stat), 1);
	if (stat(path, res) == -1)
		return (NULL);
	return (res);
}
