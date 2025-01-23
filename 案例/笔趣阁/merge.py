# -*- coding: utf-8 -*-

import os
import re


def merge_txt_files(folder_path, output_file):
    all_text = []
    txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
    txt_files.sort(key=lambda f: int(re.match(r'(\d+)_', f).group(1)))

    ads_to_remove = {
        '『点此报错』',
        '『加入书签』',
        '请收藏本站：https://www.bigee.cc。笔趣阁手机版：https://m.bigee.cc'
    }

    for filename in txt_files:
        file_path = os.path.join(folder_path, filename)

        with open(file_path, mode='r', encoding='utf-8') as file:
            lines = file.readlines()
            filtered_lines = [line for line in lines if line.strip() not in ads_to_remove]
            all_text.append(f'## {filename}')
            all_text.append(''.join(filtered_lines))

    with open(output_file, mode='w', encoding='utf-8') as output:
        output.write('\n'.join(all_text))


if __name__ == '__main__':
    try:
        folder_path = '万历十五年'
        output_file = '万历十五年.txt'

        if os.path.exists(output_file):
            print(f"The file '{output_file}' already exists.")
        else:
            merge_txt_files(folder_path, output_file)

    except Exception as error:
        print(f"An error occurred: {error}.")
