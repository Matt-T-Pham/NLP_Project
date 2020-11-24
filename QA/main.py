import nltk
import os
import spacy
import sys

from nltk.corpus import stopwords

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

nlp = spacy.load('en_core_web_md')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

Stories = {}
Questions = {}
TokenizedStories = {}
TokenizedQuestions = {}
Answers = {}
tagged = {}

input_file = sys.argv[1]

with open(input_file, 'r') as f:
    inputFile = f.readlines()
    inputFile = [x.strip() for x in inputFile]

datasetDir = inputFile.pop(0)
storiesFile = inputFile

NamedEntityRecognition = {
    'who': ['PERSON'],
    'whose': ['PERSON'],
    'where': ['LOC', 'FAC', 'ORG', 'GPE'],
    'when': ['DATE', 'TIME'],
    'how big': ['QUANTITY'],
    'how much money': ['MONEY'],
    'how much': ['QUANTITY'],
    'how old': ['CARDINAL'],
    'how often': ['DATE', 'TIME'],
    'how': ['CARDINAL'],
}


# anotoher change
# this is a change I made
# Gets the data from given Directory and puts the parsed data in dictionaries
class GetData:
    path = os.listdir(datasetDir)
    for fileName in storiesFile:
        with open(os.path.join(datasetDir, fileName + ".story"), 'r') as temp:
            TextFlag = False
            storiesText = ""
            storyID = ""
            for i in temp:
                if TextFlag:
                    storiesText += str(i.replace('\n', ' '))
                if i.__contains__('TEXT:'):
                    TextFlag = True
                if i.__contains__('STORYID:'):
                    split = i.split(':')
                    storyID = split[1]
                if i.__contains__('HEADLINE:'):
                    split = i.split(':')
                    # storiesText += split[1].lstrip()
                if i.__contains__('DATE:'):
                    split = i.split(':')
                # storiesText += split[1].lstrip()
            TextFlag = False
            Stories[storyID.strip('\n')] = storiesText
        with open(os.path.join(datasetDir, fileName + ".questions"), 'r') as temp:
            tempQuestionID = None
            tempQuestion = None
            for i in temp:
                split = i.split(':')
                if split[0] == 'QuestionID':
                    tempQuestionID = split[1]
                if split[0] == 'Question':
                    tempQuestion = split[1]
                    Questions[tempQuestionID.strip('\n')] = tempQuestion
                    Answers[tempQuestionID.strip('\n')] = []
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
        tagged_words.extend(wordTokenized)
    TokenizedStories[ID] = sentTokenized


def questionToken(question):
    listQuestion = getQuestion(question)
    for i in listQuestion:
        sentTokenized = nltk.sent_tokenize(Questions[i])
        for j in sentTokenized:
            wordTokenized = nltk.word_tokenize(j)
            # tagged_words = nltk.pos_tag(wordTokenized)
            wordTokenized = {w for w in wordTokenized if not w in stop_words}
            wordTokenized = [word for word in wordTokenized if word.isalnum()]
            TokenizedQuestions[i] = wordTokenized


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


def answerQuestions(id):
    listQuestion = getQuestion(id)
    for i in listQuestion:
        for question in NamedEntityRecognition.keys():
            if Questions[i].lower().find(question) != -1:
                answerlist = []
                maxi = 0
                # print(Questions[i],question,id)
                for key, val in tagged[id].items():
                    if val in NamedEntityRecognition[question]:
                        answerlist.append(key)
                # print(Questions[i], question, answerlist)
                # for k in answerlist:
                #  for tok in TokenizedStories[id]:
                #      if tok.find(k) != -1:
                #         print(TokenizedQuestions[i])
                #        print(k, '\t', tok)
                Answers[i] = list(set(answerlist + Answers[i]))


def spacyTest(key, text):
    tagged[key] = dict([(str(x), x.label_) for x in nlp(text).ents])


def printAns():
    with open('results.response', 'w') as f:
        for a, b in Answers.items():
            f.write('QuestionID: ' + a + '\n')
            f.write('Answer:' + ' '.join(map(str, b)))
            f.write('\n')


def main():
    GetData()
    for i, j in Stories.items():
        stoiresToken(i, j)
        questionToken(i)
        spacyTest(i, j)
    for l in Stories.keys():
        answerQuestions(l)
    printAns()


if __name__ == "__main__":
    main()