import json
import x8

data=[]
zero=1
while zero<=1000:
    try:
	    for d in x8.analysis_page(zero):
		    data.append(d)
	    print(zero)
	    zero+=1
    except:
        with open('data.json','w')as file:
        	file.write(json.dumps(data,ensure_ascii=False))
with open('data.json','w')as file:
	file.write(json.dumps(data,ensure_ascii=False))
