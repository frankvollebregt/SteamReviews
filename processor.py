import json
import nltk

# The different aspects by which a game is judged
points = [
    ['graphics', 'graphical', 'graphic', 'visuals', 'visual', 'art', 'style', 'artstyle', 'art-style'],  # visuals
    ['music', 'audio', 'soundtrack', 'sound'],                                                           # audio
    ['controls', 'control', 'mechanics', 'mechanic', 'port', 'gameplay'],                                # mechanics
    ['performance', 'optimization', 'optimisation', 'stability'],                                        # performance
    ['story', 'writing', 'storytelling', 'immersion', 'characters', 'character']                         # story
]

negative_words = []
positive_words = []


# Fill the arrays with positive and negative words. URL is linked in the readme
def getSentimentWords():
    neg = open('data/negative-words.txt', 'r')
    for word in neg:
        negative_words.append(word[:-1])
    neg.close()

    pos = open('data/positive-words.txt', 'r')
    for word in pos:
        positive_words.append(word[:-1])
    pos.close()


# load all positive and negative words
getSentimentWords()


def process(_filename):
    with open('data/'+_filename+'.txt', 'r') as infile:
        json = json.load(infile)
        print("Total of "+str(len(json))+" reviews")

        rating = []

        # emtpy objects to keep track of ratings
        for i in range(6):
            rating.append({
                'neg': 0,
                'pos': 0
            })

        index = 0
        for review in json:
            # print("Review "+str(index)+"/"+str(len(json)))
            # Only include down-voted reviews, with a 'positive' score
            if not review['voted_up'] and float(review['weighted_vote_score']) > 0.5:
                tokens = nltk.word_tokenize(review['review'].lower())
                tags = nltk.pos_tag(tokens)

                for i in range(len(tags)):
                    # an aspect of the game is mentioned
                    for point in range(len(points)):
                        if tags[i][0] in points[point]:
                            # preceded by an adjective --> weird controls
                            if tags[i-1][1] == 'JJ' or tags[i-1][1] == 'JJS' or tags[i-1][1] == 'JJR':
                                if tags[i-1][0] in positive_words:
                                    rating[point]['pos'] += 1
                                elif tags[i-1][0] in negative_words:
                                    rating[point]['neg'] += 1
                            # (indirectly) succeeded by an adjective --> the controls are weird
                            else:
                                for j in range(2):
                                    if i+1+j >= len(tags):
                                        continue
                                    if tags[i+1+j][1] == 'JJ' or tags[i+1+j][1] == 'JJS' or tags[i+1+j][1] == 'JJR':
                                        if tags[i+1+j][0] in positive_words:
                                            rating[point]['pos'] += 1
                                        elif tags[i+1+j][0] in negative_words:
                                            rating[point]['neg'] += 1
            index += 1

        # others try to extract whether a review is positive or negative, i try to tactically summarize

        print("Final ratings:")
        print("Visuals: " + str(rating[0]))
        print("Audio: " + str(rating[1]))
        print("Mechanics: " + str(rating[2]))
        print("Peformance: " + str(rating[3]))
        print("Story: " + str(rating[4]))
