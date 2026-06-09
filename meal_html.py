import requests
import json
import os
import webbrowser
import sys

PROJECT_ID = "meal-steals-app"
API_KEY = "AIzaSyDU3sOn2jgM2qsXVcdtil2e2bJh3O0o7As"
FIRESTORE_URL = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents:runQuery?key={API_KEY}"

HEADERS = {
    "X-Android-Package": "com.mealsteals.app",
    "X-Android-Cert": "22A03BF8A1F71768CDCB475E61101D638A2B2245",
    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 15; Pixel 3 Build/AP4A.241205.013)"
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Live Deal Feed</title>
    <style>
        :root {
            --bg-color: #0f1115;
            --card-bg: #1a1d24;
            --text-main: #e2e8f0;
            --text-muted: #94a3b8;
            --accent: #3b82f6;
            --accent-hover: #2563eb;
            --border: #334155;
            --dodgers: #005A9C;
            --lakers: #552583;
            --kings: #111111;
            --manual: #059669;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            padding: 2rem;
            line-height: 1.5;
        }

        header {
            max-width: 1200px;
            margin: 0 auto 2rem;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            border-bottom: 1px solid var(--border);
            padding-bottom: 1rem;
        }

        h1 { font-size: 2rem; font-weight: 700; letter-spacing: -0.025em; }
        .stats { color: var(--text-muted); font-size: 0.9rem; }

        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 1.5rem;
            max-width: 1200px;
            margin: 0 auto;
        }

        .card {
            background-color: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.5rem;
            display: flex;
            flex-direction: column;
            transition: transform 0.2s ease, border-color 0.2s ease;
        }

        .card:hover {
            transform: translateY(-2px);
            border-color: var(--accent);
        }

        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
        }

        .restaurant { font-weight: 700; font-size: 1.1rem; }

        .badge {
            font-size: 0.75rem;
            font-weight: 600;
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .badge.dodgers { background-color: var(--dodgers); color: white; }
        .badge.lakers { background-color: var(--lakers); color: #FDB927; }
        .badge.kings { background-color: var(--kings); color: #A2AAAD; border: 1px solid #333; }
        .badge.manual { background-color: var(--manual); color: white; }
        .badge.default { background-color: #475569; color: white; }

        .deal-title { font-size: 1.25rem; font-weight: 600; margin-bottom: 0.5rem; color: #fff; }
        .reason { font-size: 0.875rem; color: #cbd5e1; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem; }
        .details { font-size: 0.875rem; color: var(--text-muted); margin-bottom: 1.5rem; flex-grow: 1; }

        .card-footer {
            display: flex;
            justify-content: flex-end;
            padding-top: 1rem;
            border-top: 1px solid var(--border);
        }

        .btn {
            background-color: var(--accent);
            color: white;
            text-decoration: none;
            padding: 0.5rem 1rem;
            border-radius: 6px;
            font-size: 0.875rem;
            font-weight: 500;
            transition: background-color 0.2s;
        }

        .btn:hover { background-color: var(--accent-hover); }
        .expiration { font-size: 0.75rem; color: #ef4444; margin-top: 0.5rem; font-weight: 600;}
    </style>
</head>
<body>
    <header>
        <div>
            <h1>Live Deal Feed</h1>
            <div class="stats" id="last-updated">Status: Rendering...</div>
        </div>
    </header>

    <main class="grid" id="deals-container"></main>

    <script>
        const rawData = INJECT_JSON_HERE;

        function getBadgeClass(team, source) {
            if (source === 'manual') return 'manual';
            if (!team) return 'default';
            const t = team.toLowerCase();
            if (t.includes('dodgers')) return 'dodgers';
            if (t.includes('lakers')) return 'lakers';
            if (t.includes('kings')) return 'kings';
            return 'default';
        }

        function formatDate(isoString) {
            const date = new Date(isoString);
            return date.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit' });
        }

        function renderDeals() {
            const container = document.getElementById('deals-container');
            const activeDeals = rawData.filter(d => new Date(d.validUntil) > new Date());
            
            document.getElementById('last-updated').innerText = `Active Deals: ${activeDeals.length} | Auto-Generated`;

            container.innerHTML = activeDeals.map(deal => `
                <div class="card">
                    <div class="card-header">
                        <span class="restaurant">${deal.restaurant}</span>
                        <span class="badge ${getBadgeClass(deal.team, deal.source)}">${deal.team || deal.source}</span>
                    </div>
                    <h3 class="deal-title">${deal.deal}</h3>
                    <div class="reason">⚡ ${deal.reason}</div>
                    <p class="details">${deal.details}</p>
                    
                    <div class="card-footer">
                        ${deal.promoUrl ? `<a href="${deal.promoUrl}" target="_blank" class="btn">View Promo</a>` : ''}
                    </div>
                    <div class="expiration">Expires: ${formatDate(deal.validUntil)}</div>
                </div>
            `).join('');
        }

        document.addEventListener('DOMContentLoaded', renderDeals);
    </script>
</body>
</html>
"""

def parse_firestore_document(doc):
    parsed_data = {}
    if 'fields' not in doc:
        return parsed_data
    for key, value_dict in doc['fields'].items():
        data_type = list(value_dict.keys())[0]
        parsed_data[key] = value_dict[data_type]
    return parsed_data

def get_offers(city="Los Angeles"):
    print(f"[-] Fetching live offers for {city} from Firebase...")
    
    payload = {
        "structuredQuery": {
            "from": [{"collectionId": "offers"}],
            "where": {
                "fieldFilter": {
                    "field": {"fieldPath": "city"},
                    "op": "EQUAL",
                    "value": {"stringValue": city}
                }
            }
        }
    }
    
    response = requests.post(FIRESTORE_URL, headers=HEADERS, json=payload)
    
    if response.status_code == 200:
        results = response.json()
        documents = [parse_firestore_document(res['document']) for res in results if 'document' in res]
        print(f"[+] Successfully extracted {len(documents)} offers.")
        return documents
    else:
        print(f"[!] Query failed (Status {response.status_code}): {response.text}")
        return []

def generate_and_open_html(deals, filename="deals_dashboard.html"):
    print("[-] Generating HTML dashboard...")
    
    # Inject the JSON payload directly into the JavaScript variable
    final_html = HTML_TEMPLATE.replace("INJECT_JSON_HERE", json.dumps(deals))
    
    file_path = os.path.abspath(filename)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(final_html)
        
    print(f"[+] Dashboard saved to: {file_path}")
    
    if "CI" not in os.environ:
        print("[-] Opening in web browser...")
        webbrowser.open('file://' + file_path)
    else:
        print("[-] CI environment detected. Skipping browser opening.")

if __name__ == "__main__":
    offers = get_offers()
    if offers:
        filename = sys.argv[1] if len(sys.argv) > 1 else "deals_dashboard.html"
        generate_and_open_html(offers, filename)