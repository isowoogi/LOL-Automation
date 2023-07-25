@echo off
IF EXIST "LOL-Automation" (
  cd LOL-automate-youtube
  git add .> log.txt 2>&1
  git commit -m "updated" > log.txt 2>&1
  git push > log.txt 2>&1
  git pull > log.txt 2>&1
) ELSE (    
    echo "== Installing set up=="
  git clone https://github.com/isowoogi/LOL-Automation.git > log.txt 2>&1
  cd LOL-Automation
)
if not exist venv (
    echo "    * Creating environment=="
    python -m venv venv
)
call venv\Scripts\activate
git restore .> log.txt 2>&1
git pull> log.txt 2>&1
@echo off
pip install -r requirements.txt > log.txt 2>&1

call python video_maker/main.py


