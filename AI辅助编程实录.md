# AI辅助编程实录

## 1. 任务与提示词
要做什么：读取生词表CSV文件，筛选HSK4等级词汇，统计词性分布，自动生成造句练习题输出到练习.txt，只用Python标准库。

我写的提示词：
>角色：Python教学助手
>任务：写脚本读生词表CSV并生成练习题
>要求：按HSK等级筛选、统计词性分布、输出txt，仅用标准库，每行加注释
>示例：期望输出 用“坚持”造一个句子。（动词）

## 2. AI 初版代码
```python
# AI给我的初稿
import csv

def load_words():
    f = open("生词表.csv")
    reader = csv.DictReader(f)
    return list(reader)

def filter_by_level(words):
    res = []
    for w in words:
        if w["HSK等级"] ==4:
            res.append(w)
    return res

def gen_exercise(words):
    f2 = open("练习.txt","w")
    for item in words:
        f2.write(f"用“{item['词汇']}”造一个句子。（{item['词性']}）")
    f2.close()

ws = load_words()
hsk4 = filter_by_level(ws)
gen_exercise(hsk4)
```
## 3. 我的修改点（≥3条）
① 增加weekpath路径工具，统一管理csv和输出txt路径；
原因：防止不同运行目录出现找不到文件FileNotFoundError，保证脚本在哪运行都能找到data下面的csv。

② 所有文件open()加上`encoding="utf-8"`；
原因：Windows系统默认GBK编码，不加会出现中文乱码报错UnicodeDecodeError。

③ 等级对比处包上str()，`str(w["HSK等级"]) == str(level)`；
原因：csv读取出来有可能是数字或字符串，统一转字符串避免类型不一样筛选不到词汇。
## 4. 最终版 vs 初版差异说明
1. AI初稿打开文件没有用`with open()`，不会自动关闭文件；我改用with上下文管理器，自动管理文件关闭，更安全。
2. AI初稿缺少词性统计count_by_pos函数，控制台看不到统计信息，我新增这个函数实现词性计数输出。
3. AI初稿没有`if __name__ == "__main__"`入口，代码直接全局执行，不方便后续函数被复用调用。

## 课后修改
④ 参考Python官方教程，引入`collections.defaultdict`改写词性统计函数，简化计数逻辑，替代原来的dict.get()写法。
⑤ 扩展脚本功能，新增挖空填空题输出，保留原本的造句题目，增加换行优化练习.txt的排版。