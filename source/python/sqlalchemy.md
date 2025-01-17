---
date: 2025-01-17 15:57
---

# SQLAlchemy Tips

## 公式ドキュメント

[SQLAlchemy \- The Database Toolkit for Python](https://www.sqlalchemy.org/)

## Tips

### 宣言ベースでのテーブル定義

SQLAlchemy 2.0からは、宣言ベースでのテーブル定義が推奨されている。

```python
from datetime import datetime
from typing import List
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase


# declarative base class
class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"

    id = mapped_column(Integer, primary_key=True)
    name: Mapped[str]
    fullname: Mapped[Optional[str]]
    nickname: Mapped[Optional[str]] = mapped_column(String(64))
    create_date: Mapped[datetime] = mapped_column(insert_default=func.now())

    addresses: Mapped[List["Address"]] = relationship(back_populates="user")


class Address(Base):
    __tablename__ = "address"

    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(ForeignKey("user.id"))
    email_address: Mapped[str]

    user: Mapped["User"] = relationship(back_populates="addresses")
```

参考: [Declarative Mapping Styles — SQLAlchemy 2\.0 Documentation](https://docs.sqlalchemy.org/en/20/orm/declarative_styles.html)

Mapped[]はテーブルのカラムのPythonの型とSQLAlchemyの型をマッピングするためのクラスです。

mapped_column()は、具体的にSQLでのテーブル定義を行う関数です。インデックスの有無指定や、デフォルト値の指定などができます。

カラムの定義に関しては以下も参考にしてください。

参考: [Table Configuration with Declarative — SQLAlchemy 2\.0 Documentation](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#using-annotated-declarative-table-type-annotated-forms-for-mapped-column)
