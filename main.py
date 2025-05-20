import time
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer

# ตัวแปรเพื่อเก็บข้อมูล
data_dict = {
    "ACC": {},
    "GYRO": {},
    "MAG": {}
}


def print_all(address, *args):
    # แยกข้อมูลตามประเภท
    if "ACC" in address:
        key = address.split(':')[-1]
        data_dict["ACC"][key] = args[-1]  # เก็บค่าเฉพาะค่าล่าสุด
    elif "GYRO" in address:
        key = address.split(':')[-1]
        data_dict["GYRO"][key] = args[-1]  # เก็บค่าเฉพาะค่าล่าสุด
    elif "MAG" in address:
        key = address.split(':')[-1]
        data_dict["MAG"][key] = args[-1]  # เก็บค่าเฉพาะค่าล่าสุด

    # ตรวจสอบว่ามีข้อมูลครบถ้วนหรือไม่
    if len(data_dict["ACC"]) == 3 and len(data_dict["GYRO"]) == 3 and len(data_dict["MAG"]) == 3:
        time.sleep(0)  # ดีเลย์ 3 วินาที
        print_data()


def print_data():
    print("\n### EmotiBit Data ###\n")

    for category, values in data_dict.items():
        print(f"**{category}**")
        for key, value in values.items():
            print(f"  - {key}: {value:.4f}")  # แสดงค่าในรูปแบบที่สวยงาม
        print()  # เพิ่มบรรทัดว่างหลังแต่ละหมวดหมู่

    print("------------------------------")  # แบ่งระหว่างชุดข้อมูล

    # ล้างข้อมูลหลังจากแสดงผล
    for category in data_dict:
        data_dict[category].clear()


dispatcher = Dispatcher()
dispatcher.set_default_handler(print_all)  # รับทุก path

ip = "0.0.0.0"
port = 12345

server = BlockingOSCUDPServer((ip, port), dispatcher)
print("Listening for EmotiBit OSC data...")
server.serve_forever()