MAZE/
├── main.py
├── main_logic.py
├── Scenes/
│   ├── Base_Scene.py
│   ├── Home_Scene.py
│   └── Maze_Scene.py
└── themes/
    ├── theme.json
    └── custom.json



aMAZEing/
├── main.py
│   ├── Main                  # mainloopの管理クラス
│   └── call_back             # シーンとのインタラクション用、Mainのインスタンスを使用
│
├── main_logic.py
│   ├── stopwatch             # 時間を測る
│   ├── loopTimer             # 定期的に実行される関数を管理
│   ├── Timer                 # タイマー
│   ├── eachFrame             # 毎Frame、実行される関数を管理
│   ├── YieldListloop         # listを保存し順番に返す
│   ├── Maze                  # 迷路作成、迷路解析の1つのクラスを所持
│   ├── Render                # 描画関連のクラス
│   ├── DynaPlayerMaster      # プレイヤーのマスタークラス
│   └── MazeGen               # 迷路生成のクラス
│
├── Scenes/
│   ├── Base_Scene.py
│   │   ├── BaseScene         # シーンの共通基本機能を提供する基本クラス
│   │   └── UIStore(BaseScene)# UI要素を保存し管理するクラス
│   ├── Home_Scene.py
│   │   └── home(BaseScene)   # 要素とイベント処理を含む、Mainのインスタンスを使用
│   └── Maze_Scene.py
│       └── maze(BaseScene)   # 要素とイベント処理を含む、Mainのインスタンスを使用
│
└── themes/
    ├ theme.json             # デフォルトのテーマ設定ファイル
    └ custom.json            # カスタムテーマ設定ファイル





