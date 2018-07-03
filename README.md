# mixiの過去日記抽出

mixiの過去の日記を取得するスクリプトです。  
mixiのAPIのレスポンス（JSON）をファイルに保存します。  

mixiは日本がメインのサービスなので、日本語で作成しています。  

## 環境

Python3.6

## 事前準備

2つの作業が必要です。  

### サービス登録

[サービス管理](http://developer.mixi.co.jp/connect/mixi_graph_api/services/)の手順でサービスを追加する必要があります。  
注意としては、`リダイレクトURL`に*http://localhost:9999/redirect*を設定する必要があります。  

### mixi日記の一覧ページをダウンロード

[日記の一覧](http://mixi.jp/list_diary.pl?page=1)を右クリックでダウンロードし、htmlを特定のディレクトリ配下においてください。  

## インストール

必要様なスクリプトは以下のコマンドでダウンロードできます。  
また、依存ライブラリをインストールする必要があります。  

```bash
git clone https://github.com/pyohei/extract-mixi-diary.git
cd extract-mixi-diary
pip install -r requirements.txt # virtualenv上の実行がオススメ
```

## 使い方

### アクセストークン取得用サーバ起動

APIにアクセスするために、アクセストークンを取得する必要があります。  
以下のコマンドを実行し、  

```bash
python server.py -c `Consumer Key` -s `Consumer Secret`
```

`http://localhost:9999`にアクセスすればアクセストークンを取得できます。  

* 次のスクリプトで自動的にアクセストークンを取得するので、メモする必要はありません
* アクセストークンは期限が切れても自動で再取得します

### mixi日記取得スクリプトの起動

以下のコマンドで実行し、`-d`で渡したディレクトリに日記の作成日でファイルが作成されます。  

```bash
python main.py -o `上記で取得したHTMLを保存しているディレクトリ` -d `保存先ディレクトリ`
```

## 参考情報

* [mixi Connect » mixi Graph API » 認証認可手順（新方式）](http://developer.mixi.co.jp/connect/mixi_graph_api/api_auth/)
* [API共通仕様](http://developer.mixi.co.jp/connect/mixi_graph_api/mixi_io_spec_top/api_common_spec/)
* [Diary API](http://developer.mixi.co.jp/connect/mixi_graph_api/mixi_io_spec_top/diary-api/)

## License

* MIT
