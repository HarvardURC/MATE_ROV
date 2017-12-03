ptables=/sbin/iptables
    iptables --flush -t nat
    iptables --table nat --append POSTROUTING --out-interface wlp3s0 -j MASQUERADE
    iptables --append FORWARD --in-interface enp0s25 -j ACCEPT
    echo 1 > /proc/sys/net/ipv4/ip_forward
