# Baby Turtle Communication

まず、Baby Turtleの概要を述べ、次にBaby Turtle 通信プログラムの説明と導入手順を説明します。

## Baby Turtle概要

Baby TurtleはEDGEMATRIX Inc.が開発した３２ビットMCUを内蔵した超小型ボードで、Edge AI BOX内のJetson moduleとシリアル通信を介してheat beatや各種コマンドのやりとりを行います。またEdge AI BOXの主電源をON/OFFできる機能を持っており、Edge AI BOXの異常を検出した場合に主電源を入れ直すことで異常状態からの回復を試みることが可能です。

Baby Turtleには外付け型と内蔵型の2種類があります。詳細はXXXXを参照してください。

以下は外付け型子亀通信プログラムの導入手順になります。

## 外付け型Baby Turtle 通信プログラム

ファイルは以下の3種類になります。

- BT-SerialCommunication.py
- start_bt.service
- start_bt.sh

PythonはPython 3.6 にて動作検証しています。

### Edge AI BOx Light への導入手順

- Edge AI BOXに nvidia でlogin します。
- pipをインストールします。
  - sudo apt install -y python3-pip
  - python3 -m pip install --upgrade pip
- schedule and pyserialをインストールします。
  - python3 -m pip install schedule pyserial
- dialoutグループにnvidiaを追加します。
  - id -a   （dialoutにnvidiaが含まれていないことを確認）
  - sudo gpasswd -a nvidia dialout
  - reboot
- nvidiaでloginし、dialoutに追加できたか確認する
  - id -a

- BT-SerialCommunication.py, start_bt.service, start_bt.shを~/bt-01/下にコピーします。
  - scp例
    - 例えば自分のPCのフォルダに移動してscpコマンドを実行する。
      - scp BT-SerialCommunication.py nvidia@xxx.xxx.xxx.xxx
- BT-SerialCommunication.pyの内容を確認・変更する。
  - /dev/ttyACM0　　<- USBケーブルを使ったシリアル通信デバイスがこれでいいか確認
  - log file folder　　<- /home/nvidia/bt-01を基本にしています
- python3 BT-SerialCommunication.py で試験。　まだservice 起動していない
- 動作に問題ないようであれば自動起動設定
  - /etc/systemd/system の下にサービスファイルをコピーする。
    - sudo systemctl enable start_bt.service
    - sudo systemctl start start_bt.service     （試しに起動してみる）
    - sudo systemctl status start_bt.service　　 （動作確認）
    - rebootで起動するか確認
    - reboot　　して立ち上がってから、
    - sudo systemctl status start_bt.service      （動作確認）
