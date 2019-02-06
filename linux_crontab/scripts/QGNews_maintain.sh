baseLogdir=/root/QIANGGUO/QIANGGUO/QGNews_maintain_log
everydayLog=$baseLogdir/$(date +%F)/
[ ! -d "$everydayLog" ] && mkdir -p $everydayLog
#判断每日的日志文件存放的目录是否存在
echo $everydayLog
python /root/QIANGGUO/QIANGGUO/scrapy/news_scrapy.py >$everydayLog/$(date +%F_%H:%M).log 2>&1
