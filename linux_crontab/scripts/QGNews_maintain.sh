baseLogdir=/root/QIANGGUO/QIANGGUO/QGNews_maintain_log
everydayLog=$baseLogdir/$(date +%F)/
[ ! -d "$everydayLog" ] && mkdir -p $everydayLog
#判断每日的日志文件存放的目录是否存在

echo $everydayLog
python /root/QIANGGUO/QIANGGUO/scrapy/news_scrapy.py >$everydayLog/$(date +%F_%H:%M).log 2>&1
#创建每次维护的记录

git init
git add -f $everydayLog/$(date +%F_%H:%M).log
git commit -m "这是$(date +%F_%H:%M)的维护日志，由crontab程序自动创建"
git remote add origin git@github.com:chinaltx/QIANGGUO.git
git pull origin master
git push -u origin master

  
#把每次维护的记录push到github
