import urllib.request, json, base64

base = 'http://localhost:9000/api/issues/search?projectKeys=BenchmarkJava&types=VULNERABILITY&ps=500&p='
creds = base64.b64encode(b'admin:Admin@123456789').decode('ascii')
all_issues = []
page = 1

while True:
    try:
        url = base + str(page)
        req = urllib.request.Request(url)
        req.add_header('Authorization', 'Basic ' + creds)
        with urllib.request.urlopen(req) as r:
            data = json.loads(r.read())
        issues = data['issues']
        if not issues:
            break
        all_issues.extend(issues)
        print(f'Page {page}: {len(issues)} issues, total so far: {len(all_issues)}')
        total = data['paging']['total']
        if len(all_issues) >= total or len(all_issues) >= 10000:
            break
        page += 1
    except Exception as e:
        print(f'Stopped at page {page}: {e}')
        break

with open(r'C:\SAST-Benchmark\results\sonar_issues_all.json', 'w') as f:
    json.dump({'issues': all_issues, 'total': len(all_issues)}, f)
print('Done. Total issues saved:', len(all_issues))