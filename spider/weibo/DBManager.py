from sqlalchemy import \
    Column, Integer, String, Text, DateTime, create_engine, MetaData, Table, text, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
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
    __tablename__ = 'topic'

    mid = Column(Integer, primary_key=True)
    word = Column(String(32, 'utf8mb4_0900_ai_ci'), nullable=False)
    summary = Column(Text(collation='utf8mb4_0900_ai_ci'))
    read = Column(Integer)
    mention = Column(Integer)
    href = Column(Text(collation='utf8mb4_0900_ai_ci'))
    timeStamp = Column(DateTime)
    link = Column(Text)


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
    __tablename__ = 'hotSearch'

    mid = Column(Integer, primary_key=True)
    word = Column(String(32, 'utf8mb4_0900_ai_ci'), nullable=False)
    hot = Column(Integer)
    href = Column(Text(collation='utf8mb4_0900_ai_ci'))
    timeStamp = Column(DateTime)


    def __repr__(self):
        return f"word={self.word}, hot={self.hot}, href={self.href}, timeStamp={self.timeStamp}"

    def __init__(self, word, hot=0, href="", timeStamp=datetime.utcnow()):
        self.word = word
        self.hot = hot
        self.href = href
        self.timeStamp = timeStamp


class SearchTrend(Base):
    __tablename__ = 'searchTrend'

    word = Column(String(32), primary_key=True)
    href = Column(Text)
    trend = Column(Text)
    timeStamp = Column(DateTime)

    def __repr__(self):
        return f"word={self.word}, href={self.href}, trend={self.trend}, timeStamp={self.timeStamp}"

    def __init__(self, word, href="", trend="", timeStamp=datetime.utcnow()):
        self.word = word
        self.href = href
        self.trend = trend
        self.timeStamp = timeStamp


class TopicDetail(Base):
    __tablename__ = 'topicDetail'

    mid = Column(String(16, 'utf8mb4_unicode_ci'), primary_key=True)
    detail_url = Column(String(collation='utf8mb4_unicode_ci'))
    screen_name = Column(String(32, 'utf8mb4_unicode_ci'))
    uid = Column(String(10, 'utf8mb4_unicode_ci'))
    gender = Column(String(5, 'utf8mb4_unicode_ci'), server_default=text("'未知'"))
    profile_url = Column(String(collation='utf8mb4_unicode_ci'))
    followers_count = Column(String(10, 'utf8mb4_unicode_ci'))
    status_province = Column(String(10, 'utf8mb4_unicode_ci'))
    type = Column(String(20, 'utf8mb4_unicode_ci'))
    topic_name = Column(String(32, 'utf8mb4_unicode_ci'))
    attitudes_count = Column(Integer)
    comments_count = Column(Integer)
    reposts_count = Column(Integer)
    text = Column(String(collation='utf8mb4_unicode_ci'))
    timeStamp = Column(DateTime)

    def __repr__(self):
        return f"TopicDetail(mid={self.mid}, " \
               f"detail_url={self.detail_url}, " \
               f"screen_name={self.screen_name}, " \
               f"uid={self.uid})," \
               f"topic_name={self.topic_name}"

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


class Comment(Base):
    __tablename__ = 'comments'

    comment_id = Column(String(16, 'utf8mb4_unicode_ci'), primary_key=True)
    screen_name = Column(String(32, 'utf8mb4_unicode_ci'))
    profile_url = Column(Text(collation='utf8mb4_unicode_ci'))
    gender = Column(String(5))
    source = Column(String(10, 'utf8mb4_unicode_ci'))
    created_at = Column(DateTime)
    text = Column(Text(collation='utf8mb4_unicode_ci'))
    like_count = Column(Integer)
    mid = Column(ForeignKey('topicDetail.mid'), nullable=False, index=True)
    topic_name = Column(String(32))
    topicDetail = relationship('TopicDetail')

    def __repr__(self):
        return f"comment_id: {self.comment_id}, " \
               f"screen_name: {self.screen_name}, " \
               f"created_at: {self.created_at}" \
               f"topic_name: {self.topic_name}"

    def __init__(self, **data):
        self.comment_id = data.get('comment_id')
        self.screen_name = data.get('screen_name')
        self.profile_url = data.get('profile_url')
        self.gender = data.get("gender")
        self.source = data.get('source')
        self.created_at = data.get('created_at')
        self.text = data.get('text')
        self.like_count = data.get('like_count')
        self.mid = data.get('mid')
        self.topic_name = data.get('topic_name')
