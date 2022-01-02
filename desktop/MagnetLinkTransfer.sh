test -z $1 && echo "need magnet link!" && exit
LINK="$1"
curl -X POST 192.168.1.10:8000/automommy/transmission/fetch/ -H "Content-Type: application/json" -d "{\"torrent\": \"${LINK}\"}"
