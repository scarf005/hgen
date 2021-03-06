# hgen

## Introduction

![showcase](https://user-images.githubusercontent.com/83401142/144825570-210f51ed-ddfc-4a14-b84a-10db1aac8563.gif)

Injects c function prototypes(BSD-style) into header.

limitations
- breaks when function does not work with norminette
- that means a function must not have any whitespace before its return type
- and exactly one tab must seperate its return type and name

## Usage

`hgen [-h] -I header.h src.c [src/ ...] [-c path]`

your header should have flags that

- begins with: `@func` or `@function(s)` at your comment
- ends with: `#endif` or `@end` or multiple `=` (ex:`== some identifier ==`)

### examples

```c
//	@func
//	@end
```

```c
#ifndef HEAD_H
# define HEAD_H

//	===== @functions =====
#endif
```

## Plans

- refactors
- json based configuration
- support K&R style function definitions
- support multiline function definitions
