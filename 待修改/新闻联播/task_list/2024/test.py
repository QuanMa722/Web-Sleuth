

file_path = '../2020/202001.txt'
with open(file_path, mode='r', encoding='utf-8') as f:

    news_list = f.readlines()


for new in news_list:
    if str(new[-5:]) == str('文字版/\n'):
        print(new)
        with open(file_path, mode='a', encoding='utf-8') as f2:
            f2.write(str(new))

    else:
        continue