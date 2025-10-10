from operator import truediv

import pandas as pd
import urllib.request
import gzip
import shutil

# IMDb 官方数据下载链接
def download_imdb_data():
    base_url = "https://datasets.imdbws.com/"
    files = [
        "title.basics.tsv.gz",  # 基本信息
        "title.ratings.tsv.gz",  # 评分信息
        "title.crew.tsv.gz",  # 导演和编剧
        "title.principals.tsv.gz",  # 主要演员
        "name.basics.tsv.gz"  # 人物信息
    ]

    for file in files:
        print(f"下载 {file}...")
        urllib.request.urlretrieve(base_url + file, file)

        # 解压文件
        with gzip.open(file, 'rb') as f_in:
            with open(file.replace('.gz', ''), 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        print(f"解压完成: {file}")

def clean_imdb_data(df):
    """
    专门清理IMDb数据的函数
    """
    print("开始清理IMDb数据...")
    print(f"原始数据形状: {df.shape}")

    # 1. 替换所有 \N 为 NaN
    df_clean = df.replace('\\N', pd.NA)

    # 2. 显示清理前的空值情况
    print("\n清理前空值统计:")
    null_summary = df_clean.isna().sum()
    for col, null_count in null_summary.items():
        if null_count > 0:
            print(f"  {col}: {null_count} 个空值")

    # 3. 删除所有包含空值的行
    df_clean = df_clean.dropna()

    # 4. 重置索引
    df_clean = df_clean.reset_index(drop=True)

    print(f"\n清理后数据形状: {df_clean.shape}")
    print(f"删除了 {len(df) - len(df_clean)} 行数据")

    return df_clean

def load_imdb_data():
    # 加载电影基本信息
    movies_df = pd.read_csv('title.basics.tsv', sep='\t', low_memory=False)
    movies_df = movies_df[movies_df['titleType'] == 'movie']
    # 加载评分信息
    ratings_df = pd.read_csv('title.ratings.tsv', sep='\t')
    # 合并数据
    movies_with_ratings = pd.merge(movies_df, ratings_df, on='tconst', how='inner')
    crew_df = pd.read_csv('title.crew.tsv', sep='\t')
    movies_with_ratings_and_crew = movies_with_ratings.merge(crew_df, on='tconst', how='inner')
    # 进行数据清洗
    movies_with_ratings_and_crew.drop('titleType', axis=1, inplace=True)
    movies_with_ratings_and_crew.drop('originalTitle', axis=1, inplace=True)
    movies_with_ratings_and_crew.drop('endYear', axis=1, inplace=True)
    movies_with_ratings_and_crew = clean_imdb_data(movies_with_ratings_and_crew)
    return movies_with_ratings_and_crew

def main():
    show_all_columns = True # 是否显示所有的行
    download = False # 是否进行下载
    # 永久设置显示选项（在当前会话中有效）
    if show_all_columns:
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_colwidth', None)
        pd.set_option('display.width', None)
    # 下载数据
    if download:
        download_imdb_data()
    # 使用数据
    movies_data = load_imdb_data()  # 需要单独建表movie
    print(movies_data.head())
    print(movies_data.info())
    # principals_data = pd.read_csv('title.principals.tsv', sep='\t', low_memory=False)  # 需要单独建表
    # principals_data = clean_imdb_data(principals_data)
    # print(principals_data.head())
    # name_data = pd.read_csv('name.basics.tsv', sep='\t', low_memory=False)
    # name_data = clean_imdb_data(name_data)
    # print(name_data.head())

if __name__ == "__main__":
    main()
