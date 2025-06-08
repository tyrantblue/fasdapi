import time

import pymysql
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from config import MYSQL_INFO, GENERATION_CONFIG, GOOGLE_API_KEY, SYSTEM_CONTENT
import uuid
from loguru import logger
# def to_markdown(text):
#     import textwrap
#     from IPython.display import display
#     from IPython.display import Markdown
#     text = text.replace('•', '  *')
#     return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


# Used to securely store your API key
# Or use `os.getenv('GOOGLE_API_KEY')` to fetch an environment variable.
# GOOGLE_API_KEY=userdata.get('GOOGLE_API_KEY')

# def init(api_key=GOOGLE_API_KEY):
#     genai.configure(api_key=api_key, transport="rest")
#     genai.GenerationConfig(**GENERATION_CONFIG)
#     return genai.GenerationConfig(**GENERATION_CONFIG)

def get_model_list():
    genai.configure(api_key=GOOGLE_API_KEY, transport="rest")
    for m in genai.list_models():
        print(m.name, m.version)


def msg_insert(msg: list[dict]):
    """
    将信息插入数据库
    :param msg: 字典类型，包含这条信息的信息
    :return:
    """
    db = pymysql.connect(**MYSQL_INFO)
    sql = ("INSERT INTO AI_MSG(`msg_id`, `user_id`, `msg`, `last_msg_id`) "
           "VALUES(%(msg_id)s, %(user_id)s, %(msg)s, %(last_msg_id)s)")

    with db.cursor() as cursor:
        for m in msg:
            cursor.execute(sql, m)
        db.commit()


def get_history_messages(last_msg_id: str | None = None, max_level: int = 100) -> list[dict]:
    """
    从指定的消息处开始查找历史消息
    :param last_msg_id: 上一条消息id
    :param max_level: 最大历史记录
    :return:
    """
    db = pymysql.connect(**MYSQL_INFO)
    sql = """
            WITH RECURSIVE conversation AS (
            -- 基础查询：从指定的msg_id开始
            SELECT msg_id, user_id, msg, last_msg_id, create_time, 1 AS level
            FROM ai_msg
            WHERE msg_id = %s  -- 替换为你要查询的msg_id
            
            UNION ALL
            
            -- 递归部分：连接上一句话（注意这里是a.msg_id = c.last_msg_id）
            SELECT a.msg_id, a.user_id, a.msg, a.last_msg_id, a.create_time, c.level + 1
            FROM ai_msg a
            JOIN conversation c ON a.msg_id = c.last_msg_id  -- 关键变化在这里
            WHERE c.level < %s 
        )
        SELECT msg_id, user_id, msg, create_time, level
        FROM conversation
        ORDER BY level DESC; 
        """
    with db.cursor() as cursor:
        cursor.execute(sql, (last_msg_id, max_level, ))
        result = cursor.fetchall()

    if not result or len(result) == 0:
        return []

    return [{'role': "user" if 'user' in r[0] else "model", 'parts': [r[2]]} for r in result]


def get_ai_result(model_id: str, user_id: str,
                  user_msg: str, user_msg_id: str,
                  last_msg_id: str | None = None, card: str = '') -> str:
    """
    获取ai返回数据并插入数据库
    :param card:
    :param model_id:
    :param user_id:
    :param user_msg:
    :param user_msg_id:
    :param last_msg_id:
    :return:
    """

    # 配置ai
    genai.configure(api_key=GOOGLE_API_KEY, transport="rest")
    model = genai.GenerativeModel(model_name=model_id, system_instruction=SYSTEM_CONTENT+card)
    # 设置提示词获取ai历史对话记录
    messages = []
    messages.extend(get_history_messages(last_msg_id))
    messages.append({'role': 'user', 'parts': [user_msg]})
    logger.info(messages)

    # 请求对话
    response = model.generate_content(
        contents=messages,
        stream=False,
        generation_config=genai.GenerationConfig(**GENERATION_CONFIG),
        # 其他选项: BLOCK_MEDIUM_AND_ABOVE, BLOCK_LOW_AND_ABOVE, BLOCK_NONE (非常不推荐)
        safety_settings={
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }
        )
    # if not response.candidates:
    #     logger.error(response)
    #     return "error"

    ai_msg = ''
    ai_msg = response.text
    print(ai_msg)

    # 输出对话
    # for chunk in response:
    #     if chunk.text.strip() == '':
    #         continue
    #     print(chunk.text)
    #     ai_msg += chunk.text

    # 将本轮对话插入数据库
    user_msg_dict = {
        "msg_id": user_msg_id,
        "user_id": f'user_{user_id}',
        "msg": user_msg,
        "last_msg_id": last_msg_id,
    }

    model_msg_dict = {
        "msg_id": str(uuid.uuid4()),
        "user_id": f'model_{model_id}',
        "msg": ai_msg,
        "last_msg_id": user_msg_id,
    }
    msg_insert([user_msg_dict, model_msg_dict])
    logger.info(f"此回复的msg_id为: {model_msg_dict['msg_id']}")
    return model_msg_dict['msg_id']


def send_msg():
    from config import test_card02
    # gemini-2.0-flash, gemini-2.0-flash-exp, models/gemini-2.5-pro-exp-03-25
    model_id = 'models/gemini-2.5-pro-exp-03-25'
    send = """
    我看看，先召唤这个：战场原黒仪！这大长腿真的无敌了！
    """
    last_msg_id = "319e51f1-407a-4bce-a581-6914d5cf4dcc"

    while True:
        time.sleep(0.5)
        send = input("请输入: ")
        last_msg_id = get_ai_result(model_id=model_id, user_id='test',
                                    user_msg=send, user_msg_id=str(uuid.uuid4()),
                                    last_msg_id=last_msg_id, card=test_card02)


def main():
    send_msg()


if __name__ == '__main__':
    from config import nov_01
    model_id = 'gemini-2.0-flash'
    last_msg_id = "start_like"
    get_ai_result(model_id=model_id, user_id='test',
                  user_msg=nov_01, user_msg_id=str(uuid.uuid4()),
                  last_msg_id=last_msg_id, card="")
    # main()
    # get_model_list()
