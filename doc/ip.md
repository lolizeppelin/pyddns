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

## Proxy

```shell

export http_proxy=http://192.168.250.1:1081/
export https_proxy=http://192.168.250.1:1081/
export MAVEN_OPTS="-DsocksProxyHost=192.168.250.1 -DsocksProxyPort=1080"


```