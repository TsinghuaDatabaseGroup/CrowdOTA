from django.shortcuts import render
import json

def choicesPage(request,questions,workerId,assignmentId,hitGroupId,hitId):
    print questions[0].taskDescription
    cNum = len(json.loads(questions[0].taskDescription))
    que = []
    for x in questions:
        dic = {"content":x.taskContent}
        choiceslist = []
        choices = json.loads(x.taskDescription)
        for index in range(len(choices)):
            choiceslist.append({"key":index,"value":choices[index]})
        dic ["choices"] = choiceslist
        dic["id"] = x.taskId
        que.append(dic)
    return render(request, 'choices.html', {
        'questions': que,
        'workerId' : workerId,
        'assignmentId' : assignmentId,
        'hitId' : hitId,
        'cicCount' : cNum,
        'hitGroupId' : hitGroupId,
    }
                  )
def singleChoicePage(request, questions, workerId, assignmentId, hitGroupId, hitId):
    print questions[0].taskLabels
    cNum = len(json.loads(questions[0].taskLabels)["choices"])
    que = []
    for x in questions:
        dic = {"content":x.taskDescription}
        choiceslist = []
        choices = json.loads(x.taskLabels)["choices"]
        for index in range(len(choices)):
            choiceslist.append({"key":index,"value":choices[index]})
        dic ["choices"] = choiceslist
        dic["id"] = x.taskId
        dic["img"] = json.loads(x.taskLabels)["img"]
        que.append(dic)
    return render(request, 'singleChoice.html',
                  {
                      'questions': que,
                      'workerId' : workerId,
                      'assignmentId' : assignmentId,
                      'hitId' : hitId,
                      'cicCount' : cNum,
                      'hitGroupId' : hitGroupId,
                  }
                  )
def multiChoicePage(request, questions, workerId, assignmentId, hitGroupId, hitId):
    print questions[0].taskDescription
    cNum = len(json.loads(questions[0].taskDescription)["choices"])
    que = []
    for x in questions:
        dic = {"content":x.taskContent}
        choiceslist = []
        choices = json.loads(x.taskDescription)["choices"]
        for index in range(len(choices)):
            choiceslist.append({"key":index,"value":choices[index]})
        dic ["choices"] = choiceslist
        dic["id"] = x.taskId
        dic["img"] = json.loads(x.taskDescription)["img"]
        que.append(dic)
    return render(request, 'multiChoice.html',
                  {
                      'questions': que,
                      'workerId' : workerId,
                      'assignmentId' : assignmentId,
                      'hitId' : hitId,
                      'cicCount' : cNum,
                      'hitGroupId' : hitGroupId,
                  }
                  )
def collectPage(request,questions,workerId,assignmentId,hitGroupId,hitId):
    print questions[0].taskDescription
    que = []
    for x in questions:
        dic = {"content":x.taskContent}
        dic["id"] = x.taskId
        que.append(dic)
    return render(request, 'collect.html',
                  {
                      'content' :questions[0].taskContent,
                      'questions': que,
                      'workerId' : workerId,
                      'assignmentId' : assignmentId,
                      'hitId' : hitId,
                      'hitGroupId' : hitGroupId,
                  }
                  )
def fillPage(request,questions,workerId,assignmentId,hitGroupId,hitId):
    print questions[0].taskDescription
    que = []
    for x in questions:
        dic = {"content":x.taskContent}
        dic["id"] = x.taskId
        que.append(dic)
    return render(request, 'fill.html',
                  {
                      'questions': que,
                      'workerId' : workerId,
                      'assignmentId' : assignmentId,
                      'hitId' : hitId,
                      'hitGroupId' : hitGroupId,
                  }
                  )


def welChoicesPage(request,questions,title,description):
    print questions[0].taskDescription
    cNum = len(json.loads(questions[0].taskDescription))
    que = []
    for x in questions:
        dic = {"content":x.taskContent}
        choiceslist = []
        choices = json.loads(x.taskDescription)
        for index in range(len(choices)):
            choiceslist.append({"key":index,"value":choices[index]})
        dic ["choices"] = choiceslist
        dic["id"] = x.taskId
        que.append(dic)
    return render(request,
                  'welcome/welcomeChoices.html',
                  {
                            'questions': que,
                            'title':title,
                            'description':description
                    }
                )
def welSingleChoicePage(request, questions, title, description):
    print questions[0].taskLabels
    cNum = len(json.loads(questions[0].taskLabels)["choices"])
    que = []
    for x in questions:
        dic = {"content":x.taskDescription}
        choiceslist = []
        choices = json.loads(x.taskLabels)["choices"]
        for index in range(len(choices)):
            choiceslist.append({"key":index,"value":choices[index]})
        dic ["choices"] = choiceslist
        dic["id"] = x.taskId
        dic["img"] = json.loads(x.taskLabels)["img"]
        que.append(dic)
    return render(request,
                  'welcome/welcomeSingleLabel.html',
                  {
                      'questions': que,
                      'title':title,
                      'description':description
                  }
                  )
def welMultiChoicePage(request, questions, title, description):
    print questions[0].taskDescription
    cNum = len(json.loads(questions[0].taskDescription)["choices"])
    que = []
    for x in questions:
        dic = {"content":x.taskContent}
        choiceslist = []
        choices = json.loads(x.taskDescription)["choices"]
        for index in range(len(choices)):
            choiceslist.append({"key":index,"value":choices[index]})
        dic ["choices"] = choiceslist
        dic["id"] = x.taskId
        dic["img"] = json.loads(x.taskDescription)["img"]
        que.append(dic)
    return render(request,
                  'welcome/welcomeMultiLabel.html',
                  {
                      'questions': que,
                      'title':title,
                      'description':description
                  }
                  )
def welCollectPage(request,questions,title,description):
    print questions[0].taskDescription
    que = []
    for x in questions:
        dic = {"content":x.taskContent}
        dic["id"] = x.taskId
        que.append(dic)
    return render(request,
                  'welcome/welcomeCollect.html',
                  {
                      'questions': que,
                      'title':title,
                      'content':que[0]["content"],
                      'description':description
                  }
                  )
def welFillPage(request,questions,title,description):
    print questions[0].taskDescription
    que = []
    for x in questions:
        dic = {"content":x.taskContent}
        dic["id"] = x.taskId
        que.append(dic)
    return render(request,
                  'welcome/welcomeFill.html',
                  {
                      'questions': que,
                      'title':title,
                      'description':description
                  }
                  )
