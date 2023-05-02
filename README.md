# BabyTurtleCommunication
Baby Turtle Communication Programs
外付け型子亀の導入手順になります。
Python 3.6 にて検証しています。
Edge AI BOx Light への導入手順
    * install pip
        * sudo apt install -y python3-pip
        * python3 -m pip install --upgrade pip 
    * install schedule and pyserial
        * python3 -m pip install schedule pyserial
    * dialoutグループにnvidia追加
        * id -a   （dialoutにnvidiaが含まれていないことを確認）
        * sudo gpasswd -a nvidia dialout
        * reboot
    * dialoutに追加できたか確認する
        * id -a
    * BT-SerialCommunication.py 変更
        * scpなどでfileコピー 
            * 他に、start_bt.service と start_bt.sh も
        * USBでファイルを読もうとする場合のUSBマウント（参考）
            * https://www.rough-and-cheap.jp/linux/ubuntu-server-mount-usb/

        * edit プログラムのnano をinstallし、nanoでeditする
        * /dev/ttyACM0　　<- USBケーブルを使ったシリアル通信デバイスがこれでいいか確認
        * log file folder　　<- /home/nvidia/bt-01を基本にしています
    * python3 BT-SerialCommunication.py で試験。　まだservice 起動していない
    * 自動起動設定
        * /etc/systemd/system の下にサービスファイルをコピーする。
        * sudo systemctl enable start_bt.service
        * sudo systemctl start start_bt.service     （試しに起動してみる）
        * sudo systemctl status start_bt.service　　 （動作確認）
    * rebootで起動するか確認
        * reboot　　して立ち上がってから、
        * sudo systemctl status start_bt.service

