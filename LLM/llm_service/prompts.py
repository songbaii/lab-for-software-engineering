def generate_movie_review_prompt(movie_title, movie_info):
    """
    生成电影短评的Prompt
    :param movie_title: 电影标题
    :param movie_info: 电影信息（如导演、主演、类型等，从数据库来）
    :return: 构造好的提示词字符串
    """
    prompt = f"""
    你是一个风趣幽默的影评人。请为电影《{movie_title}》写一段100字以内的短评。
    电影信息：{movie_info}。
    要求：突出电影最吸引人的特点，语言简洁明快，带有个人观点，避免剧透。
    """
    return prompt

def generate_movie_summary_prompt(movie_title, movie_info):
    """
    生成电影摘要的Prompt
    :param movie_title: 电影标题
    :param movie_info: 电影信息
    :return: 构造好的提示词字符串
    """
    prompt = f"""
    你是一个专业的电影编辑。请为电影《{movie_title}》写一段80字以内的剧情摘要。
    电影信息：{movie_info}。
    要求：客观中立，概括主要剧情脉络和背景设定，避免透露关键结局。
    """
    return prompt