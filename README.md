# ZJU DDNS

Dynamic DNS script for the LAN of Zhejiang University, working with DNSPOD API v3.

为浙江大学局域网设计的动态 DNS 脚本，与 DNSPOD API v3 配合使用。

### Usage

太困了，明天补

### Configuration

#### secret

DNSPOD API 的 secret，请自行在腾讯云后台获取。

#### keyword

脚本用于检索 IPv4 连接的关键词，如果你使用学校的拨号上网工具，这项可以为 `SRun3K专用宽带拨号`，如果你使用 ZJU Connect 等第三方工具，这项应该为 `ZJUVPN` 或你自己设定的 VPN 名称。

具体查看方法为，在终端输入 `ipconfig` 指令，找到某个 `210/222.*.*.*` 的 IPv4 地址，查看其对应的链接名称。如果使用学校的拨号上网工具，这项可能为 `PPP 适配器 SRun3K专用宽带拨号连接`，如果使用 ZJU Connect 工具，这项可能为 `PPP 适配器 ZJUVPN`，只需要从中截取一个能唯一确定连接的关键词填入配置项即可。
