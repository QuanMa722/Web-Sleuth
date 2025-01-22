# -*- coding: utf-8 -*-

import os

def clean_and_count_lines(folder_path):
    total_lines = 0
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)

            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            non_empty_lines = [line for line in lines if line.strip() != '']
            num_lines = len(non_empty_lines)
            total_lines += num_lines

            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(non_empty_lines)

            print(f"File: {filename}, Number of non-empty lines: {num_lines}")

    print(f"Total non-empty lines processed in this folder: {total_lines}")
    print(

    )
    return total_lines

def main():
    base_folder = '.'
    total_count = 0
    for year in range(2015, 2026):
        folder_path = os.path.join(base_folder, str(year))

        if os.path.exists(folder_path):
            print(f"Processing folder: {folder_path}")
            total_lines = clean_and_count_lines(folder_path)
            total_count += total_lines

    print(f"Total non-empty lines processed across all years: {total_count}")

if __name__ == "__main__":
    main()

