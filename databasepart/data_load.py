import pandas as pd
import os


def simple_load_movielens(dataset_size="100k"):
    """
    数据加载
    参数:
    dataset_size: 数据集大小，可选 "100k", "1m", "10m", "25m"
    """
    base_path = f"./movielens_data/ml-{dataset_size}"

    # 加载核心三个表
    if dataset_size == "100k":
        users = pd.read_csv(f"{base_path}/u.user", sep='|',
                            names=['user_id', 'age', 'gender', 'occupation', 'zip_code'])
        movies = pd.read_csv(f"{base_path}/u.item", sep='|', encoding='latin-1',
                             names=['movie_id', 'title', 'release_date', 'video_release_date',
                                    'imdb_url'] + [f'genre_{i}' for i in range(19)])
        ratings = pd.read_csv(f"{base_path}/u.data", sep='\t',
                              names=['user_id', 'movie_id', 'rating', 'timestamp'])
    else:
        users = pd.read_csv(f"{base_path}/users.dat", sep='::',
                            names=['user_id', 'gender', 'age', 'occupation', 'zip_code'],
                            engine='python')
        movies = pd.read_csv(f"{base_path}/movies.dat", sep='::',
                             names=['movie_id', 'title', 'genres'], engine='python')
        ratings = pd.read_csv(f"{base_path}/ratings.dat", sep='::',
                              names=['user_id', 'movie_id', 'rating', 'timestamp'],
                              engine='python')

    return {
        'users': users,
        'movies': movies,
        'ratings': ratings
    }


# 快速使用
if __name__ == "__main__":
    # 使用简化版
    data = simple_load_movielens("100k")

    print("用户表:")
    print(data['users'].head())
    print("\n电影表:")
    print(data['movies'].head())
    print("\n评分表:")
    print(data['ratings'].head())