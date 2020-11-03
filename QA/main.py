import nltk
import os
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

Stories = {}
Questions = {}

TokenizedStories = {}
TokenizedQuestions = {}

Answers = {}

#this is a change I made
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
            Stories[storyID.strip('\n')] = storiesText
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
                    Questions[tempQuestionID.strip('\n')] = tempQuestion
                    Answers[tempQuestionID.strip('\n')] = None
                    tempQuestionID = None
                    tempQuestion = None


# Returns a list of storyIDs
def getQuestion(storyID):
    questionID = []
    for i in Questions.keys():
        if i.__contains__(storyID):
            questionID.append(i)
    return questionID


# Tokenzined using NLTK
def stoiresToken(ID, text):
    sentTokenized = nltk.sent_tokenize(text)
    tagged_words = []
    for i in sentTokenized:
        wordTokenized = nltk.word_tokenize(i)
        tagged_words.extend(nltk.pos_tag(wordTokenized))
    TokenizedStories[ID] = tagged_words


def questionToken(question):
    listQuestion = getQuestion(question)
    for i in listQuestion:
        sentTokenized = nltk.sent_tokenize(Questions[i])
        for j in sentTokenized:
            wordTokenized = nltk.word_tokenize(j)
            tagged_words = nltk.pos_tag(wordTokenized)
            TokenizedQuestions[i] = tagged_words


def printDictionaries():
    print("PRINTING STORIES ###########################################")
    for i in Stories:
        print(i, Stories[i])
    print("PRINTING Questions #########################################")
    for j in Questions:
        print(j, Questions[j])
    print("PRINTING Tokenized Stories ##################################")
    for k in TokenizedStories:
        print(k, TokenizedStories[k])
    print("PRINTING Tokenized Questions ################################")
    for l in TokenizedQuestions:
        print(l, TokenizedQuestions[l])


#this is main
# another comment
def main():
    GetData()
    for i, j in Stories.items():
        stoiresToken(i, j)
        questionToken(i)
    printDictionaries()


if __name__ == "__main__":
    main()