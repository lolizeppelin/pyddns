# 可以探测外网IP的API

### http://pv.sohu.com/cityjson?ie=utf-8

### https://www.juhe.cn/docs/api/id/1

# 获取国内ip

### http://www.ipdeny.com/ipblocks/data/countries/cn.zone

---

# 代理

```text
# noproxy.zone 屏蔽代理
10.0.0.0/8
127.0.0.0/8
172.16.0.0/12
192.168.0.0/16
169.254.0.0/16
240.0.0.0/4
107.148.250.180/32
```

```text
# proxy.zone  强制代理
111.230.82.224/24
```

## firewall

```shell
#ipset destroy china

# Create the ipset list
#ipset -N china hash:net

firewall-cmd --permanent --ipset=china --remove-entries-from-file=cn.zone
firewall-cmd --permanent --delete-ipset=china

# remove any old list that might exist from previous runs of this script
rm cn.zone

# Pull the latest IP set for China
wget -P . http://www.ipdeny.com/ipblocks/data/countries/cn.zone

# Add each IP address from the downloaded list into the ipset 'china'
#for i in $(cat ./cn.zone ); do ipset -A china $i; done

firewall-cmd --permanent --new-ipset=china --type=hash:net
firewall-cmd --permanent --new-ipset=proxy --type=hash:net
firewall-cmd --permanent --new-ipset=noproxy --type=hash:net


firewall-cmd --permanent --ipset=proxy --add-entries-from-file=proxy.zone
firewall-cmd --permanent --ipset=noproxy --add-entries-from-file=noproxy.zone
firewall-cmd --permanent --ipset=china --add-entries-from-file=cn.zone

```

```text
Firewall 能将不同的网络连接归类到不同的信任级别，Zone 提供了以下几个级别
drop: 丢弃所有进入的包，而不给出任何响应
block: 拒绝所有外部发起的连接，允许内部发起的连接
public: 允许指定的进入连接
external: 同上，对伪装的进入连接，一般用于路由转发
dmz: 允许受限制的进入连接
work: 允许受信任的计算机被限制的进入连接，类似 workgroup
home: 同上，类似 homegroup
internal: 同上，范围针对所有互联网用户
trusted: 信任所有连接

```

```shell

firewall-cmd --zone=public --add-forward-port=port=22:proto=tcp:toport=2055:toaddr=192.168.1.100
firewall-cmd --zone=external --add-forward-port=port=7901:proto=tcp:toport=22:toaddr=10.10.0.101

```

## Proxy

```shell

export http_proxy=http://192.168.250.1:1081/
export https_proxy=http://192.168.250.1:1081/
export MAVEN_OPTS="-DsocksProxyHost=192.168.250.1 -DsocksProxyPort=1080"


```



