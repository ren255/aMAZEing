MAZE/
├── main.py
├── main_logic.py
├── Scenes/
│   ├── BaseScene.py
│   ├── home.py
│   └── maze.py
└── themes/
    ├── theme.json
    └── custom.json



aMAZEing/
├── main.py
│   ├── Main()                  # メインループの管理クラス
│   └── call_back()             # シーンとのインタラクション用、Mainのインスタンスを使用
│
├── main_logic.py
│   ├── Timer()                 # ゲーム内のタイミング管理クラス
│   ├── Render()                # 描画関連のクラス
│   └── MazeGen()               # 迷路生成のクラス
│
├── Scenes/
│   ├── Base_Scene.py
│   │   ├── BaseScene()         # シーンの共通基本機能を提供する基本クラス
│   │   └── UIStore(BaseScene)  # UI要素を保存し管理するクラス
│   ├── Home_Scene.py
│   │   └── home(BaseScene)     # 要素とイベント処理を含む、Mainのインスタンスを使用
│   └── Maze_Scene.py
│       ├── maze(BaseScene)     # 要素とイベント処理を含む、Mainのインスタンスを使用
│       └── Player()            # プレイヤークラス
│
└── themes/
    ├ theme.json               # デフォルトのテーマ設定ファイル
    └ custom.json              # カスタムテーマ設定ファイル




