
cmd = {
    "hostname_s": "hostname -s",
    "hostname_i": "hostname -I",
    "vCPU": "grep -c ^processor /proc/cpuinfo",
    "memory": "sudo dmidecode -t memory | grep 'Maximum Capacity' | cut -d':' -f2 | awk '{print $1}'",
    "disk": "sudo fdisk -l | grep 'Disk /dev/vda' | awk '{print $5}'",
    "outbound": "curl --connect-timeout 5 -s -o /dev/null -I -w '%{http_code}\n' https://www.google.com/",
    "process": "sudo pgrep -c {}",
    "port": "ss -lt src :{} | grep LISTEN | wc -l"
}