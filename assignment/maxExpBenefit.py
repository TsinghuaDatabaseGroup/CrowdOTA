import random
from plat.models import WorkerInfo
from utils import entropy
import json
import copy
def assign(questions,quesNum,workId):
    quality = WorkerInfo.objects.get(workerId= workId).quality
    etpList = []
    for x in range(len(questions)):
        dis = json.loads(questions[x].distribution)
        etp = entropy(dis)
        l = len(dis)
        sample = random.random()
        for t in range(l):
            delta = dis[t] * quality + (1.0 - dis[t]) *(1-quality)/(l-1)
            sample = sample - dis[t]
            disTemp =[]
            if (sample < 1e-7):
                for j in range(l):
                    if (t!=j):
                        disTemp.append(dis[j]*(1.0-quality)/(l-1)/delta)
                    else:
                        disTemp.append(dis[j]*quality/delta)
                etp = etp- entropy(disTemp)
                break
        etpList.append((x,etp))
    etpList = sorted(etpList,key=lambda x:x[1],reverse=True)
    res = [questions[etpList[x][0]] for x in range(quesNum)]
    return res
