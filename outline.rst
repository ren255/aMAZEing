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



MAZE/
├── main.py
│   ├── Main                    # メインループ
│   └── call_back               # シーンとのインタラクション用、Mainのインスタンスを使用
│
├── main_logic.py
│   ├── Timer                   # 定期的な動作管理
│   ├── Render                  # 描画クラス
│   └── MazeGen                 # 迷路ジェネレータクラス
│
├── Scenes/
│   ├── Base_Scene.py           # シーンの共通基本機能
│   │   ├── BaseScene           # 基本のシーン関数、auto_layout
│   │   └── UIStore(BaseScene)  # UIelementを保存
│   ├── home.py                 # ホームシーン
│   │   └── home(BaseScene)     # Elementとevent処理 Mainのインスタンスを使用
│   └── maze.py                 # 迷路シーン
│       └── maze(BaseScene)     # Elementとevent処理 Mainのインスタンスを使用
│
└── themes/
    ├ theme.json               # デフォルトのテーマ設定ファイル
    └ custom.json              # カスタムテーマ設定ファイル






