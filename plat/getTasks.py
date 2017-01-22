from assignment import maxExpBenefit
from models import Submission, TaskInfo


def getTasks(workerId, hitGroupId, hitId, quesNum):
    submittedId = [x['taskId'] for x in Submission.objects.filter(workerId = workerId,hitGroupId = hitGroupId).values("taskId")]
    print submittedId
    alter = TaskInfo.objects.filter(hitGroupId = hitGroupId).exclude(taskId__in=submittedId)
    print alter.count()
    if (alter.count()==0):
        return [],False
    return maxExpBenefit.assign(alter, quesNum, workerId), True

