TFT-Robot 开发规范
1. 依赖管理（uv）
Bash

# 初始化虚拟环境（可选，uv默认自动管理）
uv venv  

# 安装依赖
uv sync

# 添加新依赖（自动更新requirements.txt和uv.lock）
uv add xxx=version

2. 分支策略
主分支

main：生产环境代码，仅允许通过 PR 合并。

Bash

# 创建特性分支（从dev拉取）
git checkout dev
git pull origin dev
git checkout -b feature/<功能>-<作者名>  # 例如 feature/match-algorithm-optimize
示例：
✅ feature/auto-card-drawing-pq
❌ feature/login（过于模糊）
紧急修复
使用 hotfix/ 前缀分支（如 hotfix/payment-timeout）。

3. 代码提交规范
Bash

# 提交格式
git commit -m "<type>: <description>"

# 示例
git commit -m "feat: 增加自动战斗模块"
git commit -m "fix: 修复技能冷却时间计算错误"
常用类型：

类型	用途
feat	新功能
fix	Bug修复
docs	文档更新
refactor	重构（不改变功能）
chore	构建/依赖调整


Pyenv 环境管理指南
1. 安装 Pyenv
Linux/macOS
Bash

# 安装依赖（Ubuntu示例）
sudo apt update && sudo apt install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

# 通过脚本安装
curl https://pyenv.run | bash

# 添加到Shell配置文件（~/.bashrc 或 ~/.zshrc）
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
exec "$SHELL"  # 重新加载Shell
Windows
使用 pyenv-win：

PowerShell

# 管理员权限运行
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"
& "./install-pyenv-win.ps1"