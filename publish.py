from __future__ import print_function
__author__ = 'yxfish13'
from boto.mturk.connection import MTurkConnection
from boto.mturk.question import *
import uuid
import json

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "amtplat.settings")

import django
django.setup()

from plat.models import HitInfo,HitGroupInfo
from plat.models import TaskInfo

def loadJson(fileName):
    import json
    config = {}
    try:
        filejson = file(fileName)
        config = json.load(filejson)
    except:
        print("load Json ERROR")
        exit(0)
    return config
def connect(pubCon):
    if pubCon["sandbox"]:
        HOST="mechanicalturk.sandbox.amazonaws.com"
    else:
        HOST="mechanicalturk.amazonaws.com"
        #Host = "1"
    mtc = MTurkConnection(aws_access_key_id=pubCon["AWS_ACCESS_ID"], aws_secret_access_key=pubCon["AWS_SECRET_KEY"], host=HOST)
    return mtc
if __name__=="__main__":
    pubCon = loadJson("config.json")
    if ( not pubCon["test"]):
        con = connect(pubCon)

    hitGroupId = str(uuid.uuid1())

    import utils

    HitGroup = HitGroupInfo(hitGroupId= hitGroupId,title=pubCon["title"],description= pubCon["description"],questionsPerHit=pubCon["questionsPerHit"],taskFile=pubCon["taskFile"],taskType=pubCon["taskType"],cNum=pubCon["cNum"],hitRemains=((pubCon["questionsTotal"]-1)/pubCon["questionsPerHit"]+1)*pubCon["workerLimit"])
    HitGroup.save()
    questions = utils.quesLoader(pubCon["taskFile"]);
    if (pubCon["taskType"]=='CLT'):
        for iter in range(pubCon["questionsPerHit"]):
            print(iter," ",questions[0]["content"])
            TaskInfo.objects.create(hitGroupId = hitGroupId, taskContent = questions[0]["content"],answered = 0)
    else:
        for question in questions:
            #try:
                task,created = TaskInfo.objects.get_or_create (hitGroupId = hitGroupId, taskDescription = question["description"],taskLabels= question["labels"],answered = 0)
                if (pubCon["taskType"]=='CIC' or pubCon["taskType"]=='SLB'):
                    task.distribution = json.dumps([1.0/pubCon['cNum']]*pubCon['cNum'])
                    task.save()
                elif (pubCon["taskType"]=='MLB'):
                    task.distribution = json.dumps([1.0/2]*pubCon['cNum'])
                    task.save()
                else:
                    task.distribution = json.dumps([]);
                    task.save()
            #except:
            #   print("test:",question["content"])
    #exit(0)
    for i in range((pubCon["questionsTotal"]-1)/pubCon["questionsPerHit"]+1):
        print ((pubCon["questionsTotal"]-1)/pubCon["questionsPerHit"]+1)
        if (not pubCon["test"]):
            hit, = con.create_hit(
            question = ExternalQuestion(pubCon["questionUrl"]+'/'+hitGroupId+"/", 800),
            max_assignments = pubCon["workerLimit"],
            title = pubCon["title"],
            description = pubCon["description"],
            keywords = pubCon["keywords"],
            lifetime = pubCon["lifetime"],
            duration = pubCon["duration"],
            approval_delay = pubCon["approval_delay"],
            reward = pubCon["reward"])
            Hit = HitInfo(hitGroupId= hitGroupId, hitId=hit.HITId)
            Hit.save()
            print(hit.HITId)
        else:
            Hit = HitInfo(hitGroupId= hitGroupId, hitId=uuid.uuid4())
            Hit.save()

    print("hitGroup :"+str(hitGroupId))
