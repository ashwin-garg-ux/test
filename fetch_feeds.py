import json
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

# Brand handles to track
BRANDS = [
    {"name": "Tide", "ig": "tidelaundry", "tiktok": "tidelaundry"},
    {"name": "Old Spice", "ig": "oldspice", "tiktok": "oldspice"},
    {"name": "Olay", "ig": "olay", "tiktok": "olay"},
    {"name": "Dawn", "ig": "dawndishwash", "tiktok": "dawndishwash"},
    {"name": "Pampers", "ig": "pampersus", "tiktok": "pampers"},
    {"name": "Pantene", "ig": "pantene", "tiktok": "pantene"},
    {"name": "Gillette", "ig": "gillette", "tiktok": "gillette"},
    {"name": "Febreze", "ig": "febreze", "tiktok": "febreze"},
    {"name": "Crest", "ig": "crest", "tiktok": "crest"},
    {"name": "Charmin", "ig": "charmin", "tiktok": "charmin"},
    {"name": "Swiffer", "ig": "swiffer", "tiktok": "swiffer"},
    {"name": "Gain", "ig": "ilovegain", "tiktok": "gain"},
    {"name": "Always", "ig": "always_brand", "tiktok": "always_brand"},
    {"name": "Head & Shoulders", "ig": "headandshoulders", "tiktok": "headandshoulders"},
    {"name": "Oral-B", "ig": "oralb", "tiktok": "oralb"},
    {"name": "Bounty", "ig": "bountypapertowels", "tiktok": "bounty"},
    {"name": "Braun", "ig": "braun_global", "tiktok": "braun"},
    {"name": "Venus", "ig": "gillettevenus", "tiktok": "gillettevenus"},
    {"name": "Aussie", "ig": "aussiehair", "tiktok": "aussiehair"},
    {"name": "Secret", "ig": "secretdeodorant", "tiktok": "secretdeodorant"}
]

posts = []
FALLBACK_IMG = "https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=800&auto=format&fit=crop&q=60"

for b in BRANDS:
    try:
        query = urllib.parse.quote(f"{b['name']} (TikTok OR Instagram OR campaign)")
        url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
        
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            xml_data = resp.read()
            root = ET.fromstring(xml_data)
            
            for item in root.findall('.//item')[:2]:
                title = item.find('title').text
                pub_date = item.find('pubDate').text
                
                posts.append({
                    "author": f"@{b['ig']}",
                    "platform": "TikTok/IG Spotlight",
                    "text": title,
                    "image": FALLBACK_IMG,
                    "date": pub_date[:16] if pub_date else "Recent"
                })
    except Exception as e:
        print(f"Error fetching {b['name']}: {e}")

with open("feed.json", "w") as f:
    json.dump(posts, f, indent=2)

print(f"Successfully compiled {len(posts)} posts into feed.json")
