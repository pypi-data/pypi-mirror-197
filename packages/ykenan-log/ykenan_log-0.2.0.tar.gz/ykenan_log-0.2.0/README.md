# ykenan_log

> **`Print and save a simple log to a file`**

This is a simple log package. You can see
[Github-ykenan_log](https://github.com/YuZhengM/ykenan_log)

> upload

```shell
py -m build
twine check dist/*
twine upload dist/*
```

## Use

> install

```shell
pip install ykenan_log
```

> use

```python
# -*- coding: utf-8 -*-

import ykenan_log

logger = ykenan_log.Logger("name", "log")

if __name__ == '__main__':
    print("run...")
    logger.debug("info......")
    logger.info("info......")
    logger.warn("info......")
    logger.error("info......")
```

> output

```shell
run...
2023-03-17 09:21:36 root name[34768] DEBUG info......
2023-03-17 09:21:36 root name[34768] INFO info......
2023-03-17 09:21:36 root name[34768] WARNING info......
2023-03-17 09:21:36 root name[34768] ERROR info......

```

## Introduction

> **main function**

> ykenan_log.Logger(
>> name: str = None,
> 
>> log_path: str = None,
> 
>> level: str = "DEBUG",
> 
>> is_solitary: bool = True,
> 
>> is_form_file: bool = True,
> 
>> size: int = 104857600,
> 
>> backup_count: int = 10,
> 
>> encoding: str = "UTF-8"
> 
> ) 

```
:param name: Project Name
:param log_path: Log file output path. Default is log_%Y%m%d.log.
:param level: Log printing level. Default is DEBUG.
:param is_solitary: When the file path is consistent (here, the log_path parameter is not a specific file name, but a file path), whether the file is formed independently according to the name parameter. Default is True.
:param is_form_file: Whether to form a log file. Default is True.
:param size: Setting the file size if a file is formed. Default is 104857600. (100MB)
:param backup_count: Setting the number of rotating files if a file is formed. Default is 10.
:param encoding: Setting of file encoding if a file is formed. Default is UTF-8.
```
