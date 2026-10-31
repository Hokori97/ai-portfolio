# W3 生词表 CSV -> 自动生成练习题
# 运行：python vocab_tool.py
import os
import csv
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import weekpath  # noqa: E402  统一解析 data/ 路径，换目录也不会找不到文件

DATA = weekpath.data_path("生词表.csv")


def load_words(path=DATA):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def filter_by_level(words, level="4"):
    return [w for w in words if str(w["HSK等级"]) == str(level)]


def count_by_pos(words):
    d = {}
    for w in words:
        d[w["词性"]] = d.get(w["词性"], 0) + 1
    return d


def gen_exercises(words, out=None):  # ④ 写
    out = out or weekpath.root_path("练习.txt")
    with open(out, "w", encoding="utf-8") as f:
        for w in words:
            # 原来完整题目
            f.write("用“%s”造一个句子。（%s）\n" % (w["词汇"], w["词性"]))
            # 新增：挖空填空题
            f.write("用____造一个句子。（%s：%s）\n\n" % (w["词性"], w["词汇"]))


# 作业2新增：生成填空题，把目标词替换成____
def make_fill_blank(sentence, target_word):
    blank_sentence = sentence.replace(target_word, "____")
    return blank_sentence

if __name__ == "__main__":
    words = load_words()
    lv4 = filter_by_level(words, "4")
    print("总词汇 %d 个，其中 HSK4 词汇 %d 个，词性分布：%s"
          % (len(words), len(lv4), count_by_pos(lv4)))
    out = weekpath.root_path("练习.txt")
    gen_exercises(lv4, out)
    print("已生成：%s" % out)
# 作业1新增：字典统计词性分布
    pos_count = {}
    for w in words:
        pos = w["词性"]
        if pos in pos_count:
            pos_count[pos] += 1
        else:
            pos_count[pos] = 1
    print("词性统计结果：", pos_count)

    # 作业2：测试填空功能
test_sentence = "我吃饭。"
blank_result = make_fill_blank(test_sentence, "吃")
print("填空练习题：", blank_result)
