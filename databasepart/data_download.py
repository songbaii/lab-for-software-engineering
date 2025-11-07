import requests
import zipfile
import os
import pandas as pd
import pymysql

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

def data_load():
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

    # 2. 导入电影数据 (movies.dat)
    # 格式: MovieID::Title::Genres
    movies_file = os.path.join(data_path, "movies.dat")
    movies = pd.read_csv(movies_file,
                        sep='::',
                        engine='python',
                        names=['MovieID', 'Title', 'Genres'],
                        encoding='utf-8')

    # 3. 导入简评数据 (tag.dat)
    # 格式: UserID::MovieID::Tag::Timestamp
    tags_file = os.path.join(data_path, "tags.dat")
    tags = pd.read_csv(tags_file,
                       sep='::',
                       engine='python',
                       names=['UserID', 'MovieID', 'Tag', 'Timestamp'],
                       encoding='utf-8')

    # 显示数据基本信息
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

def data_import(ratings, movies, tags):
    # 插入数据集到数据库
    ratings.drop('Timestamp', axis=1, inplace=True)
    tags.drop('Timestamp', axis=1, inplace=True)
    print("开始插入数据到数据库")

    db_config = {  # 对应数据库的链接信息
        'host': 'localhost',
        'user': 'violet',
        'password': 's131601',
        'database': 'soft_ware_engineering',
        'charset': 'utf8mb4'
    }

    connection = pymysql.connect(**db_config)


def main():
    download_movielens()
    ratings, movies, tags = data_load()
    data_import(ratings, movies, tags)

if __name__ == '__main__':
    main()