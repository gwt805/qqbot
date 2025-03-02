# 必读
  当前仅在沙箱环境中运行，使用 webhook 方式发送消息；研究不易，觉得有用的话，点点 star 和 fork

# 免费白嫖搭建教程
 0. [更多教程请点我](https://blog.csdn.net/qq_42889888/article/details/145925852)

 1. 首先要有一个自己创建的QQ群(需要小于20人)

 2. 在 [QQ开放平台](https://q.qq.com/#/) 注册一个机器人，拿到 appid 和 secret

 3. 在 [QQ开放平台](https://q.qq.com/qqbot/#/developer/sandbox) 上配置沙箱环境(QQ群ID | 消息列表)

 4. app.py 是一个 flask 项目，所以可以部署在 [pythonanywhere](https://pythonanywhere.com) 上 ，部署教程 [点我查看](https://www.cnblogs.com/gwt805/p/16905376.html)

 5. 由于 pythonanywhere 无法访问 openapi， 所以这里要用到 [cloudfare](http://www.cloudflare-cn.com/) 来做代理转发

 6. 注册好 cloudfare 账号后， 分别创建两个 worker.js 将 目录 workerjs 下的两个文件内容分别复制过去，拿到两个链接

 7. 将函数 get_access_token 中 url 的 qqbot-token.weilong.workers.dev 部分 替换为你的链接

 8. 将函数 send_private_message 和 send_group_message 中 url 的 qqbot-msg.weilong.workers.dev 替换为你的链接

 9. 重新运行 pythonanywhere 项目

 10. 在 [QQ开放平台](https://q.qq.com/qqbot/#/developer/webhook-setting) 上设置回调地址，就是的 pythonanywhere 链接，username.pythonanywhere.com/qqbot 这里的username 替换为自己的

 11. 在 [QQ开放平台](https://q.qq.com/qqbot/#/developer/developer-setting) 上设置 IP白名单， 35.173.69.207 和 18.205.21.37 和 103.252.115.53
  
     11.1 这几个ip 是 pythonanywhere.com 和 your_username.pythonanywhere.com(在终端获取) 和 cloudfare
     
     11.2 该步骤等测试后，如果消息发不出来，再设置，因为一旦设置，就删不掉了(至少保留1个)

 13. 然后在 QQ群里 @机器人+消息 做测试，如果机器人有消息发出，则部署成功

# 其他
  - 当前 app.py 文件中仅为文本类型，其他类型的消息需自己完善，markdown 格式需要自己申请
  - pythonanywhere 有很多requests访问不了的，所以推荐使用 [LinuxONE](https://linuxone.cloud.marist.edu/#/login) + 免费域名(eu.org等) + caddy 来搭建
