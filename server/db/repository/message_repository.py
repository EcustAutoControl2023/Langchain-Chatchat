from itertools import groupby
from server.db.session import with_session
from typing import Dict, List
import uuid
import datetime
from server.db.models.message_model import MessageModel



@with_session
def add_message_to_db(session, conversation_id: str, chat_type, query, user_id, response="", message_id=None,
                      metadata: Dict = {}):
    """
    新增聊天记录
    """
    if not message_id:
        message_id = uuid.uuid4().hex
    m = MessageModel(id=message_id, user_id=user_id, chat_type=chat_type, query=query, response=response,
                     conversation_id=conversation_id,
                     meta_data=metadata)
    session.add(m)
    session.commit()
    return m.id

@with_session
def delete_message_from_db(session, conversation_id: str, user_id: str):
    """
    新增聊天记录
    """
    m = session.query(MessageModel).filter_by(conversation_id=conversation_id, user_id=user_id).all()
    if m:
        for i in m:
            session.delete(i)
        session.commit()
        return m[0].conversation_id

    return None


@with_session
def update_message(session, message_id, response: str = None, metadata: Dict = None):
    """
    更新已有的聊天记录
    """
    m = get_message_by_id(message_id)
    if m is not None:
        if response is not None:
            m.response = response
        if isinstance(metadata, dict):
            m.meta_data = metadata
        session.add(m)
        session.commit()
        return m.id


@with_session
def get_message_by_id(session, message_id) -> MessageModel:
    """
    查询聊天记录
    """
    m = session.query(MessageModel).filter_by(id=message_id).first()
    return m

@with_session
def get_message_by_user_id(session, user_id):
    """
    查询聊天记录
    """
    m = session.query(MessageModel).filter_by(user_id=user_id).all()

    # 根据m中的conversation_id将m分组
    m = sorted(m, key=lambda x: x.conversation_id)
    m = [list(g) for k, g in groupby(m, key=lambda x: x.conversation_id)]
    m = sorted(m, key=lambda x: x[0].create_time, reverse=True)

    mm = {
        "cur_chat_name": "新的对话",
        "session_key": "chat_history",
        "user_avatar": "user",
        "assistant_avatar": "img/chatchat_icon_blue_square_v2.png",
        "greetings": [],
        "histories": {
            # historys[0].query + '\n' + str(historys[0].create_time ): [({
            # 加8小时
            historys[0].query + '\n' + str(historys[0].create_time + datetime.timedelta(hours=8)): [({
                "role": "user",
                "conversation_id": history.conversation_id,
                "elements": [
                    {
                        "content": history.query,
                        "output_method": "markdown",
                        "title": "",
                        "in_expander": False,
                        "expanded": False,
                        "state": "running",
                        "metadata": {},
                        "kwargs": {
                          "unsafe_allow_html": True
                        }
                    }
                ],
                "metadata": history.meta_data,
            },
            {
                "role": "assistant",
                "conversation_id": history.conversation_id,
                "elements": [
                    {
                        "content": history.response,
                        "output_method": "markdown",
                        "title": "",
                        "in_expander": False,
                        "expanded": False,
                        "state": "running",
                        "metadata": {},
                        "kwargs": {
                          "unsafe_allow_html": True
                        }
                    }
                ],
                "metadata": history.meta_data,
            }) for history in historys]
        for historys in m}
    }

    # 把{"key": [({}, {}), ({})]}转换为[{"key": [{}, {}, {}]}]
    for k, v in mm["histories"].items():
        mm["histories"][k] = [item for sublist in v for item in sublist]

    return mm

@with_session
def feedback_message_to_db(session, message_id, feedback_score, feedback_reason):
    """
    反馈聊天记录
    """
    m = session.query(MessageModel).filter_by(id=message_id).first()
    if m:
        m.feedback_score = feedback_score
        m.feedback_reason = feedback_reason
    session.commit()
    return m.id


@with_session
def filter_message(session, conversation_id: str, limit: int = 10):
    messages = (session.query(MessageModel).filter_by(conversation_id=conversation_id).
                # 用户最新的query 也会插入到db，忽略这个message record
                filter(MessageModel.response != '').
                # 返回最近的limit 条记录
                order_by(MessageModel.create_time.desc()).limit(limit).all())
    # 直接返回 List[MessageModel] 报错
    data = []
    for m in messages:
        data.append({"query": m.query, "response": m.response})
    return data
