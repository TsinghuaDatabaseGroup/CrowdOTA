import logging
import json
logging.basicConfig(level=logging.DEBUG)
from django.shortcuts import redirect,render
from django.utils import timezone


from plat.models import Assignment, TaskInfo , Submission,HitGroupInfo, WorkerInfo
from getTasks import getTasks
from completeTasks import completeTasks
from page import choicesPage,singleChoicePage,multiChoicePage,fillPage,collectPage
from page import welChoicesPage,welCollectPage,welFillPage,welMultiChoicePage,welSingleChoicePage

def welcome(taskType,hitGroupId,request,title,description):
    task =TaskInfo.objects.filter(hitGroupId=hitGroupId)[0:2]
    if (taskType == 'SC'):
        return welSingleChoicePage(request, task, title, description)
    if (taskType == 'MC'):
        return welMultiChoicePage(request, task, title, description)
    if (taskType == 'CT'):
        return welCollectPage(request,task,title,description)
    if (taskType == 'FL'):
        return welFillPage(request,task,title,description)


def quesPage(request,questions,workerId,assignmentId,hitGroupId,hitId,cNum,taskType):
    if (taskType == 'SC'):
        return singleChoicePage(request, questions, workerId, assignmentId, hitGroupId, hitId)
    if (taskType == 'MC'):
        return multiChoicePage(request, questions, workerId, assignmentId, hitGroupId, hitId)
    if (taskType == 'CT'):
        return collectPage(request,questions,workerId,assignmentId,hitGroupId,hitId)
    if (taskType == 'FL'):
        return fillPage(request,questions,workerId,assignmentId,hitGroupId,hitId)

def question(request,hitGroupId):
    logging.debug(request.GET)
    logging.debug(hitGroupId)
    assignmentId = request.GET.get('assignmentId', 'NO_ASSIGNMENT_ID')
    hitId = request.GET.get('hitId', 'NO_hit_ID')
    # turk_submit_to = request.GET['turkSubmitTo']
    workerId = request.GET.get('workerId', 'NO_WORKER_ID')
    worker, created  = WorkerInfo.objects.get_or_create(workerId = workerId)
    if (created):
        worker.quality = 1
        worker.save()
    if assignmentId == 'ASSIGNMENT_ID_NOT_AVAILABLE':
        projectInfo = HitGroupInfo.objects.get(hitGroupId=hitGroupId);
        return welcome(taskType=projectInfo.taskType,hitGroupId= hitGroupId,request= request,title = projectInfo.title,description = projectInfo.description)
    else:
        logging.debug(workerId)
        logging.debug(hitId)
        projectInfo = HitGroupInfo.objects.get(hitGroupId=hitGroupId);
        logging.debug("getQuestion")
        questions,accept = getTasks(workerId, hitGroupId, hitId, projectInfo.questionsPerHit)
        logging.debug("asn")
        ass,created = Assignment.objects.get_or_create(assignmentId = assignmentId,workerId = workerId,hitId = hitId)
        if (ass.arriveTime is None):
            ass.accept = accept
            ass.arriveTime = timezone.now()
            ass.save()
        else:
            print "arriveTime:",timezone.now()
        logging.debug("ret")
        return quesPage(request,questions=questions,workerId=workerId,assignmentId=assignmentId,hitGroupId=hitGroupId,hitId=hitId,cNum= projectInfo.cNum,taskType=projectInfo.taskType)

def test(request,hitGroupId):
    return render(request, 'test.html',
                          {
                            'submit':'/question/'+hitGroupId+'/'
                          }
                  )


def submit(request):
    assignmentId = request.POST.get('assignmentId', 'NO_ASSIGNMENT_ID')
    workerId = request.POST.get('workerId', 'NO_WOKRER_ID')
    hitId = request.POST.get('hitId', '')
    hitGroupId = request.POST.get('hitGroupId', '')

    url = "https://workersandbox.mturk.com/mturk/externalSubmit"
    #else:
        #url = "https://www.mturk.com/mturk/externalSubmit"
    #return
    asn = Assignment.objects.get(assignmentId=assignmentId)
    asn.finishTime = timezone.now()
    asn.save()
    postDict = dict(request.POST.iterlists())
    #print "####",postDict

    for key in postDict:
        try:
            taskId = key
            answer = postDict[taskId]
            #print taskId," ",answer
            answerC = int(answer[0])-1
            if (len(taskId)>20):
                print "submit : ",taskId,' ',type(answerC)
                Submission.objects.create(workerId=workerId,taskId = taskId, result=json.dumps(answer), hitId = hitId,hitGroupId = hitGroupId)
                task = TaskInfo.objects.get(taskId = taskId)
                if (HitGroupInfo.objects.get(hitGroupId=hitGroupId).taskType=='CIC' or HitGroupInfo.objects.get(hitGroupId=hitGroupId).taskType=='SLB'):
                    dis = json.loads(task.distribution)
                    quality = WorkerInfo.objects.get(workerId=workerId).quality
                    delta = dis[answerC]*quality+(1.0-dis[answerC])*(1.0-quality)/(len(dis)-1)
                    for i in range(len(dis)):
                        if i!=answerC:
                            dis[i] = dis[i]*(1.0-quality)/(len(dis)-1)/delta
                        else:
                            dis[i] = dis[i]*quality/delta
                    task.distribution = json.dumps(dis)
                task.answered = task.answered + 1
                task.save()
        except ValueError as e:
            pass

    hitGroup = HitGroupInfo.objects.get(hitGroupId= hitGroupId)
    hitGroup.hitRemains = hitGroup.hitRemains -1
    hitGroup.save()
    if (hitGroup.hitRemains == 0):
        completeTasks(hitGroupId)
    logging.debug(url + "?assignmentId=" + assignmentId + "&foo=bar")
    #return redirect(url + "?assignmentId=" + assignmentId + "&foo=bar")
    return redirect("http://127.0.0.1:8000/test/"+hitGroupId+"/")
