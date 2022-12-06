from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, Text, Enum, DateTime
from sqlalchemy.orm import relationship, backref
from app import db, app
from enum import Enum as UserEnum
from flask_login import UserMixin
from datetime import datetime


class UserRole(UserEnum):
    USER = 1
    ADMIN = 2


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class Category(BaseModel):
    __tablename__ = 'category'

    name = Column(String(50), nullable=False)
    products = relationship('Product', backref='category', lazy=False)

    def __str__(self):
        return self.name


prod_tag = db.Table('prod_tag',
                    Column('product_id', Integer,
                           ForeignKey('product.id'), nullable=False, primary_key=True),
                    Column('tag', Integer,
                           ForeignKey('tag.id'), nullable=False, primary_key=True))


# class Product(BaseModel):
#     name = Column(String(50), nullable=False)
#     # author = Column(String(50), nullable=False)
#     description = Column(Text)
#     price = Column(Float, default=0)
#     image = Column(String(100))
#     active = Column(Boolean, default=True)
#     category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
#     tags = relationship('Tag', secondary='prod_tag', lazy='subquery',
#                         backref=backref('products', lazy=True))
#     receipt_details = relationship('ReceiptDetails', backref='product', lazy=True)
#
#     def __str__(self):
#         return self.name
class Product(BaseModel):
    name = Column(String(50), nullable=False)
    author = Column(String(50), nullable=False)
    description = Column(Text)
    price = Column(Float, default=0)
    image = Column(String(100))
    active = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    tags = relationship('Tag', secondary='prod_tag', lazy='subquery',
                        backref=backref('products', lazy=True))
    receipt_details = relationship('ReceiptDetails', backref='product', lazy=True)

    def __str__(self):
        return self.name

class Tag(BaseModel):
    name = Column(String(50), nullable=False, unique=True)

    def __str__(self):
        return self.name


class User(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100), nullable=False)
    active = Column(Boolean, default=True)
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    receipts = relationship('Receipt', backref='user', lazy=True)

    def __str__(self):
        return self.name


class Receipt(BaseModel):
    created_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    details = relationship('ReceiptDetails', backref='receipt', lazy=True)


class ReceiptDetails(BaseModel):
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        db.session.commit()
        # c1 = Category(name='Điện thoại')
        # c2 = Category(name='Máy tính bảng')
        # c3 = Category(name='Phụ kiện')
        #
        # db.session.add_all([c1, c2, c3])
        # db.session.commit()

        # p1 = Product(name='Tin Vào Chính Mình', description='I Can Do It – Tin Vào Chính Mình – Sức Mạnh Của Sự Tự Khẳng Định', price=87000,
        #              image='https://nhasachmienphi.com/images/thumbnail/nhasachmienphi-tin-vao-chinh-minh.jpg',
        #              category_id=2)
        # p2 = Product(name='Tin Vào Chính Mình',description='Đừng Bao Giờ Đi Ăn Một Mình được viết với lời văn giản dị và chân thực', price=145000,
        #              image='https://nhasachmienphi.com/images/thumbnail/nhasachmienphi-dung-bao-gio-di-an-mot-minh.jpg',
        #              category_id=2)
        # p3 = Product(name='Đấm Phát Chết Luôn', description='Sức mạnh tuyệt đối của saitama sau khi nỗ lực tập luyện ', price=360000,
        #              image='https://nhasachmienphi.com/images/thumbnail/nhasachmienphi-dam-phat-chet-luon.jpg',
        #              category_id=3)
        # p4 = Product(name='Cạm Bẫy Của Nữ Thần', description='Một tác phẩm đến từ tác giả Câu Lạc Bộ Ngoại Tình – Kha Tiểu. ', price=100000,
        #              image='https://nhasachmienphi.com/images/thumbnail/nhasachmienphi-cam-bay-cua-nu-than.jpg',
        #              category_id=3)
        # p5 = Product(name='Thất Hình Đại Tội', description='“Thất đại ác nhân”, một nhóm chiến binh có tham vọng lật đổ vương quốc Britannia, được cho là đã bị tiêu diệt bởi các “hiệp sĩ thánh chiến” mặc dù vẫn còn 1 số người cho rằng họ vẫn còn sống. 10 năm sau, Các hiệp sĩ thánh chiến đã làm 1 cuộc đảo chính và khống chế đức vua, họ trở thành người cai trị độc tài mới của vương quốc. Elizabeth, con gái duy nhất của nhà vua, đã lên đường tìm “thất đại ác nhân” để nhờ họ tái chiếm lại vương quốc. Công chúa có thành công trong việc tìm kiếm “thất đại ác nhân”, các “hiệp sĩ thánh chiến” sẽ làm gì để ngăn chăn cô? xem các chap truyện sau sẽ rõ.', price=15000,
        #              image='https://nhasachmienphi.com/images/thumbnail/nhasachmienphi-nanatsu-no-taizai-that-hinh-dai-toi.jpg',
        #              category_id=3)
        #
        # # db.session.add(p1)
        # # db.session.add(p2)
        # # db.session.add(p3)
        # # db.session.add(p4)
        # db.session.add(p5)
        #
        # db.session.commit()

        # import hashlib
        # password = str(hashlib.md5('123456'.encode('utf-8')).hexdigest())
        # u = User(name='Quản trị viên', username='admin',
        #          password=password,
        #          user_role=UserRole.ADMIN,
        #          avatar='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg')
        # db.session.add(u)
        # db.session.commit()

