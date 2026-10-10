import socket
import os
import sys
import subprocess
import time

# 兼容 Windows 控制台 UTF-8 编码
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 确保项目根目录在 python path 中
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

def find_available_port(start_port: int, max_attempts: int = 50, host: str = "127.0.0.1") -> int:
    """从 start_port 开始探测可用端口，若被占用或受限则自动递增"""
    for port in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                s.bind((host, port))
                return port
            except OSError:
                continue
    raise RuntimeError(f"在 {start_port} ~ {start_port + max_attempts} 范围内未找到可用端口！")

def update_frontend_proxy(backend_port: int):
    """动态更新前端 vite.config.ts 的代理目标端口"""
    vite_config_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "vite.config.ts")
    if not os.path.exists(vite_config_path):
        return
    
    with open(vite_config_path, "r", encoding="utf-8") as f:
        content = f.read()

    import re
    # 替换 target: 'http://127.0.0.1:XXXX' 或 'http://localhost:XXXX'
    new_content = re.sub(
        r"target:\s*['\"]http://(127\.0\.0\.1|localhost):\d+['\"]",
        f"target: 'http://127.0.0.1:{backend_port}'",
        content
    )
    with open(vite_config_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"[*] 已同步更新前端反向代理指向: http://127.0.0.1:{backend_port}")

def main():
    preferred_port = 8000
    host = "127.0.0.1"
    
    print("=" * 60)
    print(" VoiceOps 自适应端口巡检与后端智能启动器")
    print("=" * 60)
    
    # 探测后端可用端口
    target_port = find_available_port(preferred_port, host=host)
    if target_port != preferred_port:
        print(f"[!] 默认端口 {preferred_port} 被占用或受系统策略限制")
        print(f"[✓] 端口巡检机制自动切换至下一个可用端口 -> {target_port}")
    else:
        print(f"[✓] 默认端口 {preferred_port} 校验通过，状态空闲")
        
    # 同步前端代理
    update_frontend_proxy(target_port)
    
    print(f"\n[🚀] 正在启动 FastAPI 后端服务: http://{host}:{target_port}")
    print(f"[📖] 交互式 API 文档地址: http://{host}:{target_port}/docs\n")
    
    # 运行 uvicorn
    import uvicorn
    uvicorn.run("backend.app.main:app", host=host, port=target_port, reload=True, app_dir=ROOT_DIR)

if __name__ == "__main__":
    main()
