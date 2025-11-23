import requests
import zipfile
import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.engine import connection_memoize
from dotenv import load_dotenv

# 数据库链接语句
connection_string_set = "mysql+pymysql://violet:s131601@localhost:3306/soft_ware_engineering"
# connection_string = "mysql+pymysql://user:passowrd@localhost:端口/数据库"

def download_movielens():
    """下载数据集"""
    dataset_size = "10M100K"
    url = "https://files.grouplens.org/datasets/movielens/ml-10m.zip"
    filename = f"ml-{dataset_size}.zip"
    extract_path = f"./movielens_data"

    if os.path.exists(f"{extract_path}/ml-{dataset_size}"):
        print(f"{dataset_size}数据集先前已经下载完毕")
        return

    os.makedirs(extract_path, exist_ok=True)

    try:
        print(f"正在下载MovieLens {dataset_size.upper()} 数据集...")
        response = requests.get(url, stream=True)
        response.raise_for_status()

        # 显示下载进度
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0

        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                downloaded += len(chunk)
                if total_size > 0:
                    progress = (downloaded / total_size) * 100
                    print(f"\r下载进度: {progress:.1f}%", end="")

        print("\n下载完成，正在解压...")
        with zipfile.ZipFile(filename, 'r') as zip_ref:
            # 解压所有文件
            zip_ref.extractall(extract_path)
        os.remove(filename)
        print(f"数据集已保存到: {extract_path}")

    except Exception as e:
        print(f"下载失败: {e}")

def data_load(show = False):
    # 设置pandas显示选项，取消省略号
    pd.set_option('display.max_columns', None)  # 显示所有列
    pd.set_option('display.max_rows', None)     # 显示所有行
    pd.set_option('display.width', None)        # 不限制显示宽度
    pd.set_option('display.max_colwidth', None) # 不限制列宽

    # 设置数据文件路径
    data_path = "movielens_data/ml-10M100K"

    print("开始导入数据")

    # 1. 导入评分数据 (ratings.dat)
    # 格式: UserID::MovieID::Rating::Timestamp
    ratings_file = os.path.join(data_path, "ratings.dat")
    ratings = pd.read_csv(ratings_file,
                         sep='::',
                         engine='python',
                         names=['UserID', 'MovieID', 'Rating', 'Timestamp'],
                         encoding='utf-8')

    # print(ratings['Rating'].describe())

    # 2. 导入电影数据 (movies.dat)
    # 格式: MovieID::Title::Genres
    movies_file = os.path.join(data_path, "movies.dat")
    movies = pd.read_csv(movies_file,
                        sep='::',
                        engine='python',
                        names=['MovieID', 'Title', 'Genres'],
                        encoding='utf-8')

    # print(movies['MovieID'].describe())

    # 3. 导入简评数据 (tag.dat)
    # 格式: UserID::MovieID::Tag::Timestamp
    tags_file = os.path.join(data_path, "tags.dat")
    tags = pd.read_csv(tags_file,
                       sep='::',
                       engine='python',
                       names=['UserID', 'MovieID', 'Tag', 'Timestamp'],
                       encoding='utf-8')
    # 显示数据基本信息
    if show:
        print("评分数据形状:", ratings.shape)
        print("电影数据形状:", movies.shape)
        print("简评数据形状:", tags.shape)

        print("\n评分数据前5行:")
        print(ratings.head())

        print("\n电影数据前5行:")
        print(movies.head())

        print("\n用户简评数据前5行:")
        print(tags.head())
    return ratings, movies, tags

def insert_with_ignore(table, conn, keys, data_iter):
    """
    支持批量插入并忽略重复记录的自定义插入函数
    """
    table_name = table.name
    data = [dict(zip(keys, row)) for row in data_iter]

    if not data:
        return

    # 构建批量INSERT IGNORE语句
    columns = ', '.join(f'`{k}`' for k in keys)
    placeholders = ', '.join([f':{k}' for k in keys])

    sql = f"INSERT IGNORE INTO `{table_name}` ({columns}) VALUES ({placeholders})"

    # 使用text()包装SQL语句
    stmt = text(sql)

    # 执行批量插入
    conn.execute(stmt, data)

def movie_insert(movies, connection_string):
    # 创建数据库连接
    engine = create_engine(connection_string)

    movies_to_insert = movies[['MovieID', 'Title', 'Year']].copy()
    movies_to_insert.columns = ['movie_id', 'movie_name', 'release_year']
    print(f"找到{len(movies_to_insert)}部电影")
    print(movies_to_insert.head())
    # 插入数据到数据库
    movies_to_insert.to_sql(
        name='movie',
        con=engine,
        if_exists='append',  #
        index=False,  # 不插入DataFrame索引
        method=insert_with_ignore  # 批量插入提高性能
    )
    print(f"成功插入 {len(movies_to_insert)} 条电影数据")

def extract_genres_pandas(movie_data, database_url):
    """
    使用pandas方法提取电影类型
    """
    # 提取所有唯一的电影类型
    all_genres = set()

    # 使用apply和split提取所有类型
    movie_data['Genres'].apply(lambda x: all_genres.update(x.split('|')))

    # 创建genre DataFrame
    genres_df = pd.DataFrame({
        'genre_id': range(1, len(all_genres) + 1),
        'genre_name': sorted(list(all_genres))
    })

    print(f"找到 {len(genres_df)} 个唯一的电影类型:")
    print(genres_df)

    # 插入到数据库
    engine = create_engine(database_url)
    genres_df.to_sql('genre_table', engine, if_exists='append', index=False, method=insert_with_ignore )

    print("电影类型数据插入完成！")

def create_movie_genre_relations(movie_data, connection_string):
    """
    创建电影与类型的关系数据并插入到movie_genre表
    """
    engine = create_engine(connection_string)

    # 创建类型名称到ID的映射字典
    all_genres = set()

    # 使用apply和split提取所有类型
    movie_data['Genres'].apply(lambda x: all_genres.update(x.split('|')))

    # 创建genre DataFrame
    genres_df = pd.DataFrame({
        'genre_id': range(1, len(all_genres) + 1),
        'genre_name': sorted(list(all_genres))
    })
    genre_name_to_id = dict(zip(genres_df['genre_name'], genres_df['genre_id']))
    print("类型映射字典:", genre_name_to_id)

    # 准备插入的数据
    movie_genre_data = []

    for _, movie in movie_data.iterrows():
        movie_id = movie['MovieID']
        genres_str = movie['Genres']

        # 分割类型字符串
        genre_names = genres_str.split('|')

        # 为每个类型创建关系记录
        for genre_name in genre_names:
            genre_id = genre_name_to_id.get(genre_name)
            if genre_id:
                movie_genre_data.append({
                    'movie_id': movie_id,
                    'genre_id': genre_id
                })
            else:
                print(f"警告: 未找到类型 '{genre_name}' 的映射")

    # 创建DataFrame
    movie_genre_df = pd.DataFrame(movie_genre_data)

    if not movie_genre_data:
        print("没有找到可插入的关系数据")
        return

    print(f"准备插入 {len(movie_genre_df)} 条电影-类型关系记录")
    print(movie_genre_df.head())

    # 插入到数据库
    try:
        movie_genre_df.to_sql('movie_genre', engine, if_exists='append', index=False, method=insert_with_ignore )
        print("电影-类型关系数据插入完成！")
    except Exception as e:
        print(f"插入数据时出错: {e}")

def create_user_table_batch(ratings_df, tags_df, connection_string):
    """
    批量插入版本，性能更好
    """
    engine = create_engine(connection_string)

    # 提取所有唯一的用户ID
    users_from_ratings = set(ratings_df['UserID'].unique())
    users_from_tags = set(tags_df['UserID'].unique())
    all_user_ids = sorted(list(users_from_ratings.union(users_from_tags)))

    users_df = pd.DataFrame({
        'user_id': all_user_ids,
        'password': ['0'] * len(all_user_ids),
        'user_name': [None] * len(all_user_ids)
    })

    print(f"找到{len(users_df)}个用户")
    print(users_df.head())
    users_df.to_sql('user', engine, if_exists='append', index=False, method=insert_with_ignore )

    print("用户数据插入成功")

def insert_user_judge_pandas(df, connection_string):
    """
    使用pandas的to_sql方法插入数据（需要SQLAlchemy）
    """

    # 创建SQLAlchemy引擎
    engine = create_engine(connection_string)

    # 重命名列以匹配数据库表结构
    df_db = df.rename(columns={
        'UserID': 'user_id',
        'MovieID': 'movie_id',
        'Rating': 'rating'
    })

    # 插入数据，如果存在重复则更新
    df_db.to_sql(
        name='user_judge',
        con=engine,
        if_exists='append',
        index=False,
        method=insert_with_ignore
    )
    print("成功插入测试用户和电影的评分数据")

def insert_user_comment_pandas(df, connection_string):
    """
    使用pandas的to_sql方法插入数据（需要SQLAlchemy）
    """
    # 创建SQLAlchemy引擎
    engine = create_engine(connection_string)

    # 重命名列以匹配数据库表结构
    df_db = df.rename(columns={
        'UserID': 'user_id',
        'MovieID': 'movie_id',
        'Tag': 'comment'
    })

    # 插入数据
    df_db.to_sql(
        name='user_comment',
        con=engine,
        if_exists='append',
        index=False,
        method=insert_with_ignore
    )

    print("成功插入测试用户评价数据数据")

def data_import(ratings, movies, tags):
    # 插入数据集到数据库
    # 先进行数据处理
    ratings.drop('Timestamp', axis=1, inplace=True)
    tags.drop('Timestamp', axis=1, inplace=True)
    movies["Year"] = movies['Title'].str.extract(r'(\d{4})')
    movies['Title'] = movies['Title'].str.replace(r'\s*\(\d{4}\)$', '', regex=True)
    # print(movies.head())
    # print(ratings.head())
    # print(tags.head())
    # connection_string = "mysql+pymysql://violet:s131601@localhost:3306/soft_ware_engineering"
    # 从环境变量读取数据库连接信息
    load_dotenv()
    connection_string = (
        f"mysql+pymysql://"
        f"{os.getenv('MYSQL_USER', 'violet')}:"
        f"{os.getenv('MYSQL_PASSWORD', 's131601')}@"
        f"{os.getenv('MYSQL_HOST', 'localhost')}:"
        f"{os.getenv('MYSQL_PORT', '3306')}/"
        f"{os.getenv('MYSQL_DB', 'soft_ware_engineering')}"
    )
    print("开始插入数据到数据库")
    movie_insert(movies, connection_string)
    print("开始插入类别到数据库")
    extract_genres_pandas(movies, connection_string)
    print("开始建立电影和类别的联系")
    create_movie_genre_relations(movies, connection_string)
    print("开始插入测试用户数据")
    create_user_table_batch(ratings, tags, connection_string)
    print("开始插入测试用户和电影的评分数据")
    insert_user_judge_pandas(ratings, connection_string)
    print("开始插入测试用户评价数据")
    insert_user_comment_pandas(tags, connection_string)



def main():
    download_movielens()
    ratings, movies, tags = data_load()
    data_import(ratings, movies, tags)

if __name__ == '__main__':
    main()