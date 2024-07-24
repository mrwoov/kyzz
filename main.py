import json
import pymysql
import csv
import jieba

class transform:
    def __init__(self):
        self.year = None

    def read(self):
        data = ''
        f = open(f'data/{self.year}.json', 'r', encoding='utf-8')
        data = f.read().replace('ä½', '')
        f.close()
        data = json.loads(data)
        data = data['detail']['timu']
        return data

    def process(self, data):
        conn = pymysql.connect(host='localhost', port=3306, user='root', password='5123580rt')
        cursor = conn.cursor()
        conn.select_db('kyzz')
        out_data = []
        for i in data:
            title = i['title']
            type = i['type']
            option_text = i['xuan_text']
            option_text_backup = option_text
            option_text = option_text.replace('A.', '').replace('B.', '').replace('C.', '').replace('D.', '').replace(
                '|', '')
            option_list = option_text_backup.split('|')
            option_a = option_list[0].replace('A.', '').replace('B.', '').replace('C.', '').replace('D.', '')
            option_b = option_list[1].replace('A.', '').replace('B.', '').replace('C.', '').replace('D.', '')
            option_c = option_list[2].replace('A.', '').replace('B.', '').replace('C.', '').replace('D.', '')
            option_d = option_list[3].replace('A.', '').replace('B.', '').replace('C.', '').replace('D.', '')
            answer = i['right_text']
            answer_text = ''
            wrong_text = ''
            flag_a = False
            flag_b = False
            flag_c = False
            flag_d = False
            for char in answer:
                if char == 'A':
                    answer_text += option_a
                    flag_a = True
                elif char == 'B':
                    answer_text += option_b
                    flag_b = True
                elif char == 'C':
                    answer_text += option_c
                    flag_c = True
                elif char == 'D':
                    answer_text += option_d
                    flag_d = True
            if not flag_a:
                wrong_text += option_a
            if not flag_b:
                wrong_text += option_b
            if not flag_c:
                wrong_text += option_c
            if not flag_d:
                wrong_text += option_d
            year = '20' + self.year
            top_from = i['top_kaodian_text']
            temp = [title, type, option_text, option_a, option_b, option_c, option_d, answer, answer_text, wrong_text,year,
                    top_from]
            out_data.append(temp)
        # # 导出csv
        # f = open('data/out.csv', 'w', encoding='utf-8')
        # writer = csv.writer(f)
        # writer.writerows(out_data)
        return out_data

    def fenxi(self,data):
        option_text = ''
        answer_text = ''
        wrong_text = ''
        for i in data:
            option_text += i[2]
            answer_text += i[8]
            wrong_text += i[9]
        f = open('data/option_text.txt', 'w', encoding='utf-8')
        f.write(option_text)
        f.close()
        f = open('data/answer_text.txt', 'w', encoding='utf-8')
        f.write(answer_text)
        f.close()
        f = open('data/wrong_text.txt', 'w', encoding='utf-8')
        f.write(wrong_text)
        f.close()

        option_list = jieba.lcut(option_text)
        answer_list = jieba.lcut(answer_text)
        wrong_list = jieba.lcut(wrong_text)
        # 去除长度小于2的词
        option_list = [word for word in option_list if len(word) > 1]
        answer_list = [word for word in answer_list if len(word) > 1]
        wrong_list = [word for word in wrong_list if len(word) > 1]
        # 去除重复的词
        option_list = list(set(option_list))
        answer_list = list(set(answer_list))
        wrong_list = list(set(wrong_list))
        # 保存分词结果
        f = open('data/option_cut_list.txt', 'w', encoding='utf-8')
        f.write("\n".join(option_list))
        f.close()
        f = open('data/answer_cut_list.txt', 'w', encoding='utf-8')
        f.write("\n".join(answer_list))
        f.close()
        f = open('data/wrong_cut_list.txt', 'w', encoding='utf-8')
        f.write("\n".join(wrong_list))

    def transform(self):
        data = []
        for i in range(17, 25):
            self.year = str(i)
            # 合并数据
            data += self.read()
        out_data = self.process(data)
        self.fenxi(out_data)

a = transform()
a.transform()

