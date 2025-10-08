import pandas as pd


def clean_csv_files_specific(file1_path, file2_path, output1_path, output2_path,
                              id_column = 'id', check_columns1=None, check_columns2=None):
    """
    清洗两个CSV文件，可以指定要检查的列

    参数:
    file1_path: 第一个CSV文件路径
    file2_path: 第二个CSV文件路径
    output1_path: 第一个输出文件路径
    output2_path: 第二个输出文件路径
    id_column: ID列名
    check_columns1: 文件1中要检查的列列表，None表示检查所有列
    check_columns2: 文件2中要检查的列列表，None表示检查所有列
    """

    # 读取CSV文件
    df1 = pd.read_csv(file1_path, encoding='utf-8', encoding_errors = 'ignore')
    df2 = pd.read_csv(file2_path, encoding='utf-8', encoding_errors = 'ignore')

    print(f"原始数据 - 文件1: {len(df1)} 行, 文件2: {len(df2)} 行")

    # 如果没有指定检查列，则检查所有列（除了ID列）
    if check_columns1 is None:
        check_columns1 = [col for col in df1.columns if col != id_column]
    if check_columns2 is None:
        check_columns2 = [col for col in df2.columns if col != id_column]
    print(check_columns1)
    # 根据ID列合并
    merged_df = pd.merge(df1, df2, on=id_column, how='inner', suffixes=('_1', '_2'))

    print(f"根据ID合并后: {len(merged_df)} 行")

    # 检查指定列是否有空缺值
    mask1 = merged_df[[f"{col}_1" for col in check_columns1]].isnull().any(axis=1)
    mask2 = merged_df[[f"{col}_2" for col in check_columns2]].isnull().any(axis=1)

    # 找出在两个文件中指定列都完整的行
    complete_rows = ~(mask1 | mask2)
    complete_ids = merged_df.loc[complete_rows, id_column]

    print(f"完整数据行: {len(complete_ids)} 行")

    # 筛选数据
    cleaned_df1 = df1[df1[id_column].isin(complete_ids)]
    cleaned_df2 = df2[df2[id_column].isin(complete_ids)]

    # 保存结果
    cleaned_df1.to_csv(output1_path, index=False)
    cleaned_df2.to_csv(output2_path, index=False)

    print(f"清洗完成 - 文件1: {len(cleaned_df1)} 行, 文件2: {len(cleaned_df2)} 行")

    return cleaned_df1, cleaned_df2


# 使用示例
if __name__ == "__main__":
    file1 = "movies.csv"
    file2 = "credits.csv"
    output1 = "cleaned_file1.csv"
    output2 = "cleaned_file2.csv"

    # 可以指定要检查的特定列
    # df1_clean, df2_clean = clean_csv_files_specific(
    #     file1, file2, output1, output2,
    #     check_columns1=['age', 'name'],  # 只检查文件1中的age和name列
    #     check_columns2=['score', 'grade']  # 只检查文件2中的score和grade列
    # )

    df1_clean, df2_clean = clean_csv_files_specific(file1, file2, output1, output2)
