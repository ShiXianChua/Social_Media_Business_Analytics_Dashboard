# coding=utf-8
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import emoji
import string
from dash import html
import plotly.express as px


def give_emoji_free_comment(comment_with_emoji):
    return emoji.get_emoji_regexp().sub(r'', comment_with_emoji)


def strip_non_ascii(comment_with_emoji):
    stripped = (c for c in comment_with_emoji if 0 < ord(c) < 127)
    return ''.join(stripped)


def add_space_emoji(text):
    return ''.join(' ' + char + ' ' if char in emoji.UNICODE_EMOJI['en'] else char for char in text).strip()


def add_space_non_ascii(text):
    return ''.join(' ' + c + ' ' if not 0 < ord(c) < 127 else c for c in text).strip()


def add_space_number(text):
    return ''.join(' ' + num + ' ' if num.isdigit() else num for num in text).strip()


class SentimentAnalysisP1:
    def __init__(self):
        self.analyser = SentimentIntensityAnalyzer()

    def conduct_saP1(self, comments):
        eLexicon_update = {
            # positive
            'fire': 4.0,
            'winking-face': 2.0,
            'star-struck': 2.0,
            'face-savoring-food': 2.0,
            'smiling-face-with-smiling-eyes': 2.0,
            'face-with-tongue': 2.0,
            'winking-face-with-tongue': 2.0,
            'zany-face': 2.0,
            'squinting-face-with-tongue': 2.0,
            'money-mouth-face': 2.0,
            'smirking-face': 2.0,
            'drooling-face': 2.0,
            'face-with-open-mouth': 2.0,
            'flushed-face': 2.0,
            'heavy-check-mark': 4.0,
            'thumbs-up': 4.0,
            'victory-hand': 2.0,
            'love-you': 2.0,
            'clapping-hands': 2.0,
            'raising-hands': 2.0,
            'open-hands': 2.0,
            'palms-up': 2.0,
            'handshake': 3.0,
            'folded-hands': 2.0,
            'selfie': 2.0,
            'flexed-biceps': 4.0,
            'person-bowing': 2.0,
            'family': 2.0,
            'hundred-points': 4.0,
            'collision': 2.0,
            'dizzy': 2.0,
            'bomb': 2.0,
            # negative
            'grinning-face-with-sweat': -2.0,
            'upside-down-face': -2.0,
            'zipper-mouth-face': -2.0,
            'face-with-raised-eyebrow': -2.0,
            'unamused-face': -2.0,
            'face-with-rolling-eyes': -3.0,
            'pensive-face': -2.0,
            'sleepy-face': -2.0,
            'face-with-medical-mask': -2.0,
            'face-with-thermometer': -2.0,
            'face-with-head-bandage': -2.0,
            'nauseated-face': -2.0,
            'face-vomiting': -3.0,
            'sneezing-face': -2.0,
            'hot-face': -2.0,
            'cold-face': -2.0,
            'woozy-face': -2.0,
            'dizzy-face': -2.0,
            'exploding-head': -3.0,
            'hushed-face': -2.0,
            'pleading-face': -2.0,
            'sad-but-relieved-face': -1.0,
            'confounded-face': -2.0,
            'persevering-face': -2.0,
            'face-with-steam-from-nose': -3.0,
            'pouting-face': -2.0,
            'face-with-symbols-on-mouth': -2.0,
            'smiling-face-with-horns': -2.0,
            'skull': -2.0,
            'skull-and-crossbones': -2.0,
            'pile-of-poo': -2.0,
            'clown-face': -2.0,
            'ogre': -2.0,
            'goblin': -2.0,
            'alien': -2.0,
            'alien-monster': -2.0,
            'middle-finger': -4.0,
            'thumbs-down': -4.0,
            'person-facepalming': -3.0,
            'person-shrugging': -3.0,
            'broken-heart': -3.0
        }
        self.analyser.lexicon.update(eLexicon_update)
        print(comments)
        print(len(comments))
        newComments = []
        for comment in comments:
            # padding punctuation with white spaces (keeping punctuation)
            comment = comment.translate(str.maketrans({key: " {0} ".format(key) for key in string.punctuation}))
            # padding number with white spaces (keeping number)
            comment = add_space_number(comment)
            # padding non ascii characters with white space (keeping them) - able to turn ❤️ to ❤ with spaces
            comment = add_space_non_ascii(comment)
            newComments.append(comment)
        print(newComments)
        print(len(newComments))

        counter = 0
        ss = 0
        positive = 0
        negative = 0
        neutral = 0
        for comment in newComments:
            counter += 1
            # print(self.analyser.polarity_scores(comment))
            ss = ss + self.analyser.polarity_scores(comment).get('compound')
            if self.analyser.polarity_scores(comment).get('compound') >= 0.05:
                positive += 1
            elif self.analyser.polarity_scores(comment).get('compound') <= -0.05:
                negative += 1
            else:
                neutral += 1
            # print(counter)

        ss = round(((ss / counter) * 100), 2)
        # print(ss)
        # print(positive)
        # print(negative)
        # print(neutral)

        if ss >= 5:
            ssc = 'green'
            ssd = ['Congratulations, your Instagram page has a positive sentiment score!', html.Br(),
                   'Your audience likes your content!']
        elif ss <= -5:
            ssc = 'red'
            ssd = ['Your Instagram page has a negative sentiment score.', html.Br(),
                   'Your audience does not like your content.', html.Br(),
                   'You might want to improve your social media content strategy.']
        else:
            ssc = 'black'
            ssd = ['Your Instagram page has a neutral sentiment score.', html.Br(),
                   'It\'s time to boost up your social media content strategy!']

        # Barchart (number of positive, negative and neutral comments)
        commentDict = {'Comment': ["Positive", "Neutral", "Negative"], 'Number': [positive, neutral, negative]}
        commentDf = pd.DataFrame.from_dict(commentDict)
        commentFig = px.bar(commentDf, x="Comment", y='Number', title='Number of Positive, Negative & Neutral Comments')
        commentFig.update_layout(title={'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'})

        return ss, ssc, ssd, commentFig, positive, neutral, negative


