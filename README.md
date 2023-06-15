# Baby Turtle Communication

まず、Baby Turtleの概要を述べ、次にBaby Turtle 通信プログラムの説明と導入手順を説明します。

## Baby Turtle概要

Baby TurtleはEDGEMATRIX Inc.が開発した３２ビットMCUを内蔵した超小型ボードで、Edge AI BOX内のJetson moduleとシリアル通信を介してheat beatや各種コマンドのやりとりを行います。またEdge AI BOXの主電源をON/OFFできる機能を持っており、Edge AI BOXの異常を検出した場合に主電源を入れ直すことで異常状態からの回復を試みることが可能です。

Baby Turtleには外付け型と内蔵型の2種類があります。詳細はアプリケーションノート（準備中）を参照してください。

以下は外付け型子亀通信プログラムの導入手順になります。

## 外付け型Baby Turtle 通信プログラム

ファイルは以下の6種類になります。

- BT-SerialCommunication.py
  - 外付け子亀とシリアル通信を行います。Edge AI BOXの異常を監視し、必要があれば、子亀にEdge AI Boxのcold boot （電源の入れ直し起動）を要求して自身の回復を試みます。また、シリアル通信にてheart beatを子亀に送っており、子亀側でheart beatが途絶えたことを検出した場合もcold bootを行います。
- start_bt.service
  - BT-SerialCommunication.py自動起動用ファイル
- start_bt.sh
  - BT-SerialCommunication.py自動起動用シェルスクリプト
- send_bt-logs.sh
  - BT-SerialCommunication.pyが吐き出すlogをemailで送出するためのシェルスクリプト
- sendlog.py
  - BT-SerialCommunication.pyが吐き出すlogをemailで送出するためのプログラム
- bt_id.txt
  - 子亀を区別するためのIDファイル

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
  - chmod u+x start_bt.shで実行できる様にする。（不要かもしれませんが）
  - /etc/systemd/systemの下にサービスファイルをコピーし、次に以下のコマンドを実行する。
    - sudo systemctl enable start_bt.service
    - sudo systemctl start start_bt.service     （試しに起動してみる）
    - sudo systemctl status start_bt.service　　 （動作確認）
    - rebootで起動するか確認
    - reboot　　して立ち上がってから、
    - sudo systemctl status start_bt.service      （動作確認）
- 以上で正常動作すればbt-01にlogファイル(BT-log)が作られます。BTーlogは毎日早朝２時頃bt-log.1~7にてローテーションするようにセーブされます。
- 以下は、logファイル(BT-log, BT-log.1,...,BT-log.7)をメールで読み出すための設定になります。
- send_bt_logs.sh, sendlog.py, bt_id.txtを~/bt-01/下にscpなどでコピーします。
- bt_id.txtは対象機(子亀と通信し合うEdge AI Box)のidとなりますので、各対象機でユニークなidとなるようにファイル内容を変更してください。フォーマットは自由です。
- chmod u+x send_bt-logs.sh を ~/bt-01 で実行します。
- sendlog.pyは基本的にgoogle mailを使用するようになっており、メールアドレスとloginするためのアプリケーションパスワードを準備しなければなりません。これらはユーザーにて準備をお願いします。
- メールで読み出すためのコマンドは、$./send_bt-logs.sh from@fromsample.com from-appPassword to@tosample.com になります。
  - from@fromsample.com : メールの送信元。このsmtpサーバーを使用します。このメールアドレスはgoogle mailを前提としています。
  - from-appPassword : 上記smtpサーバー(smtp.google.com)のアプリケーションパスワード。
  - to@tosample.com : メールの送信先。
  - /home/nvidia/bt-01 に移動して本コマンドを実行します。
  - 実行例：$./send_bt-logs.sh tx@sample1.com 1111222233334444 rx@sample2.com

End Of Doc 2023/06/16
