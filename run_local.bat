@echo off
chcp 65001 > nul
echo ====================================================
echo        VoiceOps 售后智能平台 本地自适应启动器
echo ====================================================
echo [1/2] 正在启动自适应端口检测与后端服务...
start "VoiceOps Backend" cmd /k "python scripts\start_backend.py"

echo [2/2] 正在启动前端开发服务...
timeout /t 3 /nobreak > nul
cd frontend
start "VoiceOps Frontend" cmd /k "npm run dev"

echo.
echo ====================================================
echo [✓] 后端与前端已在独立窗口启动！
echo     后端启动器已自动完成端口巡检与冲突规避。
echo ====================================================
pause
