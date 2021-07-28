# 简介
提取 Excel 里的数据，导出为各种结构化的文本。除了提供命令行下的可执行脚本外也提供了
 Python API。


# 繁介
你总会需要一些由非技术人员提供的数据来充实你的程序内容，比如美术资源和各种数值。美术资源好说，
规范好目录和文件名就万事大吉了，但数值咋放呢？必须得有一个他懂、你懂、程序也懂的数值载体，
除了 Excel 估计你也没得选了，总不能指望人家跑来编辑什么 json、xml 之类的结构化文本吧？何况
 Excel 本身就是个强大的数据处理工具，拿它来做数值易如反掌。于是本项目应运而生，专门用于提取
 Excel 里的数据。

# 特性
 - 尽量约定而非配置，只需标出列名就能满足基本要求，高级玩法也只需要一点点小配置而已。 :stuck_out_tongue_winking_eye:
 - 支持多种数据结构 e.g. list,dict, （tree还有待实现）。
 - 支持导出为 json 格式
 - 支持使用 mako 生成代码


# 运行依赖

  * Python3

# 安装
```
$ python setup install
```

# 使用

## Python API示例
```python
from excel2xx import Excel

fpath = "abc.xls"
excel = Excel(fpath)

# 获取第一个 sheet 的内容
sheet = excel[0]
for row in sheet:
    print(row)
    
# 根据 sheet 名获取
sheet = excel["你好啊"]
for row in sheet:
    print(row)
```

## CLI 示例
```
$ excel2xx json example/test.xls  -o example/test.json
$ excel2xx msgpack example/test.xls --output example/test.msgpack
$ excel2xx mako example/test.xls  -o example/test.lua --template example/test.mako
```

# TODO

 - [X] Simple DSL (just coding with python :stuck_out_tongue_winking_eye:)
 - [ ] Export to Lua code
 - [ ] Export to SQL code


# LICENSE
<a href="https://www.wtfpl.net/">
    <img src="http://www.wtfpl.net/wp-content/uploads/2012/12/wtfpl-badge-1.png"
         width="88"
         height="31"
         alt="WTFPL" />
</a>

```text
            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                    Version 2, December 2004

 Copyright (C) 2014-2021 cupen<xcupen@gmail.com>

 Everyone is permitted to copy and distribute verbatim or modified
 copies of this license document, and changing it is allowed as long
 as the name is changed.

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

  0. You just DO WHAT THE FUCK YOU WANT TO.
```
