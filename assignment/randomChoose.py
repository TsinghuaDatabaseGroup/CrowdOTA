import random
from plat.models import Worker
from utils import entropy
def assign(questions,quesNum,workId):
    return random.sample(questions,quesNum)


