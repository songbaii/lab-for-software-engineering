import pandas as pd
import pymysql
import json
import csv

# 数据库连接配置
db_config = {
    'host': 'localhost',
    'user': 'violet',
    'password': 's131601',
    'database': 'soft_ware_engineering',
    'charset': 'utf8mb4'
}


def create_db_connection():
    """创建数据库连接"""
    return pymysql.connect(**db_config)


def safe_json_loads(json_str):
    """安全地解析JSON字符串"""
    if pd.isna(json_str) or json_str == '':
        return []
    try:
        # 处理单引号问题，将单引号替换为双引号
        json_str = json_str.replace("'", "\"")
        return json.loads(json_str)
    except json.JSONDecodeError:
        print(f"JSON解析错误: {json_str}")
        return []


def import_movie_data_from_csv(csv_file_path):
    """从CSV导入电影基本信息"""
    print(f"开始从 {csv_file_path} 导入电影基本信息...")

    # 读取CSV文件
    df = pd.read_csv(csv_file_path, skiprows=0)
    conn = create_db_connection()
    cursor = conn.cursor()
    try:
        # 导入电影表
        for _, row in df.iterrows():
            # 处理可能的空值
            if pd.notna(row['id']) and row['id'] != '':
                id = int(row['id'])
            else:
                break
            if pd.notna(row['title']) and row['title'] != '':
                title = row['title']
            else:
                break
            if pd.notna(row['budget']) and row['budget'] != '':
                budget = int(row['budget'] / 10000)
            else:
                break
            if pd.notna('original_language') and row['original_language'] != '':
                original_language = row['original_language']
            else:
                break
            if pd.notna(row['popularity']) and row['popularity'] != '':
                popularity = int(float(row['popularity']))
            else:
                break
            if pd.notna(row['revenue']) and row['revenue'] != '':
                revenue = int(row['revenue'] / 10000)
            else:
                break
            if pd.notna(row['vote_count']) and row['vote_count'] != '':
                vote_count = int(row['vote_count'])
            else:
                break
            if pd.notna(row['vote_average']) and row['vote_average'] != '':
                vote_average = int(float(row['vote_average']))
            else:
                break
            # 处理日期
            if pd.notna(row['release_date']) and row['release_date'] != '':
                    release_date = pd.to_datetime(row['release_date']).strftime('%Y-%m-%d')
            else:
                break
            if pd.notna(row['overview']) and row['overview'] != '':
                overview = row['overview']
            else:
                break
            movie_data = (
                id,
                title,
                budget,
                original_language,
                popularity,
                release_date,
                revenue,
                vote_count,
                vote_average,
                overview
            )

            insert_movie = """
                           INSERT ignore INTO movie (movie_id, movie_name, budget, original_language,
                                              popularity, release_date, revenue, vote_count,
                                              vote_average, overview)
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) \
                           """
            cursor.execute(insert_movie, movie_data)

        # 导入电影类型
        for _, row in df.iterrows():
            genres = safe_json_loads(row['genres'])
            for genre in genres:
                # 先检查类型是否存在，不存在则插入
                check_genre = "SELECT genre_id FROM genre_table WHERE genre_id = %s"
                cursor.execute(check_genre, (genre['id'],))
                if not cursor.fetchone():
                    insert_genre = "INSERT INTO genre_table (genre_id, genre_name) VALUES (%s, %s)"
                    cursor.execute(insert_genre, (genre['id'], genre['name']))

                # 插入电影类型关系
                insert_movie_genre = """
                                     INSERT IGNORE INTO movie_genre (movie_id, genre_id)
                                     VALUES (%s, %s) \
                                     """
                cursor.execute(insert_movie_genre, (int(row['id']), genre['id']))

        # 导入制作国家
        for _, row in df.iterrows():
            countries = safe_json_loads(row['production_countries'])
            for country in countries:
                # 先检查国家是否存在
                check_country = "SELECT country_short_name FROM country WHERE country_short_name = %s"
                cursor.execute(check_country, (country['iso_3166_1'],))
                if not cursor.fetchone():
                    insert_country = "INSERT INTO country (country_short_name, country_full_name) VALUES (%s, %s)"
                    cursor.execute(insert_country, (country['iso_3166_1'], country['name']))

                # 插入电影国家关系
                insert_movie_country = """
                                       INSERT IGNORE INTO movie_pro_country (movie_id, country_short_name)
                                       VALUES (%s, %s) \
                                       """
                cursor.execute(insert_movie_country, (int(row['id']), country['iso_3166_1']))

        # 导入制作公司
        for _, row in df.iterrows():
            companies = safe_json_loads(row['production_companies'])
            for company in companies:
                # 先检查公司是否存在
                check_company = "SELECT company_id FROM company WHERE company_id = %s"
                cursor.execute(check_company, (company['id'],))
                if not cursor.fetchone():
                    insert_company = "INSERT INTO company (company_id, company_name) VALUES (%s, %s)"
                    cursor.execute(insert_company, (company['id'], company['name']))

                # 插入电影公司关系
                insert_movie_company = """
                                       INSERT IGNORE INTO movie_pro_company (movie_id, company_id)
                                       VALUES (%s, %s) \
                                       """
                cursor.execute(insert_movie_company, (int(row['id']), company['id']))

        conn.commit()
        print("电影基本信息导入完成！")

    except Exception as e:
        conn.rollback()
        print(f"导入电影数据时出错: {e}")
        raise
    finally:
        cursor.close()
        conn.close()


def import_cast_data_from_csv(csv_file_path):
    """从CSV导入演员和工作人员信息"""
    print(f"开始从 {csv_file_path} 导入演员和工作人员信息...")

    # 读取CSV文件
    df = pd.read_csv(csv_file_path)

    conn = create_db_connection()
    cursor = conn.cursor()

    try:
        for _, row in df.iterrows():
            movie_id = int(row['movie_id'])

            # 导入演员信息
            cast_members = safe_json_loads(row['cast'])
            for cast_member in cast_members:
                # 插入人员信息
                check_person = "SELECT person_id FROM person WHERE person_id = %s"
                cursor.execute(check_person, (cast_member['id'],))
                if not cursor.fetchone():
                    insert_person = "INSERT INTO person (person_id, person_name) VALUES (%s, %s)"
                    cursor.execute(insert_person, (cast_member['id'], cast_member['name']))

                # 插入演员关系
                insert_cast = """
                              INSERT IGNORE INTO movie_cast (movie_id, cast_id)
                              VALUES (%s, %s) \
                              """
                cursor.execute(insert_cast, (movie_id, cast_member['id']))

            # 导入工作人员信息
            crew_members = safe_json_loads(row['crew'])
            for crew_member in crew_members:
                # 插入人员信息
                check_person = "SELECT person_id FROM person WHERE person_id = %s"
                cursor.execute(check_person, (crew_member['id'],))
                if not cursor.fetchone():
                    insert_person = "INSERT INTO person (person_id, person_name) VALUES (%s, %s)"
                    cursor.execute(insert_person, (crew_member['id'], crew_member['name']))

        conn.commit()
        print("演员和工作人员信息导入完成！")

    except Exception as e:
        conn.rollback()
        print(f"导入演员数据时出错: {e}")
        raise
    finally:
        cursor.close()
        conn.close()


def check_csv_encoding(file_path):
    """检查CSV文件编码"""
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']

    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                f.read()
            return encoding
        except UnicodeDecodeError:
            continue

    return 'utf-8'  # 默认使用utf-8


def import_with_encoding_check(csv_file_path, import_function):
    """带编码检查的导入函数"""
    encoding = check_csv_encoding(csv_file_path)
    print(f"检测到文件编码: {encoding}")

    # 重新读取文件
    df = pd.read_csv(csv_file_path, encoding=encoding)

    # 保存为UTF-8编码的临时文件
    temp_file = "temp_utf8.csv"
    df.to_csv(temp_file, index=False, encoding='utf-8')

    # 使用临时文件进行导入
    import_function(temp_file)

    # 清理临时文件
    import os
    os.remove(temp_file)


def main():
    """主函数"""
    # 文件路径
    movie_csv_file = "movies.csv"  # 电影基本信息CSV
    cast_csv_file = "credits.csv"  # 演员信息CSV

    # 导入电影基本信息
    import_with_encoding_check(movie_csv_file, import_movie_data_from_csv)

    # 导入演员和工作人员信息
    import_with_encoding_check(cast_csv_file, import_cast_data_from_csv)

    print("所有数据导入完成！")

if __name__ == "__main__":
    main()