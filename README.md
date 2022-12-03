# moUSDT
一个使用Flask开发的USDT收款平台，通过HTTP接口进行订单的发起及回调，自带网页管理后台管理及查询订单、钱包、及链上交易


# moUSDT目前
* 数据库使用文件数据库sqlite，方便搭建
* 支持在规定时间内`多次`小额转账完成订单
* 订单支持`任意金额`
* 钱包`本地`随机生成，降低泄露风险
* 批量生成钱包,批量导出钱包，手动导入钱包，钱包优先级设置
* 支持TRON链的USDT，使用trongrid查询链上交易
* 自带了易支付规则的接口


# 有问题反馈
在使用中有任何问题，欢迎反馈给我，可以用以下联系方式跟我交流

* tg: [@nulllllllll](https://t.me/nulllllllll)

# 感激
灵感来自以下的项目

* [epusdt](https://github.com/assimon/epusdt)
