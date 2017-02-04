LDAのトピックモデル部分
==============

# 起動

```
$ jupyter notebook --generate-config
$ vim ~/..jupyter/jupyter_notebook_config.py
c = get_config()
c.NotebookApp.ip = '*'  # localhost以外からもアクセス可能にする。
c.NotebookApp.port = 9999  # サーバのポートを指定。デフォルト8888。
c.NotebookApp.open_browser = False  # ブラウザが自動で開かないようにする。
$ jupyter notebook
```

# 実行

pti_topic_modeler.ipynbを実行する
