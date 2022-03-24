# coding=utf-8
import string
import emoji


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


class CommentProcessing:

    def __init__(self):
        self.positiveWords = []
        self.negativeWords = []
        self.positiveEmojis = []
        self.negativeEmojis = []

    def process_comment(self, comments):
        words = []
        emojis = []
        for comment in comments:
            # padding punctuation with white spaces (keeping punctuation)
            comment = comment.translate(str.maketrans({key: " {0} ".format(key) for key in string.punctuation}))
            # remove all punctuations
            comment = comment.translate(str.maketrans('', '', string.punctuation))
            # padding number with white spaces (keeping number)
            comment = add_space_number(comment)
            # remove numbers
            comment = ''.join([i for i in comment if not i.isdigit()])
            # padding non ascii characters with white space (keeping them)
            comment = add_space_non_ascii(comment)
            # extract all emojis in a comment and put them into a list
            eList = [e for e in comment if e in emoji.UNICODE_EMOJI['en']]
            # strip all non ascii characters (including emojis and chinese words)
            comment = strip_non_ascii(comment)
            # combine into words list
            words.extend(comment.split())
            # combine into emojis list
            emojis.extend(eList)

        # lowercase all words in words list
        words = [word.lower() for word in words]

        # print('OPEN STOPWORDS')

        with open('stopwords.txt') as f:
            sWords = [line.rstrip('\n') for line in f]

        with open('positive.txt') as f:
            pWords = [line.rstrip('\n') for line in f]

        # print('OPEN PE!')

        with open('positiveEmoji.txt', encoding='utf-8') as f:
            pEmojis = [line.rstrip('\n') for line in f]

        with open('negative.txt') as f:
            nWords = [line.rstrip('\n') for line in f]

        with open('negativeEmoji.txt', encoding='utf-8') as f:
            nEmojis = [line.rstrip('\n') for line in f]

        # removing stopwords
        toBeRemoved = []
        for word in words:
            if word in sWords:
                toBeRemoved.append(word)
        for word in toBeRemoved:
            words.remove(word)

        # getting positive words
        for word in words:
            if word in pWords:
                self.positiveWords.append(word)

        # getting negative words
        for word in words:
            if word in nWords:
                self.negativeWords.append(word)

        # getting positive emojis
        for item in emojis:
            if item in pEmojis:
                self.positiveEmojis.append(item)

        # getting negative emojis
        for item in emojis:
            if item in nEmojis:
                self.negativeEmojis.append(item)

        return self.positiveWords, self.negativeWords, self.positiveEmojis, self.negativeEmojis



















