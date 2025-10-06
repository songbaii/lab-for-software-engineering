# 接口定义

目前的ItemCF类实现了一个最基础的基于物品的协同过滤算法，其维护两个索引：用户-物品评分矩阵 user_item_matrix 和物品相似度矩阵 item_similarity_matrix。

接口：

```python
def recommend(self, user_id, k=10, n=100):
        """为用户生成推荐列表
        Args:
            user_id: 用户ID
            k: 推荐物品数量
            n: 每个用户物品考虑的相似物品数量
        Returns:
            推荐物品列表 [(item_id, score)]
        """
```
