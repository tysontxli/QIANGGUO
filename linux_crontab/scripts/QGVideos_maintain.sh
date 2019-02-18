baseLogdir=/root/QIANGGUO/QIANGGUO/QGVideos_maintain_log
everydayLog=$baseLogdir/$(date +%F)/
[ ! -d "$everydayLog" ] && mkdir -p $everydayLog
#判断每日的日志文件存放的目录是否存在

nowtime=`date +%F_%H:%M`
#多条程序的执行时间是有时间差的，为了避免出现push命令执行时已经到了第二分钟，程序需要一个确定的时间

python /root/QIANGGUO/QIANGGUO/scrapy/videos_scrapy.py >$everydayLog/${nowtime}.log 2>&1
#创建每次维护的记录

git init
git add -f $everydayLog/${nowtime}.log
git commit -m "这是${nowtime}的视频（或图片）维护日志，由crontab程序自动创建"
git remote add origin git@github.com:chinaltx/QIANGGUO.git
git pull origin master
git push -u origin master
#把每次维护的记录push到github
