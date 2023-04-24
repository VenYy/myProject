from sqlalchemy import Column, Integer, String, Text, DateTime, create_engine, MetaData, Table, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine.reflection import Inspector
from datetime import datetime

Base = declarative_base()


class DBManager:
    def __init__(self):
        # 连接数据库
        self.engine = create_engine("mysql+pymysql://root:0226@127.0.0.1:3306/weibo?charset=utf8")
        self.conn = self.engine.connect()

        # session用于创建程序与数据库之间的会话，所有对象的载入和保存(增删改查)都需要通过session
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.metadata = MetaData()
        self.metadata.reflect(bind=self.engine)

    # 创建表
    def create_all(self):
        Base.metadata.create_all(self.engine)
        self.session.commit()
        self.session.close()

    # 添加数据
    def add_data(self, data):
        try:
            self.session.add(data)
            self.session.commit()
        except Exception as e:
            print("Error when adding data: ", e)
            self.session.rollback()
            raise
        finally:
            self.session.close()

    # 查数据
    def get_data(self, tableName):
        table = Table(tableName, self.metadata, autoload_with=self.engine)
        topics = self.session.query(table).all()
        self.session.close()
        return topics

    # 判断表是否存在
    def has_table(self, tableName):
        inspector = Inspector.from_engine(self.engine)
        if inspector.has_table(tableName):
            return True
        else:
            return False

    # 删除表
    def drop_table(self, tableName):
        if self.has_table(tableName):
            try:
                table = Table(tableName, self.metadata, autoload_with=self.engine)
                # print(table)
                if table is not None:
                    Base.metadata.drop_all(self.engine, [table], checkfirst=True)
                    print("delete %s success" % tableName)
                    self.session.commit()
                    self.session.close()
            except KeyError as e:
                self.session.rollback()
                pass
        else:
            print(f"No table named: {tableName}")

    # 修改表数据
    def update_table(self, tableName, mid, **kwargs):
        try:
            table = Table(tableName, self.metadata, autoload_with=self.engine)
            sql = (table.update()
                   # .c表示获取Table对象的column属性
                   .where(table.c.mid == mid)
                   .values(**kwargs))
            self.session.execute(sql)
            print(f"Update table with values: {kwargs}")
            print(f"Update table: {tableName} success where mid: {mid}")
        except Exception as e:
            print("Error when updating data: ", e)
            self.session.rollback()


# 创建映射(创建表)
# 生成一个SQLORM基类，创建表必须继承

class Topic(Base):
    __tablename__ = "topic"
    mid = Column(Integer, primary_key=True, autoincrement=True)
    word = Column(String(32), nullable=False)
    summary = Column(Text)
    read = Column(Integer, default=0)
    mention = Column(Integer, default=0)
    href = Column(Text)
    link = Column(Text, default="")
    timeStamp = Column(DateTime, default=datetime.utcnow())

    def __repr__(self):
        return f"word={self.word}, summary={self.summary}, read={self.read}, " \
               f"mention={self.mention}, href={self.href}, timeStamp={self.timeStamp}"

    def __init__(self, word, summary=None, read=None, mention=None, href=None, link=None, timeStamp=datetime.utcnow()):
        self.word = word
        self.summary = summary
        self.read = read
        self.mention = mention
        self.href = href
        self.link = link
        self.timeStamp = timeStamp


class HotSearch(Base):
    __tablename__ = "hotSearch"
    mid = Column(Integer, primary_key=True, autoincrement=True)
    word = Column(String(32), nullable=False)
    hot = Column(Integer, default=0)
    href = Column(Text, default="")
    timeStamp = Column(DateTime, default=datetime.utcnow())

    def __repr__(self):
        return f"word={self.word}, hot={self.hot}, href={self.href}, timeStamp={self.timeStamp}"

    def __init__(self, word, hot=0, href="", timeStamp=datetime.utcnow()):
        self.word = word
        self.hot = hot
        self.href = href
        self.timeStamp = timeStamp


class SearchTrend(Base):
    __tablename__ = "searchTrend"
    word = Column(String(32), primary_key=True)
    href = Column(Text, default="")
    trend = Column(Text, default="")
    timeStamp = Column(DateTime, default=datetime.utcnow())

    def __repr__(self):
        return f"word={self.word}, href={self.href}, trend={self.trend}, timeStamp={self.timeStamp}"

    def __init__(self, word, href="", trend="", timeStamp=datetime.utcnow()):
        self.word = word
        self.href = href
        self.trend = trend
        self.timeStamp = timeStamp


class TopicDetail(Base):
    __tablename__ = "topicDetail"
    mid = Column(String(16), primary_key=True, unique=True)
    detail_url = Column(Text, default="")
    screen_name = Column(String(32), default="")
    uid = Column(String(10), default="")
    gender = Column(String(5), default="未知")
    profile_url = Column(Text, default="")
    followers_count = Column(String(10), default="")
    status_province = Column(String(10), default="")
    type = Column(String(20), default="")
    topic_name = Column(String(32), default="")
    attitudes_count = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    reposts_count = Column(Integer, default=0)
    text = Column(Text, default="")
    timeStamp = Column(DateTime, default=datetime.utcnow())

    def __init__(self, mid, detail_url="",
                 screen_name="", uid="", gender="未知", profile_url="",
                 followers_count="", status_province="",
                 type_="", topic_name="",
                 attitudes_count=None, comments_count=None, reposts_count=None,
                 text_="", timeStamp=datetime.utcnow()):
        self.mid = mid
        self.detail_url = detail_url
        self.screen_name = screen_name
        self.uid = uid
        self.gender = gender
        self.profile_url = profile_url
        self.followers_count = followers_count
        self.status_province = status_province
        self.type = type_
        self.topic_name = topic_name
        self.attitudes_count = attitudes_count
        self.comments_count = comments_count
        self.reposts_count = reposts_count
        self.text = text_
        self.timeStamp = timeStamp


class Comments(Base):
    __tablename__ = "comments"
    comment_id = Column(String(16), primary_key=True)
    screen_name = Column(String(32), default=None)
    profile_url = Column(Text, default=None)
    source = Column(String(10), default=None)
    follow_count = Column(String(10), default=None)
    followers_count = Column(String(10), default=None)
    created_at = Column(DateTime, default=datetime.utcnow())
    text = Column(Text, default=None)
    mid = Column(String(16), default=None)

    def __init__(self, comment_id, screen_name=None, profile_url=None, source=None,
                 follow_count=None, followers_count=None,
                 created_at=None, text_=None, mid=None):
        self.comment_id = comment_id
        self.screen_name = screen_name
        self.profile_url = profile_url
        self.source = source
        self.follow_count = follow_count
        self.followers_count = followers_count
        self.created_at = created_at
        self.text = text_
        self.mid = mid
