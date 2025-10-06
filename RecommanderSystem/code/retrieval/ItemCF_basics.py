# 一个最基础的基于物品的协同过滤的实现

import math
from collections import defaultdict

class ItemCF:
    def __init__(self):
        # 用户-物品评分矩阵 {user_id: {item_id: rating}}
        self.user_item_matrix = {}
        # 物品相似度矩阵 {item_id: {item_id: similarity}}
        self.item_similarity_matrix = {}
        
    def add_user_item_rating(self, user_id, item_id, rating):
        """添加用户对物品的评分"""
        if user_id not in self.user_item_matrix:
            self.user_item_matrix[user_id] = {}
        self.user_item_matrix[user_id][item_id] = rating
    
    def calculate_item_similarity(self):
        """计算物品之间的相似度（基于用户-物品评分矩阵中两列的余弦夹角）"""
        # 获取所有物品ID
        item_ids = set()
        for user_items in self.user_item_matrix.values():
            item_ids.update(user_items.keys())
        item_ids = list(item_ids)
        
        # 计算每对物品之间的余弦相似度
        self.item_similarity_matrix = defaultdict(lambda: defaultdict(float))
        
        for i, item1 in enumerate(item_ids):
            for j, item2 in enumerate(item_ids):
                if i >= j:  # 避免重复计算和自身相似度
                    continue
                    
                # 计算item1和item2的余弦相似度
                similarity = self._cosine_similarity(item1, item2)
                if similarity > 0:
                    self.item_similarity_matrix[item1][item2] = similarity
                    self.item_similarity_matrix[item2][item1] = similarity
    
    def _cosine_similarity(self, item1, item2):
        """计算两个物品之间的余弦相似度"""
        # 获取对两个物品都有评分的用户
        ratings1 = []
        ratings2 = []
        dot_product = 0
        
        for user_id, user_items in self.user_item_matrix.items():
            if item1 in user_items and item2 in user_items:
                dot_product += user_items[item1] * user_items[item2]
            if item1 in user_items:
                ratings1.append(user_items[item1])
            if item2 in user_items:
                ratings2.append(user_items[item2])
        
        # 分母：两个向量的模的乘积
        norm1 = math.sqrt(sum(r * r for r in ratings1))
        norm2 = math.sqrt(sum(r * r for r in ratings2))
        
        # 避免除零错误
        if norm1 == 0 or norm2 == 0:
            return 0.0
            
        return dot_product / (norm1 * norm2)
    
    def get_similar_items(self, item_id, k=10):
        """获取与指定物品最相似的k个物品"""
        if item_id not in self.item_similarity_matrix:
            return []
        
        # 按相似度排序并返回前k个
        similar_items = sorted(self.item_similarity_matrix[item_id].items(), 
                              key=lambda x: x[1], reverse=True)
        return similar_items[:k]
    
    def recommend(self, user_id, k=10, n=100):
        """为用户生成推荐列表
        Args:
            user_id: 用户ID
            k: 推荐物品数量
            n: 每个用户物品考虑的相似物品数量
        Returns:
            推荐物品列表 [(item_id, score)]
        """
        if user_id not in self.user_item_matrix:
            return []
        
        # 获取用户已评分的物品
        user_items = self.user_item_matrix[user_id]
        
        # 计算用户对物品的兴趣分数
        item_scores = defaultdict(float)
        for item, rating in user_items.items():
            # 获取与该物品最相似的n个物品
            similar_items = self.get_similar_items(item, n)
            for similar_item, similarity in similar_items:
                # 如果用户已经评分过该物品，则跳过
                if similar_item in user_items:
                    continue
                # 累加分数：用户评分 * 物品相似度
                item_scores[similar_item] += rating * similarity
        
        # 按分数排序并返回前k个
        recommendations = sorted(item_scores.items(), key=lambda x: x[1], reverse=True)
        return recommendations[:k]

# 使用示例
if __name__ == "__main__":
    # 创建ItemCF实例
    itemcf = ItemCF()
    
    # 添加用户评分数据 (用户ID, 物品ID, 评分)
    # 假设我们有5个用户对5部电影的评分数据
    ratings = [
        (1, 101, 5), (1, 102, 3), (1, 103, 4),
        (2, 101, 4), (2, 102, 2), (2, 104, 5),
        (3, 102, 4), (3, 103, 5), (3, 104, 3),
        (4, 101, 5), (4, 104, 4), (4, 105, 3),
        (5, 103, 4), (5, 104, 5), (5, 105, 2)
    ]
    
    # 添加评分数据到模型
    for user_id, item_id, rating in ratings:
        itemcf.add_user_item_rating(user_id, item_id, rating)
    
    # 计算物品相似度
    itemcf.calculate_item_similarity()
    
    # 查看物品101最相似的物品
    print("与物品101最相似的物品:")
    similar_items = itemcf.get_similar_items(101, 5)
    for item, similarity in similar_items:
        print(f"  物品{item}: 相似度 {similarity:.4f}")
    
    # 为用户1生成推荐
    print("\n为用户1推荐的物品:")
    recommendations = itemcf.recommend(1, 5)
    for item, score in recommendations:
        print(f"  物品{item}: 推荐分数 {score:.4f}")