---
title: Regular Expressions
tags:
categories:
top:
---
几年之前我就开始使用正则表达式与Python结合来处理字符串，功能确实十分强大与方便，正则表达式虽然简洁但阅读不是那么方便，理解它还是存在一定的门槛的，我之前使用到正则表达式时都是在搜索引擎上去查找，现在我决定理解它以便未来快速构造我自己的复杂正则表达式。

正则表达式是用于处理字符串的强大工具，拥有自己独特的语法以及一个独立的处理引擎，效率上可能不如str自带的方法，但功能十分强大。得益于这一点，在提供了正则表达式的语言里，正则表达式的语法都是一样的，区别只在于不同的编程语言实现支持的语法数量不同；但不用担心，不被支持的语法通常是不常用的部分。如果已经在其他语言里使用过正则表达式，只需要简单看一看就可以上手了。

<!-- more -->

**字符**

| 语法     	| 说明                                                                                              	| 表达式实例 	| 完整匹配的字符串 	|
|----------	|---------------------------------------------------------------------------------------------------	|------------	|------------------	|
| 一般字符 	| 匹配自身                                                                                          	| abc        	| abc              	|
| .        	| 匹配任意除换行符“\n”外的字符。 在DOTALL模式中也能匹配换行符。                                     	| a.c        	| abc              	|
| \        	| 转义字符，使后一个字符改变原来的意思。 如果字符串中有字符`*`需要匹配，可以使用`\*`或者字符集`[*]` 	| a\.c       	| a.c              	|
| [...]    	|                                                                                                   	| a[bcd]e    	| abe ace ade      	|
|          	|                                                                                                   	|            	|                  	|
|          	|                                                                                                   	|            	|                  	|


https://www.cnblogs.com/huxi/archive/2010/07/04/1771073.html