import pymysql
from collections import defaultdict
from config import DB_CONFIG

def get_popular_movies(conn, top_k: int, cursor=None):
    # ✅ 使用 movie_stats 汇总表，不再碰 user_judge 大表！
    sql = """
    SELECT 
        m.movie_id,
        m.movie_name,
        m.release_year
    FROM movie_stats s
    INNER JOIN movie m ON s.movie_id = m.movie_id
    WHERE 
        s.vote_count >= 50 
        AND s.avg_rating >= 4.0
    ORDER BY s.avg_rating DESC, s.vote_count DESC
    LIMIT %s
    """
    
    close_conn = False
    if cursor is None:
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        close_conn = True
    
    try:
        cursor.execute(sql, (top_k,))
        return [
            {
                "movie_id": r[0], 
                "movie_name": r[1], 
                "release_year": r[2], 
                "score": 0.0  # 兜底推荐无预测分，保持接口一致
            }
            for r in cursor.fetchall()
        ]
    finally:
        if close_conn:
            conn.close()

def recommend_by_user_id(user_id: int, top_k=10, min_sim=0.01, recent_ratings_limit=None):
    print(f"🔍 开始为用户 {user_id} 生成推荐...")
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cur:
            # 1. 拉取用户评分（少量数据，可接受）
            print(f"📥 查询用户 {user_id} 的评分记录...")
            if recent_ratings_limit:
                # 假设user_judge表中有timestamp字段记录评分时间
                cur.execute("""
                    SELECT movie_id, rating 
                    FROM user_judge 
                    WHERE user_id = %s 
                    ORDER BY timestamp DESC 
                    LIMIT %s
                """, (user_id, recent_ratings_limit))
            else:
                # 查询所有评分记录
                cur.execute("SELECT movie_id, rating FROM user_judge WHERE user_id = %s", (user_id,))
            rated = {mid: float(rating) for mid, rating in cur.fetchall()}  # 转换为float
            print(f"✅ 用户 {user_id} 共有 {len(rated)} 条评分记录")
            
            if not rated:
                print(f"⚠️ 用户 {user_id} 没有任何评分记录")
                return get_popular_movies(conn, top_k)  # 冷启动
                raise ValueError("User has not rated any movies.")
            
            # 2. 对每个已评分电影，查其相似电影
            print(f"🔄 开始计算推荐候选电影...")
            candidates = defaultdict(float)
            processed_movies = 0
            for mid, rating in rated.items():
                cur.execute("""
                    SELECT similar_movie_id, similarity 
                    FROM item_similarities 
                    WHERE movie_id = %s AND similarity > %s
                """, (mid, min_sim))
                similar_movies = cur.fetchall()
                print(f"  电影 {mid} (评分: {rating}) 找到 {len(similar_movies)} 部相似电影")
                
                for sim_mid, sim in similar_movies:
                    if sim_mid not in rated:  # 排除已看
                        candidates[sim_mid] += rating * float(sim)  # 转换sim为float
                
                processed_movies += 1
                if processed_movies % 10 == 0:
                    print(f"  已处理 {processed_movies}/{len(rated)} 部已评分电影")
            
            print(f"✅ 候选电影计算完成，共 {len(candidates)} 部候选电影")
            
            # 3. 排序取 top-k
            top_candidates = sorted(candidates.items(), key=lambda x: -x[1])[:top_k]
            print(f"🏆 筛选出 top {len(top_candidates)} 部推荐电影")
            
            # 4. 查电影信息
            if not top_candidates:
                print(f"⚠️ 未找到任何推荐电影")
                return get_popular_movies(conn, top_k)
                raise ValueError("No recommended movies found.")
            
            movie_ids = [mid for mid, _ in top_candidates]
            print(f"📽️ 查询 {len(movie_ids)} 部电影的详细信息...")
            cur.execute("SELECT movie_id, movie_name, release_year FROM movie WHERE movie_id IN %s", (tuple(movie_ids),))
            movie_info = {row[0]: row for row in cur.fetchall()}
            print(f"✅ 成功获取 {len(movie_info)} 部电影的详细信息")
            
            result = [
                {
                    "movie_id": mid,
                    "movie_name": movie_info[mid][1],
                    "release_year": movie_info[mid][2],
                    "score": round(score, 4)
                }
                for mid, score in top_candidates if mid in movie_info
            ]
            
            print(f"🎉 推荐生成完成，返回 {len(result)} 部电影")
            return result
    finally:
        conn.close()
        print("🔒 数据库连接已关闭")

def main():
    print(recommend_by_user_id(user_id=114514, top_k=10, min_sim=0.01, recent_ratings_limit=10))

if __name__ == "__main__":
    main()
    