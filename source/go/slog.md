---
date: 2025-06-05 13:22
description: log/slog
author: Tadahiro Ishisaka
---

# Go言語のlog/slogパッケージ

## log/slogについて

Go言語の`log/slog`パッケージは、Go 1.21で導入された**構造化ロギング**のための標準ライブラリです。ログをキーと値のペアとして出力することで、人間にとっての可読性だけでなく、機械による処理や分析も容易にします。

### 主な特徴 📝

* **レベル付きロギング**: `Debug`, `Info`, `Warn`, `Error`といったログレベルをサポートし、出力するログの重要度を制御できます。
* **構造化された出力**: デフォルトでは、ログはキーと値のペアで構成されるテキスト形式（`key=value`）またはJSON形式で出力されます。これにより、ログの検索やフィルタリングが容易になります。
* **柔軟なハンドラ**: `slog.Handler`インターフェースを実装することで、ログの出力形式（テキスト、JSONなど）や出力先（標準出力、ファイル、ネットワークなど）をカスタマイズできます。
* **コンテキスト対応**: `context.Context`と連携し、リクエストIDなどの共通情報をログに含めることが容易です。

### 簡単な使い方 💡

```go
package main

import (
	"log/slog"
	"os"
)

func main() {
	// デフォルトのテキストハンドラでロガーを作成
	logger := slog.New(slog.NewTextHandler(os.Stdout, nil))

	// 情報レベルでログを出力
	logger.Info("ユーザーがログインしました", "userID", 123, "userName", "gopher")

	// エラーレベルでログを出力
	logger.Error("データベース接続に失敗しました", "error", "connection refused")
}
```

### メリット ✨

`log/slog`を利用することで、ログの可読性向上、効率的なログ分析、パフォーマンスへの影響低減といったメリットが期待できます。標準パッケージであるため、外部ライブラリへの依存を減らすことも可能です。

より詳細な情報や高度な使い方については、[公式ドキュメント](https://pkg.go.dev/log/slog)を参照してください。

## 使い方の例

### 基本的なログ出力

```go
package main

import "log/slog"

func main() {
	// slogは標準のlogと違いログの出力レベルを指定できるのがメリットの一つ
	// Infoレベルで単純なログを標準エラー出力に出力する
	slog.Info("Hello, world!")
}
```

### レベル分け

slogは標準のログと違い、ログのレベルを指定できます。以下は、異なるレベルのログを出力する例です。

```go
package main

import (
	"context"
	"log/slog"
	"os"
)

func main() {
	// ログレベルの変数を作る
	var programLevel = new(slog.LevelVar)
	// ログハンドラーを作り、ログレベルの変数をHandlerOptionのLevelに割り当てる
	h := slog.NewJSONHandler(os.Stderr, &slog.HandlerOptions{Level: programLevel})
	// 作成したハンドラーを標準のログ出力に設定
	slog.SetDefault(slog.New(h))

	/*
	Log Levelの設定
	const (
		LevelDebug Level = -4
		LevelInfo  Level = 0
		LevelWarn  Level = 4
		LevelError Level = 8
	)
	*/

	// ログレベルを設定
	programLevel.Set(slog.LevelDebug)

	// 設定したレベル以上のログが表示される
	slog.Debug("debug")
	slog.Info("info")
	slog.Warn("warn")
	slog.Error("error")

	// 標準には無いログレベルの設定と出力
	slog.Log(context.TODO(), 2, "Level 2")
	// 表示例： {"time":"2025-06-04T10:04:03.603603+09:00","level":"INFO+2","msg":"Level 2"}
}
```

### 属性とグループ

`slog`では、ログに属性を追加することで、より詳細な情報を付加できます。また、属性はグループにできます。

以下は、属性を使用したログ出力の例です。

```go
package main

import (
	"context"
	"log/slog"
	"os"
)

func main() {
	// slogのメリットはログメッセージに属性を含められること
	// ログメッセージに属性を含める
	slog.Info("Hello", "number", 3)
	// slog.Attrを使用する
	// slog.Attrを使用するとリフレクションを使用しなくて済むので
	// 実行速度が速くなる
	slog.Info("hello", slog.Int("number", 3))

	// Logger.Withメソッドを使って新しいLoggerを構築し、全てのレコードにその属性を含める
	logger := slog.Default()
	logger2 := logger.With("url", "https://example.com")
	logger2.Info("Hello, world!")
	// 出力例: 2025/06/03 15:16:13 INFO Hello, world! url=https://example.com
}
```

以下は、属性をグループにしたログ出力の例です。

```go
package main

import (
	"os"

	"log/slog"
)

func main() {
	// テキストハンドラーを作成（標準エラー出力）
	logger := slog.New(slog.NewTextHandler(os.Stderr, nil))
	// JSONハンドラーを作成したい場合は以下のようにします
	// logger := slog.New(slog.NewJSONHandler(os.Stderr, nil))

	// --- グループを使用したログ出力の例 ---
	logger.Info("ユーザー情報",
		slog.String("id", "user-123"),
		slog.Group("details",
			slog.String("email", "test@example.com"),
			slog.Int("age", 30),
			slog.Group("address", // ネストしたグループ
				slog.String("street", "123 Main St"),
				slog.String("city", "Anytown"),
			),
		),
		slog.Bool("isActive", true),
	)

	// --- WithGroup を使用してロガーにグループを永続的に設定する例 ---
	// "request" グループを持つ新しいロガーを作成
	requestLogger := logger.WithGroup("request")

	requestLogger.Info("受信リクエスト",
		slog.String("method", "GET"),
		slog.String("path", "/api/data"),
	)

	requestLogger.Error("リクエスト処理エラー",
		slog.Int("statusCode", 500),
		slog.String("error", "データベース接続エラー"),
	)

	// さらにネストしたグループを WithGroup で設定
	userRequestLogger := requestLogger.WithGroup("user")
	userRequestLogger.Info("ユーザー関連リクエスト",
		slog.String("userID", "user-456"),
	)

}
```

### ハンドラーとJSON出力

`slog`では、ハンドラーを使用してログの出力形式をカスタマイズできます。以下は、JSON形式でログを出力する例です。

```go
package main

import (
	"log/slog"
	"os"
)

func main() {
	// JSONハンドラを使ってJSON形式で出力する
	// 標準のハンドラにはJSONとTEXTがある
	loggerwJsonHandler := slog.New(slog.NewJSONHandler(os.Stdout, nil))
	loggerwJsonHandler.Info("Hello, world!")
	// 出力例: {"time":"2025-06-03T15:18:52.53884+09:00","level":"INFO","msg":"Hello, world!"}
	loggerwJsonHandler.Info("Hello", slog.Int("number", 3))
}
```

### コンテキストの使用

`slog`は`context.Context`と連携して、リクエストIDやトレースIDなどの共通情報をログに含めることができます。以下は、コンテキストを使用したログ出力の例です。

ここでは、コンテキストから情報を抽出してログに追加するカスタムハンドラーを実装しています。

```go
package main

import (
	"context"
	"log/slog"
	"os"
)

// contextKey はコンテキスト内で値を一意に識別するためのキーです。
type contextKey string

const (
	traceIDKey contextKey = "traceID"
	userIDKey  contextKey = "userID"
)

// ContextHandler は、コンテキストから指定されたキーの値を抽出し、
// ログレコードに自動的に追加する slog.Handler のラッパーです。
type ContextHandler struct {
	slog.Handler
	keys []contextKey // コンテキストから抽出するキーのリスト
}

// NewContextHandler は ContextHandler を作成します。
func NewContextHandler(handler slog.Handler, keys []contextKey) *ContextHandler {
	return &ContextHandler{
		Handler: handler,
		keys:    keys,
	}
}

// Handle は、元のハンドラの Handle メソッドを呼び出す前に、
// コンテキストから情報を抽出してログレコードに追加します。
func (h *ContextHandler) Handle(ctx context.Context, r slog.Record) error {
	for _, key := range h.keys {
		if val := ctx.Value(key); val != nil {
			// slog.Any は便利ですが、具体的な型で slog.String, slog.Int などを使う方が望ましい場合もあります。
			r.AddAttrs(slog.Any(string(key), val))
		}
	}
	return h.Handler.Handle(ctx, r)
}

// WithAttrs は、ラップされたハンドラの WithAttrs を呼び出します。
// 新しい ContextHandler を返すように実装することもできます。
func (h *ContextHandler) WithAttrs(attrs []slog.Attr) slog.Handler {
	return NewContextHandler(h.Handler.WithAttrs(attrs), h.keys)
}

// WithGroup は、ラップされたハンドラの WithGroup を呼び出します。
// 新しい ContextHandler を返すように実装することもできます。
func (h *ContextHandler) WithGroup(name string) slog.Handler {
	return NewContextHandler(h.Handler.WithGroup(name), h.keys)
}

func main() {
	// ベースとなるハンドラ (例: JSONHandler)
	baseHandler := slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
		AddSource: true, // ソースコードの位置情報を追加
		Level:     slog.LevelDebug,
	})

	// コンテキストから traceIDKey と userIDKey を抽出するカスタムハンドラ
	contextAwareHandler := NewContextHandler(baseHandler, []contextKey{traceIDKey, userIDKey})

	// カスタムハンドラを使用してロガーを作成
	logger := slog.New(contextAwareHandler)

	// --- コンテキストに情報を追加 ---
	ctx := context.Background()
	ctx = context.WithValue(ctx, traceIDKey, "trace-xyz-789")
	ctx = context.WithValue(ctx, userIDKey, "user-prod-456")

	// --- ログ出力 (カスタムハンドラが自動的にコンテキスト情報を追加) ---
	logger.InfoContext(ctx, "ユーザーがログインしました", slog.String("username", "gopher"))

	// 別のリクエストのコンテキスト（異なる値）
	ctx2 := context.Background()
	ctx2 = context.WithValue(ctx2, traceIDKey, "trace-def-456")
	// userIDKey はこのコンテキストには設定しない

	logger.WarnContext(ctx2, "在庫が少なくなっています", slog.String("itemID", "item-001"), slog.Int("currentStock", 5))

	// コンテキストがない場合（またはキーが含まれていない場合）
	logger.ErrorContext(context.Background(), "重要なエラーが発生しました", slog.String("errorCode", "E-1024"))
}
```

### 属性の一部をマスクする

シークレットなどログ出力の際に一部の属性をマスクしたい場合があります。以下は、属性の一部をマスクする例です。

LogValuerインターフェイスを実装することで、特定の型の値をログ出力時にカスタマイズできます。

```go
package main

import (
	"log/slog"
	"os"
)

// Token はシークレットにしたいものの例
type Token string

// LogValue はLogValuerインターフェイスの実装
// Token型の値を"REDACTED_TOKEN"に書き換える
func (Token) LogValue() slog.Value {
	return slog.StringValue("REDACTED_TOKEN")
}

func main() {
	t := Token("shhhh!")
	logger := slog.New(slog.NewTextHandler(os.Stdout, nil))
	logger.Info("permission granted", "user", "Perry", "token", t)
	// time=2025-06-04T14:06:36.595+09:00 level=INFO msg="permission granted" user=Perry token=REDACTED_TOKEN
}
```

### ログレコードの置き換え

`slog`では、ログレコードを置き換えることができます。以下は、ログレコードを置き換える例です。

```go
package main

import (
	"os"

"log/slog"
)

func main() {
	// Exported constants from a custom logging package.
	 const (
		LevelTrace     = slog.Level(-8)
		LevelDebug     = slog.LevelDebug
		LevelInfo      = slog.LevelInfo
		LevelNotice    = slog.Level(2)
		LevelWarning   = slog.LevelWarn
		LevelError     = slog.LevelError
		LevelEmergency = slog.Level(12)
	)

	th := slog.NewTextHandler(os.Stdout, &slog.HandlerOptions{
		// カスタムレベルのLevelTraceをデフォルトのレベルに設定
		Level: LevelTrace,

		// ログレコードの属性を置き換える関数を設定
		ReplaceAttr: func(groups []string, a slog.Attr) slog.Attr {
			// ログ出力からタイムスタンプを削除
			if a.Key == slog.TimeKey {
				return slog.Attr{}
			}

			// カスタムのレベルとそのキーを設定
			if a.Key == slog.LevelKey {
				// レベルのキーを"level" から "sev" に変更
				a.Key = "sev"

				// カスタムレベル値のハンドする
				level := a.Value.Any().(slog.Level)

				// カスタムレベルに合わせてログに出力するレベルを表す文字列を設定
				switch {
				case level < LevelDebug:
					a.Value = slog.StringValue("TRACE")
				case level < LevelInfo:
					a.Value = slog.StringValue("DEBUG")
				case level < LevelNotice:
					a.Value = slog.StringValue("INFO")
				case level < LevelWarning:
					a.Value = slog.StringValue("NOTICE")
				case level < LevelError:
					a.Value = slog.StringValue("WARNING")
				case level < LevelEmergency:
					a.Value = slog.StringValue("ERROR")
				default:
					a.Value = slog.StringValue("EMERGENCY")
				}
			}

			return a
		},
	})

	logger := slog.New(th)
	logger.Log(nil, LevelEmergency, "missing pilots")
	logger.Error("failed to start engines", "err", "missing fuel")
	logger.Warn("falling back to default value")
	logger.Log(nil, LevelNotice, "all systems are running")
	logger.Info("initiating launch")
	logger.Debug("starting background job")
	logger.Log(nil, LevelTrace, "button clicked")

}

/*
出力例
sev=EMERGENCY msg="missing pilots"
sev=ERROR msg="failed to start engines" err="missing fuel"
sev=WARNING msg="falling back to default value"
sev=NOTICE msg="all systems are running"
sev=INFO msg="initiating launch"
sev=DEBUG msg="starting background job"
sev=TRACE msg="button clicked"
*/
```

### ログを同時に複数の出力先に出力する

ログを同時に複数の出力先に出力するには2つの方法があります。

1つ目は`io.MultiWriter`を使用して複数の出力先に同じ内容を出力する方法です。

```go
package main

import (
	"io"
	"log/slog"
	"os"
)

func main() {
	// ログをファイルと標準出力に同時に出力する
	// ログファイルを開く (または作成する)
	logFile, err := os.OpenFile("app.log", os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0666)
	if err != nil {
		slog.Error("ログファイルを開けませんでした", slog.Any("error", err))
		os.Exit(1)
	}
	defer logFile.Close()

	// io.MultiWriter を作成して、標準出力とファイルの両方に出力するようにする
	//    os.Stdout: 標準出力
	//    logFile:   開いたファイル
	multiWriter := io.MultiWriter(os.Stdout, logFile)

	// MultiWriter を出力先とするハンドラを作成
	// ここでは TextHandler を使用する例。JSONHandler も同様に使えます。
	//    handler := slog.NewJSONHandler(multiWriter, nil)
	handler := slog.NewTextHandler(multiWriter, &slog.HandlerOptions{
		AddSource: true,            // ソースコードの位置情報を追加する場合
		Level:     slog.LevelDebug, // ログレベルを設定
	})

	// カスタムハンドラを使用してロガーを作成
	logger := slog.New(handler)

	// ログを出力 (標準出力と app.log の両方に出力される)
	logger.Debug("これはデバッグメッセージです。")
	logger.Info("アプリケーションが起動しました。", slog.String("version", "1.0.0"))
	logger.Warn("設定ファイルが見つかりません。デフォルト値を使用します。", slog.String("config_path", "./config.toml"))
	logger.Error("重大なエラーが発生しました。", slog.String("error_code", "SYS_001"), slog.String("details", "データベース接続に失敗"))

	slog.SetDefault(logger)
	slog.Info("デフォルトロガーも設定できます。") // slog.SetDefault で設定した場合
}
```

2つ目は、`slog.Handler`を実装して、複数のハンドラーにログを出力する方法です。

```go
package main

import (
	"context"
	"errors" // Go 1.20+ で errors.Join を使う場合
	"log/slog"
	"os"
)

// MultiHandler は複数の slog.Handler にログをディスパッチします。
type MultiHandler struct {
	handlers []slog.Handler
}

// NewMultiHandler は MultiHandler を作成します。
func NewMultiHandler(handlers ...slog.Handler) *MultiHandler {
	return &MultiHandler{handlers: handlers}
}

// Enabled は、いずれかのラップされたハンドラが指定されたレベルで有効な場合に true を返します。
func (h *MultiHandler) Enabled(ctx context.Context, level slog.Level) bool {
	for _, handler := range h.handlers {
		if handler.Enabled(ctx, level) {
			return true
		}
	}
	return false
}

// Handle は、ラップされたすべてのハンドラにログレコードを渡します。
// いずれかのハンドラでエラーが発生した場合、エラーを集約して返します。
func (h *MultiHandler) Handle(ctx context.Context, r slog.Record) error {
	var errs []error
	for _, handler := range h.handlers {
		// 各ハンドラが Enabled かどうかをここで再チェックすることもできますが、
		// 通常は Enabled でフィルタリングされた後に Handle が呼ばれることを期待します。
		if err := handler.Handle(ctx, r); err != nil {
			errs = append(errs, err)
		}
	}
	if len(errs) > 0 {
		return errors.Join(errs...)
	}
	return nil
}

// WithAttrs は、ラップされたすべてのハンドラに属性を追加した新しい MultiHandler を返します。
func (h *MultiHandler) WithAttrs(attrs []slog.Attr) slog.Handler {
	newHandlers := make([]slog.Handler, len(h.handlers))
	for i, handler := range h.handlers {
		newHandlers[i] = handler.WithAttrs(attrs)
	}
	return NewMultiHandler(newHandlers...)
}

// WithGroup は、ラップされたすべてのハンドラにグループを追加した新しい MultiHandler を返します。
func (h *MultiHandler) WithGroup(name string) slog.Handler {
	newHandlers := make([]slog.Handler, len(h.handlers))
	for i, handler := range h.handlers {
		newHandlers[i] = handler.WithGroup(name)
	}
	return NewMultiHandler(newHandlers...)
}

func main() {
	// ファイルへのハンドラ (JSON形式、DEBUGレベル以上)
	logFile, err := os.OpenFile("app_multi.log", os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0666)
	if err != nil {
		slog.Error("ログファイルを開けませんでした", slog.Any("error", err))
		os.Exit(1)
	}
	defer logFile.Close()
	fileHandler := slog.NewJSONHandler(logFile, &slog.HandlerOptions{
		Level:     slog.LevelDebug,
		AddSource: true,
	})

	// 標準出力へのハンドラ (Text形式、INFOレベル以上)
	stdoutHandler := slog.NewTextHandler(os.Stdout, &slog.HandlerOptions{
		Level: slog.LevelInfo,
		ReplaceAttr: func(groups []string, a slog.Attr) slog.Attr {
			// 標準出力ではソース情報を表示しない例
			if a.Key == slog.SourceKey {
				return slog.Attr{}
			}
			return a
		},
	})

	// MultiHandler を作成
	multiHandler := NewMultiHandler(stdoutHandler, fileHandler)

	// ロガーを作成
	logger := slog.New(multiHandler)

	// ログ出力
	logger.Debug("このデバッグメッセージはファイルにのみ記録されます。") // stdoutHandlerのレベルはINFOなので表示されない
	logger.Info("この情報メッセージは標準出力とファイルの両方に記録されます。", slog.String("user", "admin"))
	logger.Warn("警告: ディスク容量が少なくなっています。", slog.Int("free_gb", 10))
	logger.Error("エラー発生！", slog.String("component", "API"))
}
```

### 設定ファイルを使用する

`slog`には標準で設定ファイルによる設定を行う機能はありませんが、独自に設定ファイルを読み込んでロガーを構成することは可能です。以下は、JSON形式の設定ファイルを読み込んで`slog`のロガーを構成する例です。

```go
/*
設定ファイルを使用してslogのログレベルやログ出力形式を設定するサンプルです。
以下のようなJSON形式のファイルを使用します。

ファイル名: config.json
{
  "log_level": "debug",
  "log_format": "json",
  "add_source": true
}
*/

package main

import (
	"encoding/json"
	"log/slog"
	"os"
)

// LogConfig はログ設定を表します。
// LogLevel はログ出力のレベルを指定します。
// LogFormat はログの出力形式を指定します。
// AddSource はログにソース情報を追加するかどうかを指定します。
type LogConfig struct {
	LogLevel  string `json:"log_level"`
	LogFormat string `json:"log_format"`
	AddSource bool   `json:"add_source"`
}

func main() {
	// 設定ファイルの読み込み
	configFile, err := os.Open("config.json")
	if err != nil {
		slog.Error("Failed to open config file", "error", err)
		os.Exit(1)
	}
	defer configFile.Close()

	var config LogConfig
	decoder := json.NewDecoder(configFile)
	if err := decoder.Decode(&config); err != nil {
		slog.Error("Failed to decode config file", "error", err)
		os.Exit(1)
	}

	// ログレベルの設定
	var level slog.Level
	switch config.LogLevel {
	case "debug":
		level = slog.LevelDebug
	case "info":
		level = slog.LevelInfo
	case "warn":
		level = slog.LevelWarn
	case "error":
		level = slog.LevelError
	default:
		slog.Warn("Invalid log level in config, defaulting to Info", "configured_level", config.LogLevel)
		level = slog.LevelInfo
	}

	// ログ出力形式の設定
	opts := &slog.HandlerOptions{
		// 出力元のファイル名と行番号を追加するかどうかの設定
		AddSource: config.AddSource,
		Level:     level,
	}

	// ログ出力形式の設定に応じてロガーの作成
	var handler slog.Handler
	switch config.LogFormat {
	case "json":
		handler = slog.NewJSONHandler(os.Stdout, opts)
	case "text":
		handler = slog.NewTextHandler(os.Stdout, opts)
	default:
		slog.Warn("Invalid log format in config, defaulting to Text", "configured_format", config.LogFormat)
		handler = slog.NewTextHandler(os.Stdout, opts)
	}

	// 新しいロガーを作成しそれ標準のロガーにする
	logger := slog.New(handler)
	slog.SetDefault(logger)

	// 設定されたロガーでログ出力
	slog.Debug("This is a debug message.")
	slog.Info("This is an info message.")
	slog.Warn("This is a warning message.")
	slog.Error("This is an error message.")
}
```

### サンプルコード

以上のサンプルコードは以下のGitHubリポジトリにまとめています。

[ishisaka/slog\_sample: Go言語のlog/slogの利用サンプル](https://github.com/ishisaka/slog_sample)
