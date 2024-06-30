# Set up VPN to coexist with office VPN

* Host: MacOS
* CPU arch: aarch64/arm64
* Intranet VPN: Cisco Anyconnect to office

Download mihomo CLI utility here: https://github.com/MetaCubeX/mihomo/releases

Install Proxy SwitchyOmega on host's chrome browser: https://chromewebstore.google.com/detail/proxy-switchyomega/padekgcemlokbadohgkifijomclgjgif?hl=en

Configure the proxy to use socks v5 on localhost:7891.

Choose one of the following:

### Socks proxy on MacOS

- Download and extract mihomo-darwin-arm64 on MacOS
- Get the config.yaml (01701802-b732-4518-86ff-f3903fdbb906) from paid services and put it to `~/.config/mihomo/config.yaml`
- Start the mihomo process (must override security settings)


### Socks proxy on office desktop

- Connect to company intranet.
- Install mihomo-linux-amd64 on office destop with config.yaml from paid services (same as above)
- Create ssh port forwarding:
```bash
ssh -N -L 7891:localhost:7891 OFFICE_DESKTOP_IP
```

### Socks proxy in virtual machine

- Download VMware Fusion for MacOS
- Download Ubuntu 22.04 ARM ISO and install it as a guest OS
- Install mihomo-linux-arm64 on the guest OS with config.yaml from paid services (same as above)
- (There is no Clash Verge for linux arm64)
  
1. Install chromium-browser and use it inside the guest OS
   (There is no prebuilt Chrome browser for linux arm64), or

2. Create ssh port forwarding:
```bash
ssh -N -L 7891:localhost:7891 GUEST_VM_IP
```

### Socks proxy in docker container

- Install docker desktop for MacOS
- docker pull ubuntu:22.04
- Some one-time setup inside the docker container and commit the image as `ubuntu22-yc`
  - Install openssh-server
  - Download mihome-linux-arm64 on the container with config.yaml from paid services (same as above)
  - ...

On MacOS:
```bash
docker run -itd --user yangchunluo --name ubuntu22 -p 8022:22 ubuntu22-yc
docker exec -it ubuntu22 /bin/bash
```
In container:
```bash
sudo service ssh start
mihomo
```
On MacOS:
```bash
ssh -N -L 7891:localhost:7891 localhost -p 8022
```

### Misc:

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
