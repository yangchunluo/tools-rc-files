* Host: MacOS
* VPN: Cisco Anyconnect to office
* Guest: Ubuntu 22.04

### Socks proxy in virtual machine

ssh -N -L 7891:localhost:7891 u22vm


### Socks proxy in docker container

Setups:

clash/mihomo

docker cp ...
cp 01701802-b732-4518-86ff-f3903fdbb906 ~/.config/mihomo/config.yaml

Optionally install [proxychains](https://github.com/shadowsocks/shadowsocks/wiki/Using-Shadowsocks-with-Command-Line-Tools)

```bash
sudo apt install proxychains
cat <<EOF > ~/.proxychains/proxychains.conf
strict_chain
proxy_dns 
remote_dns_subnet 224
tcp_read_time_out 15000
tcp_connect_time_out 8000
localnet 127.0.0.0/255.0.0.0
quiet_mode

[ProxyList]
socks5  127.0.0.1 7891
EOF
```

proxychains wget --spider https://www.google.com

sudo apt install openssh-server


docker run -itd --user yangchunluo --name ubuntu22 -p 8022:22 ubuntu22-yc
docker exec -it ubuntu22 /bin/bash
sudo service ssh start
mihomo

from macos:
ssh -N -L 7891:localhost:7891 localhost -p 8022
