from Inference import EM
from plat.models import Submission,TaskInfo,WorkerInfo,HitInfo
def completeTasks(workerId,hitId):
    hitGroupId = HitInfo.objects.get(hitId= hitId).hitGroupId
    res = Submission.objects.filter(hitGroupId=hitGroupId)
    resList = []
    workerQualityDict={}
    for x in res:
        resList.append([x.taskId,x.workerId,x.result])
        workerQualityDict[x.workerId] = WorkerInfo.objects.get(workerId=x.workerId).quality

    res = EM.infer(resList, workerQualityDict)
    for x in res:
        task = TaskInfo.objects.get(taskId=x)
        task.result=res[x]
        task.save()
    for workerId in workerQualityDict:
        worker = WorkerInfo.objects.get(workerId= workerId)
        worker.quality = workerQualityDict[workerId]
        worker.save()




