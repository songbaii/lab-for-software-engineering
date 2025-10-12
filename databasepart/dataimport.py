import pandas as pd
import urllib.request
import os
import urllib.request
import gzip
import shutil
import pymysql

db_config = {# 对应数据库的链接信息
        'host': 'localhost',
        'user': 'violet',
        'password': 's131601',
        'database': 'soft_ware_engineering',
        'charset': 'utf8mb4'
    }

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

def load_imdb_data(show_movies_head = False, show_movies_type = False, show_range = False):
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
    if show_range:
        print(movies_with_ratings['averageRating'].min())
        print(movies_with_ratings['averageRating'].max())
        print(movies_with_ratings['startYear'].min())
        print(movies_with_ratings['startYear'].max())
    return movies_with_ratings

def nan_test(name_data):
    columns_to_check = [col for col in name_data.columns if col != 'deathYear' and col != 'birthYear']
    # 检测这些列中是否存在 \N
    has_backslash_n = name_data[columns_to_check].eq('\\N').any().any()
    print(f"除deathYear和birthYear外其他列是否存在 \\N: {has_backslash_n}")
    if has_backslash_n:
        # 找出在指定列中包含 \N 的行
        mask = name_data[columns_to_check].eq('\\N').any(axis=1)
        rows_with_backslash_n = name_data[mask]

        print("\n包含 \\N 的行数据:")
        print(rows_with_backslash_n)

def insert_movie_data(df):
    """批量插入电影数据"""

    # 建立数据库连接
    connection = pymysql.connect(**db_config)

    try:
        with connection.cursor() as cursor:
            # 构建批量插入的VALUES部分
            values_placeholders = []
            data_values = []

            for index, row in df.iterrows():
                # 处理可能的NaN值
                start_year = row['startYear'] if pd.notna(row['startYear']) else None
                runtime = row['runtimeMinutes'] if pd.notna(row['runtimeMinutes']) else None
                rating = row['averageRating'] if pd.notna(row['averageRating']) else None
                votes = row['numVotes'] if pd.notna(row['numVotes']) else None

                values_placeholders.append("(%s, %s, %s, %s, %s, %s, %s)")
                data_values.extend([
                    row['tconst'],
                    row['primaryTitle'],
                    row['isAdult'],
                    start_year,
                    runtime,
                    rating,
                    votes
                ])

            # 构建完整的INSERT语句
            insert_sql = f"""
            INSERT ignore INTO movie 
            (movie_id, movie_name, isAdult, release_year, runtime_minutes, average_rating, numVotes) 
            VALUES {','.join(values_placeholders)}
            """

            # 执行插入
            cursor.execute(insert_sql, data_values)
            connection.commit()
            print(f"成功批量插入 {len(df)} 条数据")

    except Exception as e:
        print(f"插入数据时出错: {e}")
        connection.rollback()
    finally:
        connection.close()

def process_genres_and_movies(df):
    """处理电影类型数据并填充两个表"""

    # 1. 首先提取所有唯一的电影类型
    all_genres = set()
    for genres in df['genres']:
        if pd.notna(genres):
            # 分割以逗号分隔的类型字符串
            genre_list = [genre.strip() for genre in genres.split(',')]
            all_genres.update(genre_list)

    print(f"发现 {len(all_genres)} 个唯一电影类型:")
    for genre in sorted(all_genres):
        print(f"  - {genre}")

    # 2. 建立genre_id映射
    genre_to_id = {}
    for idx, genre_name in enumerate(sorted(all_genres), 1):
        genre_to_id[genre_name] = idx

    # 3. 连接数据库
    connection = pymysql.connect(**db_config)

    try:
        with connection.cursor() as cursor:

            # 4. 插入genre_table数据
            print("\n正在插入genre_table数据...")
            genre_insert_sql = "INSERT IGNORE INTO genre_table (genre_id, genre_name) VALUES (%s, %s)"
            genre_data = [(genre_id, genre_name) for genre_name, genre_id in genre_to_id.items()]

            cursor.executemany(genre_insert_sql, genre_data)
            print(f"插入 {len(genre_data)} 个电影类型到genre_table")

            # 5. 插入movie_genre关系数据
            print("\n正在插入movie_genre关系数据...")
            movie_genre_data = []

            for index, row in df.iterrows():
                movie_id = row['tconst']
                genres_str = row['genres']

                if pd.notna(genres_str):
                    genre_list = [genre.strip() for genre in genres_str.split(',')]

                    for genre_name in genre_list:
                        genre_id = genre_to_id.get(genre_name)
                        if genre_id:
                            movie_genre_data.append((movie_id, genre_id))

            # 批量插入movie_genre关系
            if movie_genre_data:
                movie_genre_sql = "INSERT IGNORE INTO movie_genre (movie_id, genre_id) VALUES (%s, %s)"
                cursor.executemany(movie_genre_sql, movie_genre_data)
                print(f"插入 {len(movie_genre_data)} 个电影-类型关系到movie_genre表")

            connection.commit()
            print("\n✅ 所有数据插入完成!")

            # 6. 验证插入结果
            print("\n验证插入结果:")
            cursor.execute("SELECT COUNT(*) FROM genre_table")
            genre_count = cursor.fetchone()[0]
            print(f"genre_table中的记录数: {genre_count}")

            cursor.execute("SELECT COUNT(*) FROM movie_genre")
            movie_genre_count = cursor.fetchone()[0]
            print(f"movie_genre中的记录数: {movie_genre_count}")

            # 显示一些样本数据
            print("\ngenre_table样本数据:")
            cursor.execute("SELECT * FROM genre_table ORDER BY genre_id LIMIT 10")
            for genre_id, genre_name in cursor.fetchall():
                print(f"  {genre_id}: {genre_name}")

            print("\nmovie_genre样本数据:")
            cursor.execute("""
                           SELECT mg.movie_id, m.movie_name, g.genre_name
                           FROM movie_genre mg
                                    JOIN movie m ON mg.movie_id = m.movie_id
                                    JOIN genre_table g ON mg.genre_id = g.genre_id
                           LIMIT 10
                           """)
            for movie_id, movie_name, genre_name in cursor.fetchall():
                print(f"  {movie_id} ({movie_name}) - {genre_name}")

    except Exception as e:
        print(f"操作失败: {e}")
        connection.rollback()
    finally:
        connection.close()

    return genre_to_id


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
    show_range = False
    movies_data = load_imdb_data(show_movies_head, show_movies_type, show_range)  # 需要单独建表movie
    # 使用示例
    insert_movie_data(movies_data)
    process_genres_and_movies(movies_data)
    '''principals_data = pd.read_csv('title.principals.tsv', sep='\t')
    principals_data = principals_data[principals_data['tconst'].isin(movies_data['tconst'])]
    principals_data.drop('job', axis=1, inplace=True)
    principals_data.drop('characters', axis=1, inplace=True)
    principals_data.reset_index(drop=True, inplace=True)
    test_nan_principal = False # 对表中是否有nan进行测试和清洗
    if test_nan_principal:
        principals_data = clean_imdb_data(principals_data)
    test_principal_type = True
    if test_principal_type:
        print(principals_data.info())
    # 检测包含逗号的行
    test_comma = False
    if test_comma:
        comma_rows = principals_data[principals_data['category'].str.contains(',', na=False)]
        print(f"包含逗号的行数: {len(comma_rows)}")
        # 显示包含逗号的样本数据
        if len(comma_rows) > 0:
            print("包含逗号的样本数据:")
            print(comma_rows.head())

    name_data = pd.read_csv('name.basics.tsv', sep='\t', low_memory=False)
    name_data = name_data[name_data['nconst'].isin(principals_data['nconst'])]
    name_data.drop('primaryProfession', axis=1, inplace=True)
    name_data.drop('knownForTitles', axis=1, inplace=True)
    name_data.reset_index(drop=True, inplace=True)
    # 选择除 deathYear和birthYear 外的所有列进行检测
    test_nan_name = False
    if test_nan_name:
        nan_test(name_data)
    print(name_data.head())
    test_name_type = True
    if test_name_type:
        print(name_data.info())
    # 数据完整性测试完毕'''
if __name__ == "__main__":
    main()
