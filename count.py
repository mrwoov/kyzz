import csv

f = open('data/answer_cut_list.txt', 'r', encoding='utf-8')
answer_list = f.read().split('\n')
f.close()
f = open('data/option_cut_list.txt', 'r', encoding='utf-8')
option_list = f.read().split('\n')
f.close()
f = open('data/wrong_cut_list.txt', 'r', encoding='utf-8')
wrong_list = f.read().split('\n')
f.close()
# 读原文
f = open('data/option_text.txt', 'r', encoding='utf-8')
option_text = f.read()
f.close()
f = open('data/answer_text.txt', 'r', encoding='utf-8')
answer_text = f.read()
f.close()
f = open('data/wrong_text.txt', 'r', encoding='utf-8')
wrong_text = f.read()
f.close()
# 统计词频在原文中的出现次数
option_word_count = {}
answer_word_count = {}
wrong_word_count = {}
for word in option_list:
    option_word_count[word] = option_text.count(word)
for word in answer_list:
    answer_word_count[word] = answer_text.count(word)
for word in wrong_list:
    wrong_word_count[word] = wrong_text.count(word)
# 词频排序
option_word_count = sorted(option_word_count.items(), key=lambda x: x[1], reverse=True)
answer_word_count = sorted(answer_word_count.items(), key=lambda x: x[1], reverse=True)
wrong_word_count = sorted(wrong_word_count.items(), key=lambda x: x[1], reverse=True)
# 保存词频排序结果为csv
f = open('data/option_word_count.csv', 'w', encoding='utf-8')
writer = csv.writer(f)
writer.writerows(option_word_count)
f.close()
f = open('data/answer_word_count.csv', 'w', encoding='utf-8')
writer = csv.writer(f)
writer.writerows(answer_word_count)
f.close()
f = open('data/wrong_word_count.csv', 'w', encoding='utf-8')
writer = csv.writer(f)
writer.writerows(wrong_word_count)
f.close()

#将分词结果转为字典
output = []
option_word_count = dict(option_word_count)
answer_word_count = dict(answer_word_count)
wrong_word_count = dict(wrong_word_count)
for word in option_word_count:
    count = option_word_count[word]
    if word in answer_word_count:
        answer_count =  answer_word_count[word]
    else:
        answer_count = 0
    if word in wrong_word_count:
        wrong_count =  wrong_word_count[word]
    else:
        wrong_count = 0
    temp = [word, count, answer_count,answer_count/count, wrong_count, wrong_count/count]
    output.append(temp)
# 保存结果为csv
f = open('data/count.csv', 'w', encoding='utf-8', newline='')
writer = csv.writer(f)
writer.writerows(output)
f.close()