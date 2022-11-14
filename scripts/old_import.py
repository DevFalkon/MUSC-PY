import urllib.request

with urllib.request.urlopen('https://github.com/DevFalkon/MUSC-PY/releases/tag/Relese') as response:
   html = str(response.read()).split()
   for ind, elem in enumerate(html):
    if elem == 'MUSC-PY':
        if html[ind+1][0] == 'v':
            ver = html[ind+1][1::].split('.')
            print(html[ind], ver)