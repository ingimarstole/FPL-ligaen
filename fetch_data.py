import json, urllib.request, re, sys

LEAGUE_ID = 1924829
TOTAL_GW  = 38

def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())

print("Henter bootstrap...")
boot = fetch("https://fantasy.premierleague.com/api/bootstrap-static/")
events = boot["events"]
current_gw = next((e["id"] for e in events if e["is_current"]), None)
if current_gw is None:
    current_gw = max(e["id"] for e in events if e["finished"])

print(f"Gjeldende GW: {current_gw}")

print("Henter ligastilling...")
league = fetch(f"https://fantasy.premierleague.com/api/leagues-classic/{LEAGUE_ID}/standings/")
entries = league["standings"]["results"]
league_name = league["league"]["name"]

print(f"Henter historikk for {len(entries)} spillere...")
players = []
for e in entries:
    hist = fetch(f"https://fantasy.premierleague.com/api/entry/{e['entry']}/history/")
    gw_pts = [r["points"] for r in hist["current"]]
    players.append({
        "name":      e["player_name"],
        "team":      e["entry_name"],
        "rank":      e["rank"],
        "lastRank":  e["last_rank"],
        "total":     e["total"],
        "eventPts":  e["event_total"],
        "gw":        gw_pts,
    })

data = {
    "leagueName": league_name,
    "currentGW":  current_gw,
    "totalGW":    TOTAL_GW,
    "players":    players,
}

with open("data.json", "w") as f:
    json.dump(data, f)

print("data.json skrevet OK")
