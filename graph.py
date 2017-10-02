from facepy import GraphAPI
import json
from json2html import *
import webbrowser

try:
    input = raw_input
except NameError:
    pass

graph = GraphAPI('YOUR_ACCESS_TOKEN')

print("Please enter the page-name:")
PageName = input()

search_res = graph.get('search?q=' + PageName + '&type=page&limit=5')

for index, item in enumerate(search_res['data']):
    # The 'data' key of 'search_res' dictionary is a list of dictionaries of 5 pages
    print(index + 1, item['name'])

pno = int(input("Please enter the page no. : "))
pid = search_res['data'][pno - 1]['id']

variable = graph.get(pid + '/posts?fields=comments.limit(5),link,full_picture,message&limit=5')

try:
    del variable['paging']
    for i in range(0, len(variable['data'])):
        del variable['data'][i]['id']
        try:
            del variable['data'][i]['comments']['paging']
            for j in range(0, len(variable['data'][i]['comments']['data'])):
                del variable['data'][i]['comments']['data'][j]['id']
                del variable['data'][i]['comments']['data'][j]['from']['id']
        except:
            pass
        try:
            variable['data'][i][
                'full_picture'] = '<div style="width:500px;height:500px;overflow:scroll"><img style="width:100%;height:auto" src=\"' + \
                                  variable['data'][i]['full_picture'] + '\"></div>'
        except:
            pass
        try:
            variable['data'][i]['link'] = '<a href=\"' + variable['data'][i]['link'] + '\">' + variable['data'][i][
                'message'] + '</a>'
        except:
            variable['data'][i]['link'] = '<a href=\"' + variable['data'][i]['link'] + '\">link</a>'
        try:
            del variable['data'][i]['message']
        except:
            pass
except:
    pass

# Removing 'data'
for i in range(0, len(variable['data'])):
    try:
        variable['data'][i]['comments'] = variable['data'][i]['comments']['data']
    except:
        pass
variable[''] = variable.pop('data')

with open('data.json', 'wb') as outfile:
    json.dump(variable, outfile)

# infoFromJson = json.loads(variable)
table = json2html.convert(json=variable)

htmlfile = table.encode('utf-8')
# print(htmlfile)
f = open('Table.html', 'wb')
f.write(htmlfile)
f.close()

webbrowser.open("Table.html")
