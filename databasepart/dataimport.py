import pandas as pd
import urllib.request
import os
import urllib.request
import gzip
import shutil

def download_imdb_data_smart(force_redownload=False):
    """
    智能下载IMDb数据

    Args:
        force_redownload (bool): 是否强制重新下载
    """
    base_url = "https://datasets.imdbws.com/"
    files = [
        "title.basics.tsv.gz",
        "title.ratings.tsv.gz",
        "title.crew.tsv.gz",
        "title.principals.tsv.gz",
        "name.basics.tsv.gz"
    ]

    downloaded_count = 0
    skipped_count = 0

    for file in files:
        gz_file = file
        extracted_file = file.replace('.gz', '')

        # 检查是否需要处理
        if not force_redownload and os.path.exists(extracted_file):
            file_size = os.path.getsize(extracted_file)
            if file_size > 1000:  # 文件大小合理（大于1KB）
                print(f"✅ 跳过 {extracted_file} (文件已存在, {file_size:,} bytes)")
                skipped_count += 1
                continue

        # 下载压缩文件（如果需要）
        if force_redownload or not os.path.exists(gz_file):
            print(f"⬇️  下载 {file}...")
            try:
                urllib.request.urlretrieve(base_url + file, gz_file)
                gz_size = os.path.getsize(gz_file)
                print(f"✅ 下载完成: {file} ({gz_size:,} bytes)")
            except Exception as e:
                print(f"❌ 下载失败: {e}")
                continue
        else:
            print(f"📦 使用现有压缩文件: {gz_file}")

        # 解压文件
        print(f"🔧 解压 {gz_file}...")
        try:
            with gzip.open(gz_file, 'rb') as f_in:
                with open(extracted_file, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)

            extracted_size = os.path.getsize(extracted_file)
            print(f"✅ 解压完成: {extracted_file} ({extracted_size:,} bytes)")
            downloaded_count += 1

        except Exception as e:
            print(f"❌ 解压失败: {e}")
            # 删除可能损坏的文件
            if os.path.exists(extracted_file):
                os.remove(extracted_file)

    print(f"\n📊 总结: 下载了 {downloaded_count} 个文件, 跳过了 {skipped_count} 个已存在文件")

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

def load_imdb_data(show_movies_head = False, show_movies_type = False, show_rating_range = False):
    # 加载电影基本信息
    movies_df = pd.read_csv('title.basics.tsv', sep='\t', low_memory=False)
    movies_df = movies_df[movies_df['titleType'] == 'movie']
    # 加载评分信息
    ratings_df = pd.read_csv('title.ratings.tsv', sep='\t')
    # 合并数据
    movies_with_ratings = pd.merge(movies_df, ratings_df, on='tconst', how='inner')
    # 进行数据清洗
    movies_with_ratings.drop('titleType', axis=1, inplace=True)
    movies_with_ratings.drop('originalTitle', axis=1, inplace=True)
    movies_with_ratings.drop('endYear', axis=1, inplace=True)
    movies_with_ratings = clean_imdb_data(movies_with_ratings)
    # 数据类型转换
    movies_with_ratings['startYear'] = pd.to_numeric(movies_with_ratings['startYear'])
    movies_with_ratings['runtimeMinutes'] = pd.to_numeric(movies_with_ratings['runtimeMinutes'])
    if show_movies_head:
        print(movies_with_ratings.head())
    if show_movies_type:
        print(movies_with_ratings.info())
    if show_rating_range:
        print(movies_with_ratings['averageRating'].min())
        print(movies_with_ratings['averageRating'].max())
    return movies_with_ratings

def main():
    # 永久设置显示选项（在当前会话中有效）
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.width', None)
    # 下载数据
    force_redownload = False  # 是否强制下载
    download_imdb_data_smart(force_redownload)
    # 使用数据
    show_movies_head = True
    show_movies_type = False
    show_rating_range = False
    movies_data = load_imdb_data(show_movies_head, show_movies_type, show_rating_range)  # 需要单独建表movie

    principals_data = pd.read_csv('title.principals.tsv', sep='\t')
    principals_data = principals_data[principals_data['tconst'].isin(movies_data['tconst'])]
    principals_data.drop('job', axis=1, inplace=True)
    principals_data.drop('characters', axis=1, inplace=True)
    principals_data.reset_index(drop=True, inplace=True)
    test_nan = False # 对表中是否有nan进行测试和清洗
    if test_nan:
        principals_data = clean_imdb_data(principals_data)
    print(principals_data.head(10))

    name_data = pd.read_csv('name.basics.tsv', sep='\t', low_memory=False)
    name_data = name_data[name_data['nconst'].isin(principals_data['nconst'])]
    name_data.drop('primaryProfession', axis=1, inplace=True)
    name_data.drop('knownForTitles', axis=1, inplace=True)
    name_data.reset_index(drop=True, inplace=True)
    # 选择除 deathYear 外的所有列
    columns_to_check = [col for col in name_data.columns if col != 'deathYear' and col != 'birthYear']
    # 检测这些列中是否存在 \N
    has_backslash_n = name_data[columns_to_check].eq('\\N').any().any()
    print(f"除deathYear外其他列是否存在 \\N: {has_backslash_n}")
    if has_backslash_n:
        # 找出在指定列中包含 \N 的行
        mask = name_data[columns_to_check].eq('\\N').any(axis=1)
        rows_with_backslash_n = name_data[mask]

        print("\n包含 \\N 的行数据:")
        print(rows_with_backslash_n)
    print(name_data.head())

if __name__ == "__main__":
    main()
