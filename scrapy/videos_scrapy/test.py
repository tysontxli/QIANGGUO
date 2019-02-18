import json
import requests

res = requests.get("https://www.xuexi.cn/4426aa87b0b64ac671c96379a3a8bd26/datadb086044562a57b441c24f2af1c8e101.js")

json.loads(res.text.lstrip("globalCache = ").rstrip(";"))