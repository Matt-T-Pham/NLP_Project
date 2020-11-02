import nltk
import os

Stories = {}
Questions = {}

# Gets the data from given Directory and puts the parsed data in dictionaries
# TODO: make this universal but currently it is easier to do it like this in pycharm
class GetData:
    dir = '../developset-v2'
    path = os.listdir(dir)
    for fileName in path:
        if fileName.endswith('.story'):
            temp = open(dir+'/'+fileName, 'r')
            TextFlag = False
            storiesText = ""
            storyID = ""
            for i in temp:
                if TextFlag:
                    storiesText += str(i)
                if i.__contains__('TEXT:'):
                    TextFlag = True
                if i.__contains__('STORYID:'):
                    split = i.split(':')
                    storyID = split[1]
                if i.__contains__('HEADLINE:'):
                    split = i.split(':')
                    storiesText += split[1].lstrip()
                if i.__contains__('DATE:'):
                    split = i.split(':')
                    storiesText += split[1].lstrip()
            TextFlag = False
            Stories[storyID.lstrip()] = storiesText
        if fileName.endswith('.questions'):
            temp = open(dir + '/' + fileName, 'r')
            tempQuestionID = None
            tempQuestion = None
            for i in temp:
                split = i.split(':')
                if split[0] == 'QuestionID':
                    tempQuestionID = split[1]
                if split[0] == 'Question':
                    tempQuestion = split[1]
                    Questions[tempQuestionID] = tempQuestion
                    tempQuestionID = None
                    tempQuestion = None


# Returns a list of storyIDs
def getQuestion(storyID):
    questionID = []
    for i in Questions.keys():
        if i.__contains__(storyID):
            questionID.append(i)
    return questionID


def main():
    GetData()


if __name__ == "__main__":
    main()