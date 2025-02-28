# 必读
  当前仅在沙箱环境中运行，使用 webhook 方式发送消息；研究不易，觉得有用的话，点点 star 和 fork

# 免费白嫖搭建教程
 1. app.py 是一个 flask 项目，所以可以部署在 [pythonanywhere](https://pythonanywhere.com) 上 ，部署教程 [点我查看](https://www.cnblogs.com/gwt805/p/16905376.html)

 2. 由于 pythonanywhere 无法访问 openapi， 所以这里要用到 [cloudfare](http://www.cloudflare-cn.com/) 来做代理转发

 3. 注册好 cloudfare 账号后， 分别创建两个 worker.js 将 目录 workerjs 下的两个文件内容分别复制过去，拿到两个链接
  
 4. 将函数 get_access_token 中 url 的 qqbot-token.weilong.workers.dev 部分 替换为你的链接
  
 5. 将函数 send_private_message 和 send_group_message 中 url 的 qqbot-msg.weilong.workers.dev 替换为你的链接
  
 6. 重新运行 pythonanywhere 项目

# 其他
  当前 app.py 文件中仅为文本类型，其他类型的消息需自己完善
