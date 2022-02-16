# hgen

## Introduction

![showcase](https://user-images.githubusercontent.com/83401142/144825570-210f51ed-ddfc-4a14-b84a-10db1aac8563.gif)

Injects c function prototypes(BSD-style) into header.

limitations
- cannot capture multi-line function prototypes
- cannot capture K&R style definitions
- breaks when function does not work with norminette
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
