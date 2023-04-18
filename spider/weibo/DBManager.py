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
                print(table)
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


# 创建映射(创建表)
# 生成一个SQLORM基类，创建表必须继承

class Topic(Base):
    __tablename__ = "topic"
    Id = Column(Integer, primary_key=True, autoincrement=True)
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
    Id = Column(Integer, primary_key=True, autoincrement=True)
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

    def __repr__(self):
        return f"word={self.word}, href={self.href}, trend={self.trend}"

    def __init__(self, word, href="", trend=""):
        self.word = word
        self.href = href
        self.trend = trend
