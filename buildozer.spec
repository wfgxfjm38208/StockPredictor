[app]

# 应用名称
title = StockPredictor

# 包名（唯一标识）
package.name = stockpredictor
package.domain = com.example

# 源码文件
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# 版本
version = 1.0.0

# 需求库
requirements = python3==3.11.9,kivy==2.2.1,numpy==1.23.5,pandas==1.5.3,requests,scikit-learn==1.2.2

# Android配置
android.permissions = INTERNET
android.api = 30
android.minapi = 21
android.ndk = 23b
android.sdk = 30

# 图标
# icon.filename = %(source.dir)s/icon.png

# 方向
orientation = portrait

# 全屏
fullscreen = 0

# 包名
package.name = stockpredictor
package.domain = com.example

[buildozer]

log_level = 2
warn_on_root = 1