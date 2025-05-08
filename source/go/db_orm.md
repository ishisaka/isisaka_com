---
date: 2025-05-08 15:16
description: Go言語でのDBアクセスについて
author: Tadahiro Ishisaka
---

# Go言語でのDBアクセスについて

## database/sql

### 概要

Go言語の`database/sql`パッケージは、SQLデータベース操作のための標準インターフェースを提供するパッケージです。RDBMSごとに異なるドライバを組み合わせて利用することで、MySQLやPostgreSQL、SQLiteなど多様なデータベースに対応できます[^2][^5][^8]。

**主な特徴と使い方**

- **ドライバのインポート**  
  利用するDBに応じたドライバ（例：`github.com/go-sql-driver/mysql`）を`_`付きでインポートします。これはドライバの`init()`を実行し、`database/sql`から利用可能にするためです[^2][^3]。

- **接続管理**  
  `sql.Open`でデータベース接続用の`*sql.DB`オブジェクトを取得しますが、これは実際のコネクションではなくコネクションプールの管理やクエリ発行のための抽象インターフェースです。実接続の確認には`db.Ping()`を使います[^2][^3]。

- **クエリ実行**  
  - 複数行のSELECTは`db.Query`、1行だけ取得する場合は`db.QueryRow`を使います。
  - INSERT/UPDATE/DELETEなどは`db.Exec`で実行し、`LastInsertId`や`RowsAffected`で結果を取得できます[^2][^6][^18]。

- **トランザクション**  
  `db.Begin`でトランザクションを開始し、`tx.Commit`または`tx.Rollback`で完了・中断を制御します。エラー発生時は必ずロールバックすることが推奨されます[^2][^17]。

- **プリペアドステートメントとプレースホルダ**  
  SQLインジェクション対策として、`?`や`$1`などのプレースホルダを使い、引数で値を渡します[^2][^15]。

- **NULL値の扱い**  
  NULLを許容するカラムはポインタ型や`sql.NullString`などの専用型で受け取ります[^6]。

- **接続のクローズ**  
  使用後は`db.Close()`でコネクションプールを閉じます。各クエリの`rows`も`defer rows.Close()`で明示的にクローズします[^2]。

**まとめ**
`database/sql`は汎用的なインターフェースを持ち、ドライバを切り替えるだけで異なるDBにも対応可能です。コネクションプールやトランザクション、プリペアドステートメントなど、実運用に必要な機能を標準で備えており、GoでのDB操作の基盤となっています[^2][^3][^5]。

### リファレンス

- [sql package \- database/sql \- Go Packages](https://pkg.go.dev/database/sql@go1.24.3)

### チュートリアル

- [Tutorial: Get started with Go \- The Go Programming Language](https://go.dev/doc/tutorial/getting-started)
- [Go database/sql tutorial](http://go-database-sql.org/index.html)

### 参考

- [Go言語でDBアクセス\(database/sql\) \#Go \- Qiita](https://qiita.com/taka23kz/items/cb7ae9ac6cf343b3dec2)

[^2]: <https://zenn.dev/skrikzts/articles/52613e78aef6d6>
[^3]: <https://golang.shop/post/go-databasesql-01-overview-ja/>
[^5]: <https://iketechblog.com/database-sql-go-sqlite3/>
[^6]: <https://www.twihike.dev/docs/golang-database/queries>
[^8]: <https://props-room.com/articles/handbook/golang-guide-416>
[^15]: <https://qiita.com/Rqixy/items/bcac0f84a537ecbc1ab4>
[^17]: <https://note.com/artefactnote/n/n096abb5bd792>
[^18]: <https://yossi-note.com/golang_database_access_2/>
