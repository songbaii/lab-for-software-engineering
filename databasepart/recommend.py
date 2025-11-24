import pymysql
from collections import defaultdict
from config import DB_CONFIG
import random

def get_popular_movies(conn, top_k: int, cursor=None, random_factor=0.3):
    # ✅ 使用 movie_stats 汇总表，不再碰 user_judge 大表！
    # 增加随机性：先获取更多电影，然后随机选择
    fetch_count = int(top_k * (1 + random_factor))  # 多获取30%的电影用于随机选择
    
    sql = """
    SELECT 
        m.movie_id,
        m.movie_name,
        m.release_year,
        s.avg_rating,
        s.vote_count
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
        cursor.execute(sql, (fetch_count,))
        movies = [
            {
                "movie_id": r[0], 
                "movie_name": r[1], 
                "release_year": r[2], 
                "avg_rating": float(r[3]),
                "vote_count": int(r[4]),
                "score": 0.0  # 兜底推荐无预测分，保持接口一致
            }
            for r in cursor.fetchall()
        ]
        
        # 增加随机性：对获取的电影进行随机排序
        if movies:
            # 使用加权随机：评分高和投票数多的电影有更高概率被选中
            weights = [movie["avg_rating"] * 0.7 + (movie["vote_count"] / max(movie["vote_count"] for movie in movies)) * 0.3 
                      for movie in movies]
            
            # 如果需要的数量小于获取的数量，则进行随机选择
            if len(movies) > top_k:
                selected_movies = random.choices(movies, weights=weights, k=top_k)
                return selected_movies
            else:
                # 如果数量不足，直接随机打乱顺序
                random.shuffle(movies)
                return movies[:top_k]
        else:
            return []
    finally:
        if close_conn:
            conn.close()

"""
    获取用户推荐
    :param user_id: 用户ID
    :param top_k: 推荐数量
    :param min_sim: 最小相似度阈值
    :param recent_ratings_limit: 取最近多少条评分记录
    :param random_factor: 随机因子，0表示不随机，1表示完全随机
    :return: 推荐结果列表
"""
def recommend_by_user_id(user_id: int, top_k=10, min_sim=0.01, recent_ratings_limit=None, random_factor=0.2):
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
                return get_popular_movies(conn, top_k, cur, random_factor)  # 冷启动
                # raise ValueError("User has not rated any movies.")
            
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
            
            # 3. 计算个性化推荐和热门推荐的数量
            personalized_count = int(top_k * 3 / 4)
            popular_count = top_k - personalized_count
            
            # 4. 获取个性化推荐（增加随机性）
            all_candidates = sorted(candidates.items(), key=lambda x: -x[1])
            
            # 增加随机性：从top候选中随机选择
            if all_candidates:
                # 获取更多候选电影用于随机选择
                fetch_count = min(int(personalized_count * (1 + random_factor)), len(all_candidates))
                candidate_subset = all_candidates[:fetch_count]
                
                # 随机选择指定数量的电影
                if len(candidate_subset) > personalized_count:
                    # 使用加权随机选择（分数越高的电影被选中的概率越大）
                    weights = [score for _, score in candidate_subset]
                    selected_indices = random.choices(
                        range(len(candidate_subset)), 
                        weights=weights, 
                        k=personalized_count
                    )
                    # 修复重复项问题：使用集合确保不重复选择相同的索引
                    unique_indices = list(set(selected_indices))
                    
                    # 如果去重后数量不足，需要补充
                    while len(unique_indices) < personalized_count and len(candidate_subset) > len(unique_indices):
                        # 从未选择的索引中随机选择补充
                        remaining_indices = set(range(len(candidate_subset))) - set(unique_indices)
                        if remaining_indices:
                            additional_index = random.choice(list(remaining_indices))
                            unique_indices.append(additional_index)
                    
                    top_candidates = [candidate_subset[i] for i in unique_indices]
                else:
                    # 如果数量不足，直接随机打乱
                    random.shuffle(candidate_subset)
                    top_candidates = candidate_subset[:personalized_count]
            else:
                top_candidates = []
                
            print(f"🏆 筛选出 {len(top_candidates)} 部个性化推荐电影")
            
            # 5. 获取热门推荐（已增加随机性）
            popular_movies = get_popular_movies(conn, popular_count, cur, random_factor) if popular_count > 0 else []
            print(f"🔥 获取 {len(popular_movies)} 部热门推荐电影")
            
            # 6. 查个性化推荐电影信息（包括avg_rating和vote_count）
            if top_candidates:
                movie_ids = [mid for mid, _ in top_candidates]
                print(f"📽️ 查询 {len(movie_ids)} 部个性化推荐电影的详细信息...")
                # 添加调试信息，检查movie_ids中是否有重复
                unique_movie_ids = set(movie_ids)
                if len(movie_ids) != len(unique_movie_ids):
                    print(f"⚠️ 注意：movie_ids中有重复项，原始数量: {len(movie_ids)}, 去重后数量: {len(unique_movie_ids)}")
                
                # 修改查询语句，同时获取movie_stats中的avg_rating和vote_count
                cur.execute("""
                    SELECT 
                        m.movie_id,
                        m.movie_name,
                        m.release_year,
                        COALESCE(s.avg_rating, 0.0) as avg_rating,
                        COALESCE(s.vote_count, 0) as vote_count
                    FROM movie m
                    LEFT JOIN movie_stats s ON m.movie_id = s.movie_id
                    WHERE m.movie_id IN %s
                """, (tuple(unique_movie_ids),))  # 使用去重后的movie_id
                
                query_results = cur.fetchall()
                print(f"🔍 数据库查询返回 {len(query_results)} 条记录")
                
                # 检查查询结果中是否有重复的movie_id
                result_movie_ids = [row[0] for row in query_results]
                unique_result_ids = set(result_movie_ids)
                if len(result_movie_ids) != len(unique_result_ids):
                    print(f"⚠️ 注意：查询结果中有重复的movie_id，原始数量: {len(result_movie_ids)}, 去重后数量: {len(unique_result_ids)}")
                
                movie_info = {row[0]: row for row in query_results}
                print(f"✅ 成功获取 {len(movie_info)} 部个性化推荐电影的详细信息")
                
                # 添加调试信息，查看哪些movie_id没有找到
                if len(unique_movie_ids) != len(movie_info):
                    missing_ids = unique_movie_ids - set(movie_info.keys())
                    print(f"⚠️ 注意：{len(missing_ids)} 部电影未找到详细信息，缺失的movie_id: {missing_ids}")
                
                personalized_result = [
                    {
                        "movie_id": mid,
                        "movie_name": movie_info[mid][1],
                        "release_year": movie_info[mid][2],
                        "avg_rating": float(movie_info[mid][3]),
                        "vote_count": int(movie_info[mid][4]),
                        "score": round(score, 4)
                    }
                    for mid, score in top_candidates if mid in movie_info
                ]
            else:
                personalized_result = []
            
            # 7. 合并结果（3/4个性化 + 1/4热门），并去除重复
            # 创建一个集合来跟踪已添加的电影ID
            seen_movie_ids = set()
            result = []
            
            # 先添加个性化推荐
            for movie in personalized_result:
                if movie["movie_id"] not in seen_movie_ids:
                    result.append(movie)
                    seen_movie_ids.add(movie["movie_id"])
            
            # 再添加热门推荐，避免重复
            for movie in popular_movies:
                if movie["movie_id"] not in seen_movie_ids:
                    result.append(movie)
                    seen_movie_ids.add(movie["movie_id"])
            
            # 如果结果不足top_k，用热门电影补充（避免重复）
            if len(result) < top_k:
                additional_count = top_k - len(result)
                if additional_count > 0:
                    # 获取更多热门电影进行补充
                    additional_popular = get_popular_movies(conn, additional_count + 10, cur, random_factor)  # 多获取一些用于去重
                    for movie in additional_popular:
                        if movie["movie_id"] not in seen_movie_ids and len(result) < top_k:
                            result.append(movie)
                            seen_movie_ids.add(movie["movie_id"])
            
            # 最终随机打乱结果顺序，增加多样性
            if random_factor > 0:
                random.shuffle(result)
            
            print(f"🎉 推荐生成完成，返回 {len(result)} 部电影 ({len([m for m in personalized_result if m['movie_id'] in seen_movie_ids])} 部个性化 + {len([m for m in popular_movies if m['movie_id'] in seen_movie_ids])} 部热门)")
            return result[:top_k]  # 确保不超过top_k数量
    finally:
        conn.close()
        print("🔒 数据库连接已关闭")

def main():
    print(recommend_by_user_id(user_id=114514, top_k=20, min_sim=0.01, recent_ratings_limit=10, random_factor=0.3))

if __name__ == "__main__":
    main()