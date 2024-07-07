# -*- coding: utf-8 -*-

import pandas as pd


class CSVDuplicatesRemover:

    def __init__(self, file_path):
        self.file_path = file_path

    def remove_duplicates(self):
        df = pd.read_csv(self.file_path)
        df_deduped = df.drop_duplicates()
        df_deduped.to_csv(self.file_path, index=False)
        print(f"Deduplicated data saved to {self.file_path}")


if __name__ == '__main__':
    file_path = 'comments.csv'
    remover = CSVDuplicatesRemover(file_path)
    remover.remove_duplicates()



