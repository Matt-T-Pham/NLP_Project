import nltk
import os

Stories = {}
Questions = {}


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


def main():
    GetData()
    for i,j in Stories.items():
        print(i,j)


if __name__ == "__main__":
    main()