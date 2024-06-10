## pyddns

--- 

DDNS触发程序, 由systemd定时器调用

默认间隔5分钟扫描一次ip并与本地缓存对比,对比结果不相等触发通知更新

--- 
需要修改间隔请使用如下命令插入内容

### 编辑

```shell
systemctl edit ddns.timer
```

### 内容

```text
[Timer]
OnUnitActiveSec=5m
```

---

### 支持插件模式编写通知程序

```ini

[DEFAULT]
notifier = dnspod

[ddns]
domain = www.aaa.com


```