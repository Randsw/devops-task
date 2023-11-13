# Show top 15 ip addresse with "process" in uri
awk -F\" '($2 ~ "process"){print $1}' nginx_access.log | awk '{print $1}' | sort | uniq -c | sort -rn | head -n 15 