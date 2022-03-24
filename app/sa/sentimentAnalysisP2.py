# coding=utf-8
import pandas as pd
from collections import Counter
import plotly.express as px


class SentimentAnalysisP2:
    def __init__(self):
        self.pTotal = 0
        self.nTotal = 0

    def conduct_saP2(self, positiveWords, negativeWords, positiveEmojis, negativeEmojis):
        # Turning into Counter and dict
        positiveWords = dict(Counter(positiveWords))
        print(positiveWords)
        negativeWords = dict(Counter(negativeWords))
        print(negativeWords)
        positiveEmojis = dict(Counter(positiveEmojis))
        print(positiveEmojis)
        negativeEmojis = dict(Counter(negativeEmojis))
        print(negativeEmojis)

        # Turning into pd df
        positiveWordsDf = pd.DataFrame.from_dict(positiveWords, orient='index', columns=['Frequency'])
        positiveWordsDf.reset_index(inplace=True)
        positiveWordsDf.columns = ['Word', 'Frequency']
        positiveWordsDf.sort_values(by='Frequency', inplace=True, ignore_index=True, ascending=False)
        # print(positiveWordsDf)
        negativeWordsDf = pd.DataFrame.from_dict(negativeWords, orient='index', columns=['Frequency'])
        negativeWordsDf.reset_index(inplace=True)
        negativeWordsDf.columns = ['Word', 'Frequency']
        negativeWordsDf.sort_values(by='Frequency', inplace=True, ignore_index=True, ascending=False)
        # print(negativeWordsDf)
        positiveEmojisDf = pd.DataFrame.from_dict(positiveEmojis, orient='index', columns=['Frequency'])
        positiveEmojisDf.reset_index(inplace=True)
        positiveEmojisDf.columns = ['Emoji', 'Frequency']
        positiveEmojisDf.sort_values(by='Frequency', inplace=True, ignore_index=True, ascending=False)
        # print(positiveEmojisDf.head(10))
        negativeEmojisDf = pd.DataFrame.from_dict(negativeEmojis, orient='index', columns=['Frequency'])
        negativeEmojisDf.reset_index(inplace=True)
        negativeEmojisDf.columns = ['Emoji', 'Frequency']
        negativeEmojisDf.sort_values(by='Frequency', inplace=True, ignore_index=True, ascending=False)
        # print(negativeEmojisDf.head(10))

        # Data Visualisation
        # Visualise words bar chart
        pWordsFreq = positiveWordsDf['Frequency'].sum()
        nWordsFreq = negativeWordsDf['Frequency'].sum()
        wordsDict = {'Word': ['positive', 'negative'], 'Frequency': [pWordsFreq, nWordsFreq]}
        wordsDf = pd.DataFrame(wordsDict)
        # print(wordsDf)
        wordsFig = px.bar(wordsDf, x="Word", y='Frequency', title='Words: Positive vs Negative')
        wordsFig.update_layout(title={'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'})
        # wordsFig.show()

        # Visualise emojis bar chart
        pEmojisFreq = positiveEmojisDf['Frequency'].sum()
        nEmojisFreq = negativeEmojisDf['Frequency'].sum()
        emojisDict = {'Emoji': ['positive', 'negative'], 'Frequency': [pEmojisFreq, nEmojisFreq]}
        emojisDf = pd.DataFrame(emojisDict)
        # print(emojisDf)
        emojisFig = px.bar(emojisDf, x="Emoji", y='Frequency', title='Emojis: Positive vs Negative')
        emojisFig.update_layout(title={'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'})
        # emojisFig.show()

        # Selective visualisation & Sentiment Score
        self.pTotal = pWordsFreq + pEmojisFreq
        self.nTotal = nWordsFreq + nEmojisFreq
        # if positive > negative
        if self.pTotal > self.nTotal:
            t10PositiveWordsDf = positiveWordsDf.copy()
            t10PositiveWordsDf = t10PositiveWordsDf.head(10).copy()
            t10PositiveWordsDf.sort_values(by='Frequency', inplace=True, ignore_index=True, ascending=True)
            t10PositiveEmojisDf = positiveEmojisDf.copy()
            t10PositiveEmojisDf = t10PositiveEmojisDf.head(10).copy()
            t10PositiveEmojisDf.sort_values(by='Frequency', inplace=True, ignore_index=True, ascending=True)
            WordFig = px.bar(t10PositiveWordsDf, x="Frequency", y='Word', title='Top 10 Positive Words')
            WordFig.update_layout(title={'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'})
            EmojiFig = px.bar(t10PositiveEmojisDf, x="Frequency", y='Emoji', title='Top 10 Positive Emojis')
            EmojiFig.update_layout(title={'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'})
        # if negative > positive
        elif self.nTotal > self.pTotal:
            t10NegativeWordsDf = negativeWordsDf.copy()
            t10NegativeWordsDf = t10NegativeWordsDf.head(10).copy()
            t10NegativeWordsDf.sort_values(by='Frequency', inplace=True, ignore_index=True, ascending=True)
            t10NegativeEmojisDf = negativeEmojisDf.copy()
            t10NegativeEmojisDf = t10NegativeEmojisDf.head(10).copy()
            t10NegativeEmojisDf.sort_values(by='Frequency', inplace=True, ignore_index=True, ascending=True)
            WordFig = px.bar(t10NegativeWordsDf, x="Frequency", y='Word', title='Top 10 Negative Words')
            WordFig.update_layout(title={'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'})
            EmojiFig = px.bar(t10NegativeEmojisDf, x="Frequency", y='Emoji', title='Top 10 Negative Emojis')
            EmojiFig.update_layout(title={'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'})
        # if positive == negative
        else:
            t10PositiveWordsDf = positiveWordsDf.copy()
            t10PositiveWordsDf = t10PositiveWordsDf.head(10).copy()
            t10PositiveWordsDf.sort_values(by='Frequency', inplace=True, ignore_index=True, ascending=True)
            t10PositiveEmojisDf = positiveEmojisDf.copy()
            t10PositiveEmojisDf = t10PositiveEmojisDf.head(10).copy()
            t10PositiveEmojisDf.sort_values(by='Frequency', inplace=True, ignore_index=True, ascending=True)
            WordFig = px.bar(t10PositiveWordsDf, x="Frequency", y='Word', title='Top 10 Positive Words!')
            WordFig.update_layout(title={'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'})
            EmojiFig = px.bar(t10PositiveEmojisDf, x="Frequency", y='Emoji', title='Top 10 Positive Emojis')
            EmojiFig.update_layout(title={'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'})

        return wordsFig, emojisFig, WordFig, EmojiFig
