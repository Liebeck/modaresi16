from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import SelectPercentile
from sklearn.preprocessing import Normalizer
from sklearn.decomposition import PCA
from sklearn.feature_selection import chi2
from sklearn.feature_selection import f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from ..tokenizers.tweet_tokenizer import TweetTokenizer
from sklearn.pipeline import FeatureUnion
from ..utils.utils import get_classifier
from ..utils.utils import show_most_informative_features
from ..utils.utils import get_stopwords
from ..preprocessors.text_cleaner import TextCleaner
from sklearn.feature_selection import SelectFromModel
from sklearn.svm import LinearSVC
from sklearn import linear_model, decomposition
from sklearn.decomposition import TruncatedSVD
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import RFECV
from sklearn.cross_validation import StratifiedKFold
from profiler16_un.profilers.spelling_error_profiler import SpellingError
from profiler16_un.profilers.pos_tag_profiler import POSFeatures

tc = TextCleaner(lowercase=True,
                 filter_urls=True,
                 filter_mentions=True,
                 filter_hashtags=True,
                 alphabetic=True,
                 strip_accents=True,
                 filter_rt=True)


class EnglishGenderProfiler():
    def __init__(self, lang='en', min_n=1, max_n=1, method=None):
        word_unigrams = ('word_unigrams', Pipeline([('vect', CountVectorizer(min_df=2,
                                                                             stop_words=get_stopwords(),
                                                                             preprocessor=tc,
                                                                             ngram_range=(1, 1))),
                                                    ('tfidf', TfidfTransformer(sublinear_tf=True)),
                                                    ('scale', Normalizer())]))

        word_bigrams = ('word_bigrams', Pipeline([('vect', CountVectorizer(preprocessor=tc, ngram_range=(2, 2))),
                                                  ('tfidf', TfidfTransformer(sublinear_tf=True)),
                                                  ('scale', Normalizer())]))

        char_ngrams = ('char_ngrams', Pipeline([('vect', CountVectorizer(min_df=1,
                                                                         preprocessor=TextCleaner(filter_urls=True,
                                                                                                  filter_mentions=True,
                                                                                                  filter_hashtags=True,
                                                                                                  lowercase=True),
                                                                         analyzer='char',
                                                                         ngram_range=(3, 6))),
                                                ('tfidf', TfidfTransformer(sublinear_tf=True)),
                                                ('scale', Normalizer())]))

        punctuation_ngrams = ('punctuation_ngrams', Pipeline([('vect', CountVectorizer(min_df=1,
                                                                                       preprocessor=TextCleaner(filter_urls=True,
                                                                                                                filter_mentions=True,
                                                                                                                filter_hashtags=True,
                                                                                                                only_punctuation=True,
                                                                                                                lowercase=True),
                                                                                       analyzer='char',
                                                                                       ngram_range=(1, 3))),
                                                              ('tfidf', TfidfTransformer(sublinear_tf=True)),
                                                              ('scale', Normalizer())]))
        # avg_spelling_error = ('avg_spelling_error', SpellingError(language=lang))
        pos_distribution = ('pos_distribution', POSFeatures(language=lang))

        self.pipeline = Pipeline([('features', FeatureUnion([word_unigrams,
                                                             word_bigrams,
                                                             # char_ngrams,
                                                             punctuation_ngrams
                                                             ])),
                                  # ('chi', SelectKBest(chi2, k=700000)),
                                  ('classifier', get_classifier(method=method))])

    def train(self, X_train, Y_train):
        self.model = self.pipeline.fit(X_train, Y_train)
        # print(type(self.pipeline.named_steps['features'].get_feature_names))
        # show_most_informative_features(self.pipeline.named_steps['features'], self.pipeline.named_steps['classifier'])

    def predict(self, X):
        return self.model.predict(X)
