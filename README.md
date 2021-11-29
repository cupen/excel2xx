# 简介
导出 Excel 到各种结构化数据或代码。除命令行接口外也提供了
 Python API 便于做二次加工。


# 繁介
你总会需要一些由非技术人员提供的数据来充实你的产品内容，比如美术资源和游戏数值。美术资源好说，
规范好目录和文件名就万事大吉了，但数值咋放呢？必须要有一个他懂、你懂、程序也懂的数值载体。
Excel 作为一款数据处理工具，做游戏数值简直易如反掌。于是本项目应运而生，用来搬运 Excel 数据。

 p.s: 别让策划编辑 json, xml, 数据库之类的，那样太低效，很没人情味。


# 特性
 - 支持数据类型约束
    - 基本类型: string, int, float, bool
    - 数组类型: array\<string\>, array\<int\>, array\<float\>, array\<bool\>
    - Map 类型: map\<string, string\>, map\<string, int\> 等等
    - ItemExpr (物品表达式), 一种易于编辑的 DSL, 用于描述游戏中的物品/数值。  
      文法: 类型-ID-数量, 比如 coin-100 表示 100 金币, weapon-1001-4 表示 4件ID为1001的武器。
 - 支持多种数据结构 e.g. list,dict, （tree 还有待探索）。
 - 支持导出到 json, msgpack.
 - 支持使用 mako 模板引擎生成到任意编程语言代码(比如枚举值声明)。


# 运行依赖

  * Python3.6+

# 安装
```
$ pip install excel2xx
```

# 使用

## Python API示例
```python
from excel2xx import Excel

excel = Excel("abc.xlsx")

# 获取第一个 sheet
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
$ excel2xx json example/test.xls    -o example/test.json
$ excel2xx msgpack example/test.xls -o example/test.msgpack
$ excel2xx mako example/test.xls    -o example/test.lua  --template example/test.lua.mako
```


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
