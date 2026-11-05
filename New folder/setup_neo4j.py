import sys
import os
import getpass

# Force UTF-8 stdout if possible
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Ensure project root in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from knowledge_graph.neo4j_manager import neo4j_manager

def main():
    print("==================================================================")
    print("🌿 CÔNG CỤ THIẾT LẬP & ĐỒNG BỘ NEO4J DESKTOP KNOWLEDGE GRAPH")
    print("==================================================================")
    
    current_status = neo4j_manager.get_status()
    print(f"\n[1] Trạng thái hiện tại: {current_status['server_info']}")
    print(f"    - URI       : {current_status['uri']}")
    print(f"    - Username  : {current_status['user']}")
    
    # Try connecting with common passwords if not connected
    common_passwords = ["password", "12345678", "admin", "123456789", "diabetes123", "neo4j"]
    
    if not current_status["connected"]:
        print("\n[2] Đang kiểm tra kết nối với các mật khẩu mặc định phổ biến...")
        connected = False
        for pwd in common_passwords:
            print(f"    --> Thử mật khẩu: '{pwd}' ... ", end="", flush=True)
            res = neo4j_manager.update_credentials(current_status["uri"], current_status["user"], pwd)
            if res.get("connected"):
                print("THÀNH CÔNG! [OK]")
                connected = True
                break
            else:
                print("Không đúng.")
                
        if not connected:
            print("\n⚠️ Chưa kết nối được với mật khẩu mặc định.")
            print("👉 Vui lòng nhập thông tin kết nối từ Neo4j Desktop của bạn:")
            custom_uri = input(f"Nhập Bolt URI [mặc định {current_status['uri']}]: ").strip() or current_status['uri']
            custom_user = input(f"Nhập Username [mặc định {current_status['user']}]: ").strip() or current_status['user']
            custom_pwd = input("Nhập Password của DBMS bạn đã đặt trong Neo4j Desktop: ").strip()
            
            print(f"\nĐang kết nối tới {custom_uri} ...")
            res = neo4j_manager.update_credentials(custom_uri, custom_user, custom_pwd)
            if res.get("connected"):
                print(f"✅ {res['message']}")
            else:
                print(f"❌ {res['message']}")
                print("\n💡 Hướng dẫn kiểm tra trên Neo4j Desktop:")
                print("1. Mở phần mềm Neo4j Desktop trên máy.")
                print("2. Tìm Database của bạn trong Project và bấm nút 'START'.")
                print("3. Đảm bảo đèn trạng thái màu xanh lá (Active / Running) tại cổng 7687.")
                return
    else:
        print("\n[2] Đang đồng bộ lại toàn bộ dữ liệu vào Neo4j...")
        sync_res = neo4j_manager.sync_data()
        print(f"✅ {sync_res['message']}")

    # Final verification
    status = neo4j_manager.get_status()
    print("\n==================================================================")
    print(f"🎉 NEO4J KNOWLEDGE GRAPH ĐÃ SẴN SÀNG:")
    print(f"   • Số lượng Nodes       : {status['node_count']}")
    print(f"   • Số lượng Relationships: {status['relation_count']}")
    print(f"   • Trạng thái           : {status['server_info']}")
    print("==================================================================")
    print("👉 Bây giờ bạn có thể mở Web App tại http://127.0.0.1:5000 và xem đồ thị trực tiếp từ Neo4j!")

if __name__ == '__main__':
    main()
