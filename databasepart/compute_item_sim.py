import pymysql
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm
import gc
import warnings
from config import DB_CONFIG

warnings.filterwarnings("ignore", category=UserWarning)  # ignore sparse matmul warning

BATCH_SIZE = 200_000  # 每批拉取 20 万条评分（根据内存调整）
TOP_K = 100           # 每个电影保留 top 100 相似
MIN_SIM = 0.01        # 过滤极低相似度
SIM_TABLE = 'item_similarities'

def connect_db():
    return pymysql.connect(**DB_CONFIG)

def build_rating_matrix(conn):
    """
    分批拉取 user_judge 表，构建稀疏评分矩阵 R (users × movies)
    返回: R (csr_matrix), user_id_to_idx, idx_to_user_id, movie_id_to_idx, idx_to_movie_id
    """
    print("🔍 正在获取用户和电影 ID 映射...")
    with conn.cursor() as cur:
        cur.execute("SELECT user_id FROM user ORDER BY user_id")
        users = [row[0] for row in cur.fetchall()]
        cur.execute("SELECT movie_id FROM movie ORDER BY movie_id")
        movies = [row[0] for row in cur.fetchall()]
    
    user_id_to_idx = {uid: i for i, uid in enumerate(users)}
    idx_to_user_id = {i: uid for uid, i in user_id_to_idx.items()}
    movie_id_to_idx = {mid: i for i, mid in enumerate(movies)}
    idx_to_movie_id = {i: mid for mid, i in movie_id_to_idx.items()}
    
    n_users = len(users)
    n_movies = len(movies)
    print(f"📊 共 {n_users} 用户, {n_movies} 电影")
    
    # 分批拉取评分
    rows, cols, data = [], [], []
    offset = 0
    
    print("📥 正在分批拉取评分数据...")
    with conn.cursor() as cur:
        while True:
            cur.execute("""
                SELECT user_id, movie_id, rating 
                FROM user_judge 
                ORDER BY user_id, movie_id 
                LIMIT %s OFFSET %s
            """, (BATCH_SIZE, offset))
            batch = cur.fetchall()
            if not batch:
                break
                
            for user_id, movie_id, rating in batch:
                rows.append(user_id_to_idx[user_id])
                cols.append(movie_id_to_idx[movie_id])
                data.append(float(rating))
            
            offset += len(batch)
            if offset % 1_000_000 == 0:
                print(f"  已加载 {offset} 条评分...")
    
    print(f"✅ 共加载 {len(data)} 条评分")
    
    # 构建稀疏矩阵 (users × movies)
    R = csr_matrix((data, (rows, cols)), shape=(n_users, n_movies), dtype=np.float32)
    print(f"📈 评分矩阵 shape: {R.shape}, sparsity: {1 - R.nnz / (R.shape[0]*R.shape[1]):.4%}")
    
    return R, user_id_to_idx, idx_to_user_id, movie_id_to_idx, idx_to_movie_id

def compute_and_save_similarities(conn, R, movie_id_to_idx, idx_to_movie_id, top_k=TOP_K, min_sim=MIN_SIM):
    """
    计算物品相似度（R.T → movies × users），取 Top-K 存入 MySQL
    """
    print("🔄 正在转置矩阵为物品-用户矩阵...")
    R_item_user = R.T  # shape: (n_movies, n_users)
    
    n_movies = R_item_user.shape[0]
    print(f"🎬 共 {n_movies} 部电影，开始计算相似度...")
    
    # 分块计算相似度（防内存爆炸）
    block_size = 1000  # 每次计算 1000 部电影的相似度
    total_written = 0
    
    with conn.cursor() as cur:
        # 先清空表（可选；若增量更新则注释）
        cur.execute(f"TRUNCATE TABLE {SIM_TABLE}")
        conn.commit()
        
        for start in tqdm(range(0, n_movies, block_size), desc="计算相似度块"):
            end = min(start + block_size, n_movies)
            block = R_item_user[start:end]
            
            # 计算当前 block 与所有电影的相似度
            sims = cosine_similarity(block, R_item_user)  # shape: (block_size, n_movies)
            
            # 为每部电影找 top-k 相似（排除自身）
            for i in range(sims.shape[0]):
                movie_idx = start + i
                sim_row = sims[i]
                
                # 排除自身：设相似度为 -1
                sim_row[movie_idx] = -1.0
                
                # 取 top-k 且 > min_sim
                top_k_idx = np.argpartition(-sim_row, kth=min(top_k, len(sim_row)-1))[:top_k]
                # 二次排序（argpartition 不保序）
                top_k_idx = top_k_idx[np.argsort(-sim_row[top_k_idx])]
                
                insert_data = []
                for j in top_k_idx:
                    sim_val = float(sim_row[j])
                    if sim_val < min_sim or sim_val <= 0:
                        break
                    # 映射回原始 movie_id
                    orig_mid = idx_to_movie_id[movie_idx]
                    sim_mid = idx_to_movie_id[j]
                    insert_data.append((orig_mid, sim_mid, round(sim_val, 4)))
                
                if insert_data:
                    # 批量插入（防 SQL 注入用 executemany）
                    cur.executemany(
                        f"INSERT INTO {SIM_TABLE} (movie_id, similar_movie_id, similarity) "
                        f"VALUES (%s, %s, %s)",
                        insert_data
                    )
                    total_written += len(insert_data)
            
            # 每块提交一次（防长事务）
            conn.commit()
            
            # 清理内存
            del sims, block
            gc.collect()
        
        print(f"✅ 共写入 {total_written} 条相似度记录到 {SIM_TABLE}")

def main():
    conn = connect_db()
    try:
        R, _, _, movie_id_to_idx, idx_to_movie_id = build_rating_matrix(conn)
        compute_and_save_similarities(conn, R, movie_id_to_idx, idx_to_movie_id)
        print("🎉 相似度计算与存储完成！")
    finally:
        conn.close()

if __name__ == "__main__":
    main()