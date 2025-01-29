---
date: 2025-01-29 16:49
---

# Pytest Tips

pytestはPython用のテストフレームワークで、ユニットテストや機能テストを簡単に作成・実行するためのツールです。

pytestは、Pythonのテストを効率的かつ効果的に行うための強力なツールです。シンプルなインターフェイスと強力な機能を兼ね備えており、小規模なプロジェクトから大規模なプロジェクトまで幅広く利用されています。公式ドキュメントも充実しているので、さらに詳細な情報が必要な場合は公式サイトや以下のコンテンツを参照してください。

**主な特徴**

1. **シンプルなテスト作成**: pytestを使用すると、テスト関数を簡単に作成できます。特別なテストクラスやセットアップが不要です。
2. **柔軟なフィクスチャ機能**: テストの前後に実行されるセットアップやクリーンアップのコードを簡単に管理できます。
3. **豊富なプラグイン**: テストカバレッジの測定やパラメタライズドテスト、他のフレームワークとの統合など、多くのプラグインが利用可能です。
4. **詳細なエラーレポート**: テストが失敗した場合、どこでどのように失敗したのかを詳細に報告します。

## 公式ドキュメント

* [pytest documentation](https://docs.pytest.org/en/stable/)

## Fixture

フィクスチャは`@pytest.fixture()`で修飾された関数を意味します。また、フィクスチャ関数を使ってセットアップするリソースのことを「フィクスチャ」と呼ぶこともあります。フィクスチャ関数はたいていテストに利用するデータを準備したり、取得したりします。場合によっては、このデータを「フィクスチャ」と見なすこともあります。pytestいがいのDjangoのようなフレームワークではもっと大きな意味で使われることもありますが、少なくともpytestの文脈ではテストの「前処理」コードと「後処理」コードをテスト関数から切り離せるようにするpytestのメカニズムを表します。

また、大事なこととして、テストコードの実行中に例外が発生した場合、しかるべくテスト結果はFAILEDになります。これに対して、フィクスチャの実行時に例外が発生した場合には、そのテスト関数はERRORになります。この違いはテストが失敗したときのデバッグの参考になります。

pytestのフィクスチャはpytestならではの機能です。多くの人がpytestに乗り換え、pytestを使い続ける理由はフィクスチャにあります。

フィクスチャの例:

```python
import pytest


@pytest.fixture()
def some_data():
    """Return answer to ultimate question."""
    return 42


def test_some_data(some_data):
    """Use fixture return value in a test."""
    assert some_data == 42
```

フィクスチャ関数は@pytest.fixture()で修飾（アノテーション）します。フィクスチャを前処理（と後処理）として使用するテスト関数はフィクスチャ関数の関数名を引数として取り、その引数にはフィクスチャ関数からの戻り値が格納されています。

### セットアップ（前処理）とティアダウン（後処理）にフィクスチャを使う

まず以下のようなテストコードがあるとします。

元のコード:

```python
from pathlib import Path
from tempfile import TemporaryDirectory
import cards


def test_empty():
    with TemporaryDirectory() as db_dir:
        db_path = Path(db_dir)
        db = cards.CardsDB(db_path)

        count = db.count()
        db.close()

        assert count == 0
```

8行目でDBのインスタンスを作成していますが、この部分はこれ以降テストを追加した場合にも必要そうです。11行目のDBのクローズ処理の呼び出しも同様です。このため、DBのインスタンス作成とテスト後のクローズ処理はフィクスチャとして切り出した方が良さそうなので、これをフィクスチャとして切り出し、コードを修正します。

フィクスチャ関数の切り出し:

```python
from pathlib import Path
from tempfile import TemporaryDirectory
import cards

import pytest


@pytest.fixture()
def cards_db():
  # 前処理
    with TemporaryDirectory() as db_dir:
        db_path = Path(db_dir)
        db = cards.CardsDB(db_path)
        yield db
        # 後処理
        db.close()


def test_empty(cards_db):
    assert cards_db.count() == 0
```

DBのインスタンス作成とクローズがフィクスチャ関数に切り出されました。pytestのフィクスチャ関数が他のテストフレームワークと大きく違うところが前処理と後処理をひとつの関数で書けてしまうので、処理の流れが掴みやすいところです。14行目でyieldで作成したDBのインスタンスをテスト関数に渡しているので、ここでいったんフィクスチャ関数の処理が中断され、テスト関数が終了してからyield以後の処理が実行されます。つまりyieldまでがテスト関数の前処理に当たり、yield以後がテスト関数の後処理に当たります。またyieldではなくreturnで呼び出し先のテスト関数に処理を戻すことで前処理だけをフィクスチャ関数に記述できます。

また、次のように追加したテスト関数でも同じフィクスチャ関数を使用できます。

```python
def test_two(cards_db):
    cards_db.add_card(cards.Card("first"))
    cards_db.add_card(cards.Card("second"))
    assert cards_db.count() == 2
```

フィクスチャとテスト関数は別々の関数です。フィクスチャで実行する処理やフィクスチャから返されるオブジェクト、あるいはその両方がフィクスチャの名前に反映されているとコードが理解しやすくなります。

### —setup-showオプションでフィクスチャの実行をトレースする

フィクスチャの実行内容はpytestに`—setup-show`オプションを付けることで確認する事ができます。

```shell
❯ pytest --setup-show test_count.py               
==== test session starts ====
platform win32 -- Python 3.12.4, pytest-8.3.2, pluggy-1.5.0
rootdir: C:\Users\ishisaka\src\pytest_book
configfile: pytest.ini
plugins: Faker-26.0.0, cov-5.0.0
collected 2 items                                                                                                                                                                           

test_count.py 
SETUP    S _session_faker
        SETUP    F cards_db
        cards_proj/tests/test_count.py::test_empty (fixtures used: _session_faker, cards_db, request).
        TEARDOWN F cards_db
        SETUP    F cards_db
        cards_proj/tests/test_count.py::test_two (fixtures used: _session_faker, cards_db, request).
        TEARDOWN F cards_db
TEARDOWN S _session_faker

==== 2 passed in 0.20s ===== 
```

SETUPとTEARDOWNの後ろにあるFはこのフィクスチャが関数（Function）単位で実行されていることを表しています。

### フィクスチャのスコープを指定する

フィクスチャにはスコープを指定する事ができます。先ほどのDBインスタンスの作成のような場合には重い処理である事が洋装されるので関数ごとにDB作成を行う事は適切ではない場合が多いです。ですので、テストコードのモジュールごとにフィクスチャ関数を実行させます。これには以下のリストのように`@pytest.fixture()`関数の`scope`引数を指定します。

フィクスチャのスコープを設定:

```python
@pytest.fixture(scope="module")
def cards_db():
    with TemporaryDirectory() as db_dir:
        db_path = Path(db_dir)
        db = cards.CardsDB(db_path)
        yield db
        db.close()
```

次に、scopeパラメーターの有効な値をまとめておきます。

* scope='function’
  テスト関数やメソッドごとに1回実行されます。セットアップの部分はこのフィクスチャを使っているテスト前に実行され、ティアダウンは部分はそのテスト後に実行されます。functionはscope引数が指定されない場合に使用されるデフォルトのスコープです。
* scope='class’
  テストクラスごとに1回実行されます。そのテストクラスにメソッドがいくつ定義されていたとしても、実行されるのは1回だけです。
* scope='module’
  モジュールごとに1回実行されます。そのモジュールにテスト関数、テストメソッド、またはその他のフィクスチャがいくつ定義されていたとしても、実行されるのは1回だけです。
* scope='package’
  パッケージごとに1回実行されます。そのパッケージにテスト関数、テストメソッド、またはその他のフィクスチャがいくつ定義されていたとしても、実行されるのは1回だけです。
* scope='session’
  セッションごとに1回実行されます。pytestコマンドを使ってテストを1回実行するのが1回のセッションです。セッションスコープのフィクスチャを使っているテストメソッドやテスト関数はすべて同じセットアップ/ティアダウン呼び出しを共有します。

スコープはフィクスチャで定義します。重要な点なのでしっかり憶えておきましょう。スコープを設定するのはフィクスチャを定義するときであり、フィクスチャを呼び出すときではありません。

フィクスチャがテストモジュールの中で定義されている場合、sessionスコープとpackageスコープの働きはmoduleスコープとまったく同じです。本来の意味でセッションやパッケージ共通のフィクスチャを記述するにはconftest.pyを使用します。

### conftest.pyを使ってフィクスチャを共有する

フィクスチャはここのテストファイルに配置できますが、複数のテストファイルでフィクスチャを共有したい場合conftest.pyファイルを使う必要があります。このファイルは、そのフィクスチャを使っているテストファイルと同じディレクトリか、親ディレクトリに配置します。`conftest.py`はpytestによって「ローカルプラグイン」と見なされるファイルで、このファイルもオプションです。このファイルにはフック関数やフィクスチャを追加できます。

ここまでテストファイルに記述していた、DBに関するフィクスチャを、同じディレクトリにある`conftest.py`ファイルに移動します。

conftest.py:

```python
from pathlib import Path
from tempfile import TemporaryDirectory
import cards
import pytest


@pytest.fixture(scope="session")
def cards_db():
    """CardsDB object connected to a temporary database"""
    with TemporaryDirectory() as db_dir:
        db_path = Path(db_dir)
        db = cards.CardsDB(db_path)
        yield db
        db.close()
```

それを使ったテストファイル:

```python
import cards


def test_empty(cards_db):
    assert cards_db.count() == 0


def test_two(cards_db):
    cards_db.add_card(cards.Card("first"))
    cards_db.add_card(cards.Card("second"))
    assert cards_db.count() == 2
```

DB処理のフィクスチャのスコープがセッション単位となり、普通にテストを実行できます。

フィクスチャが他のフィクスチャ（フィクスチャは他のフィクスチャを呼び出せます）に依存するとしたら、依存先のフィクスチャは同じスコープかそれより広いスコープのものでなければなりません。関数スコープのフィクスチャは、クラススコープ、モジュールスコープ、セッションスコープのフィクスチャに依存できますが、クラススコープのフィクスチャが関数スコープのフィクスチャに依存することはできません

また、`conftest.py`はimportすべきではありません。

### 組込フィクスチャ

pytestにはよく使われるフィクスチャがあらかじめ用意されています。

#### tmp_pathとtmp_path_factoryを使う

tmp_pathとtmp_path_factoryは一時ディレクトリの作成に使うフィクスチャです。

mp_pathは関数スコープのフィクスチャで有り、一時ディレクトリを表すpathlib.Pathを返します。この一時ディレクトリはテストが終了した後もしばらく残ります。tmp_path_factoryはセッションスコープのフィクスチャで、TempPathFactoryのオブジェクトを返します。このオブジェクトにはPathオブジェクトを返すmktmp()というメソッドが定義されていて、このメソッドを使って複数の一時ディレクトリを作成できます。

tmp_pathの例:

```python
def test_tmp_path(tmp_path):
    file = tmp_path / "file.txt"
    file.write_text("Hello")
    assert file.read_text() == "Hello"


def test_tmp_path_factory(tmp_path_factory):
    path = tmp_path_factory.mktemp("sub")
    file = path / "file.txt"
    file.write_text("Hello")
    assert file.read_text() == "Hello"
```

tmp_pathとtmp_path_factoryの使い方はほぼ同じですが、次のような違いがあります。

* tmp_path_factoryでは、ディレクトリを取得するためにmktmp()を呼び出す必要がある。
* tmp_path_factoryはセッションスコープ
* tmp_pathは関数スコープ

pytestに含まれている一時ディレクトリ関連のフィクスチャでは、ベースディレクトリはシステムとユーザーに依存します。このディレクトリはセッションが終わってもすぐに削除されるわけではないので、テストが失敗したときにはこのディレクトリを調べることができます。pytestがシステムに残しておくのは数回分のベースディレクトリだけであり、それ以外は最終的にクリーンアップされます。

また、ベースディレクトリを独自に指定したい場合には、`pytest —basetemp=<ディレクトリ名>`を使います。

#### capsysを使う

アプリケーションが出力したい標準出力や、標準エラー出力をテスト場合があります。そのような場合にはcapsysを使うと便利です。

capsysは標準出力と標準エラー出力をキャプチャするためのフィクスチャです。capsysはキャプチャした出力をキャプチャした順番で返すため、標準出力と標準エラー出力の順番が保持されます。

capsysの例:

```python
def test_version_v2(capsys):
    cards.cli.version()
    output = capsys.readouterr().out.rstrip()
    assert output == cards.__version__
```

3行目で使われています。`capsys.readouterr()`はoutとerrorが格納された名前付きタプルを返します。この例ではout側だけを取り出し、`rstrip()`で改行を削除しています。

#### モンキーパッチ

「モンキーパッチ」は実行時にクラスやモジュールを動的に変更するというものです。テスト時のモンキーパッチは、アプリケーションコードの実行環境を一部操作し、入力または出力の依存ファイルを置き換えるための手段になります。monkeypatchという組込フィクスチャを利用すればモンキーパッチをテスト実現できます。

詳細については以下の公式ドキュメントを確認してください。

[How to monkeypatch/mock modules and environments \- pytest documentation](https://docs.pytest.org/en/stable/how-to/monkeypatch.html#how-to-monkeypatch-mock-modules-and-environments)

#### その他の組込フィクスチャ

以下の公式ドキュメントを確認してください。

[Fixtures reference \- pytest documentation](https://docs.pytest.org/en/stable/reference/fixtures.html#built-in-fixtures)

### 非同期のfixture

`pytest_asyncio`をインポートして、`@pytest.mark.asyncio`を使うことで非同期のfixtureを定義できる。

```python
import pytest
import pytest_asyncio
from collections.abc import AsyncGenerator

@pytest_asyncio.fixture()
async def fixture() -> AsyncGenerator[str, None]:
    yield "a"

@pytest.mark.asyncio
async def test(fixture: str):
    assert fixture == "a"
```
