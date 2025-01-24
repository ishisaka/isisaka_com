---
date: 2025-01-24 23:00
---

# SQLAlchemy Tips

## SQLAlchemyとは

SQLAlchemyはPythonで使用されるオープンソースのSQLツールキットおよびオブジェクトリレーショナルマッピング（ORM）ライブラリです。データベース操作を効率化し、オブジェクト指向プログラミングとリレーショナルデータベースを橋渡しする役割を果たします。2006年にリリースされ、現在も広く利用されています [^2] [^9] [^16]。

### 主な特徴

- **ORM（Object Relational Mapping）**  
  SQLAlchemyは、テーブルとPythonクラスを1対1で対応させ、SQL文を直接記述することなくデータベースを操作できます。これにより、開発者はPythonのオブジェクト指向的な方法でデータベース操作が可能になります [^6] [^16] [^20]。

- **柔軟性と拡張性**  
  MySQL、PostgreSQL、SQLite、Oracleなど、多くのデータベースエンジンに対応しており、異なるデータベース間の違いを吸収する抽象化レイヤーを提供します。また、開発段階ではSQLite、本番環境ではMySQLやPostgreSQLなどに切り替えることも容易です [^13] [^16].

- **データマッパーパターン**  
  SQLAlchemyはデータマッパーパターンを採用し、高度なクエリやトランザクションの管理も可能です。他のORMライブラリが採用するアクティブレコードパターンよりも柔軟性が高い設計です [^9] [^7].

### 利点

1. **SQL不要**  
   SQL文を書く必要がなく、Pythonコードのみでデータベース操作が可能です [^16] [^20]。

2. **スケーラビリティ**  
   大規模で複雑なデータモデルやクエリに対応可能で、スケーラブルなアプリケーション開発に適しています [^3] [^16]。

3. **簡単なスキーマ変更**  
   Alembicツールを使用することで、コードからスキーマの変更やマイグレーションが容易に行えます [^2] [^3]。

4. **テスト環境への適応性**  
   テスト時にはシンプルなSQLiteを利用し、本番環境では堅牢なデータベースに切り替えるなど柔軟な運用が可能です [^13].

### 注意点

- **学習コスト**: 柔軟性が高い分、学習コストが他のORMライブラリよりも高めです。しかし公式ドキュメントやチュートリアルが充実しているため、初心者でも学びやすい環境が整っています [^2] [^16].
- **N+1問題**: ORM全般に共通する課題ですが、大量の関連データを扱う際には注意が必要です。適切なローディング戦略（eager loadingやlazy loading）を選択することで回避できます [^10].

### 適用例

- 大規模アプリケーション開発（例: Yelp, Reddit, Dropboxなどで利用実績あり）
- リレーショナルデータベースを使用するWebアプリケーション
- データ分析やETL処理のバックエンド構築 [^2] [^9].

SQLAlchemyはその柔軟性と強力な機能から、多様なプロジェクトで活用されています。Pythonプログラマーにとって非常に有用なツールと言えるでしょう。

Citations:
[^2]: <https://www.jssrv.co.jp/sqlalchemy%E3%81%A8%E3%81%AF%E4%BD%95%E3%81%A7%E3%81%99%E3%81%8B%E3%80%82sqlalchemy%E3%81%AE%E5%88%A9%E7%82%B9%E3%81%A8%E3%81%AF%E4%BD%95%E3%81%A7%E3%81%99%E3%81%8B%E3%80%82/>
[^3]: <https://qiita.com/Tadataka_Takahashi/items/f212c34971dca7845aec>
[^6]: <https://qiita.com/arkuchy/items/75799665acd09520bed2>
[^7]: <https://www.kaitoy.xyz/2020/11/05/sqlalchemy-core/>
[^9]: <https://ja.wikipedia.org/wiki/SQLAlchemy>
[^10]: <https://benelop.jp/blog/flask/application-models/>
[^13]: <https://scrapbox.io/PythonOsaka/SQLAlchemy%E3%82%92%E4%BD%BF%E3%81%A3%E3%81%A6%E3%81%BF%E3%82%88%E3%81%86>
[^16]: <https://chocottopro.com/?p=190>
[^20]: <https://book.st-hakky.com/hakky/sqlalchemy-intro/>

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

### テーブルのリレーションシップ

参考: [Relationship Configuration — SQLAlchemy 2\.0 Documentation](https://docs.sqlalchemy.org/en/20/orm/relationships.html)

1:1のリレーションシップの場合

```python
class Parent(Base):
    __tablename__ = "parent_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    children: Mapped[List["Child"]] = relationship(back_populates="parent")


class Child(Base):
    __tablename__ = "child_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey("parent_table.id"))
    parent: Mapped["Parent"] = relationship(back_populates="children")
```

1:nのリレーションシップの場合

```python
class Parent(Base):
    __tablename__ = "parent_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    children: Mapped[List["Child"]] = relationship(back_populates="parent")


class Child(Base):
    __tablename__ = "child_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey("parent_table.id"))
    parent: Mapped["Parent"] = relationship(back_populates="children")
```

n:1のリレーションシップの場合

```python
from typing import Optional


class Parent(Base):
    __tablename__ = "parent_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    child_id: Mapped[Optional[int]] = mapped_column(ForeignKey("child_table.id"))
    child: Mapped[Optional["Child"]] = relationship(back_populates="parents")


class Child(Base):
    __tablename__ = "child_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    parents: Mapped[List["Parent"]] = relationship(back_populates="child")
```

n:nのリレーションシップの場合

```python
from __future__ import annotations

from sqlalchemy import Column
from sqlalchemy import Table
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


# note for a Core table, we use the sqlalchemy.Column construct,
# not sqlalchemy.orm.mapped_column
association_table = Table(
    "association_table",
    Base.metadata,
    Column("left_id", ForeignKey("left_table.id")),
    Column("right_id", ForeignKey("right_table.id")),
)


class Parent(Base):
    __tablename__ = "left_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    children: Mapped[List[Child]] = relationship(secondary=association_table)


class Child(Base):
    __tablename__ = "right_table"

    id: Mapped[int] = mapped_column(primary_key=True)
```

リレーションに関連する事項としてカスケードが有ります。

参考: [Cascades — SQLAlchemy 2\.0 Documentation](https://docs.sqlalchemy.org/en/20/orm/cascades.html#cascade-delete)

カスケードの指示は`relationship()`の引数に`cascade`を指定することで行えます。

参考: [Relationships API — SQLAlchemy 2\.0 Documentation](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.cascade)

以下は、カスケードの機能を使って、親テーブルのデータを削除すると子テーブルのデータも削除される例です。

```python
class Profile(Base):
    """ユーザープロフィール"""

    __tablename__ = "user_profiles"
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(unique=True, index=True)
    date_of_birth: Mapped[Optional[datetime]]
    gender: Mapped[Optional[str]]
    occupation: Mapped[Optional[str]]
    interests: Mapped[list["Interest"]] = relationship(
        cascade="all, delete", order_by="Interest.id"
    )


class Interest(Base):
    """ユーザー興味事項"""

    __tablename__ = "user_interests"
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    interest: Mapped[str]
    user_profile_id: Mapped[int] = mapped_column(ForeignKey("user_profiles.id"))
    profile: Mapped["Profile"] = relationship(back_populates="interests")
```

リレーションシップを結んだテーブルのデータを取得する場合のサンプルコードです。

```python
    session = Session(engine)
    stmt = (
        select(Profile)
        .where(Profile.user_id == user_id)
        .options(joinedload(Profile.interests))
    )
    selected_profile = session.scalar(stmt)
```

`joinedload()`はリレーションシップを結んだテーブルのデータを取得する際に使用します。`joinedload()`は親子のデータをいっぺんにメモリ上にデータを取得するので、メモリの使用量やDBアクセスのパフォーマンスには注意が必要です。
