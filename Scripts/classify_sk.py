#!/usr/bin/env python3

import glob
import numpy
import sys
import warnings
import argparse
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import LinearSVC


def load_data(languages, label_encoder, path, extension, balance=True):
    """
    Create an array of filenames which contain samples, and an array of associated labels.
    if balance is set to True, the dataset will automatically be balanced.
    """
    x = []
    y = []
    # If we want to use a balanced dataset, we use the same number of samples for every class.
    # This number is determined by the number of samples in the class with the least amount of samples.
    if balance:
        min_size = min([len(glob.glob('{}/{}/*{}'.format(path, lang, extension))) for lang in languages])
    else:
        min_size = None  # Slicing a list with [:None] returns the whole list
    # Put filenames in x, and the corresponding label in y
    for lang in languages:
        filenames = glob.glob('{}/{}/*{}'.format(path, lang, extension))
        x += filenames[:min_size]
        y += [lang] * len(filenames[:min_size])
    return numpy.array(x), label_encoder.transform(y)


def get_ngrams(list_of_tags, n=3):
    """Create a list containing strings which denote n-grams"""
    return [ascii(tuple(list_of_tags[i:i + n])) for i in range(len(list_of_tags) - (n - 1))]


def create_ngrams(contents):
    """Convert the content of a file to a list of n-grams"""
    features = []
    tags = contents.split()
    if args.features == 'tokens':
        for i in range(1, 3):
            features += get_ngrams(tags, i)
    else:
        for i in range(2, 6):
            features += get_ngrams(tags, i)
    return features


def print_confusion_matrix(classes, matrix):
    """Print a confusion matrix to the standard output"""
    print('\t' + '\t'.join(classes))
    for i, line in enumerate(matrix):
        print(classes[i], end='\t')
        print('\t'.join(str(j) for j in line))


def show_most_informative_features(vectorizer, label_encoder, pipeline):
    """Show the most informative features for the given pipeline/classifier"""
    print('Analysing most informative features')
    features = vectorizer.get_feature_names()
    for label in label_encoder.classes_:
        i = label_encoder.transform([label])[0]
        most_informative = numpy.argsort(pipeline.get_params()['clf'].coef_[i])[-10:]
        print('{}: {}'.format(label, ' | '.join(str(features[j]) for j in most_informative)))
    print()


def main():
    numpy.random.seed(0)
    languages = ['DE', 'EN', 'ES', 'FR', 'IT', 'NL']

    print('Loading filenames and labels...')
    label_encoder = LabelEncoder()
    label_encoder.fit(languages)
    x, y = load_data(languages, label_encoder, args.path, args.extension, args.balance)

    print('Transforming data...')
    vectorizer = CountVectorizer(input='filename', preprocessor=None, tokenizer=create_ngrams, binary=True)
    # As the occurence of certain tags won't be influenced by the presence of texts from the testset,
    # we can already transform all data into binary matrices here. This avoids processing the
    # same data multiple times for no good reason.
    x = vectorizer.fit_transform(x)
    print('Data transformed into {} features'.format(len(vectorizer.vocabulary_)))

    print('Starting cross validation steps:')
    folds = StratifiedKFold(n_splits=10, shuffle=True)
    y_total_test = numpy.array([])
    y_total_observed = numpy.array([])
    for train_index, test_index in folds.split(x, y):
        x_train, x_test = x[train_index], x[test_index]
        y_train, y_test = y[train_index], y[test_index]
        print('Fitting classifier...')
        pipeline = Pipeline([('transformer', TfidfTransformer()), ('clf', LinearSVC(class_weight='balanced'))])
        pipeline.fit(x_train, y_train)
        y_observed = pipeline.predict(x_test)
        # Print the most informative features and other metrics
        show_most_informative_features(vectorizer, label_encoder, pipeline)
        print('Showing metrics...')
        print_confusion_matrix(list(label_encoder.classes_), confusion_matrix(y_test, y_observed))
        print()
        print(classification_report(y_test, y_observed, target_names=languages))
        y_total_test = numpy.concatenate([y_total_test, y_test])
        y_total_observed = numpy.concatenate([y_total_observed, y_observed])
        print()

    print('Showing overall metrics...')
    print_confusion_matrix(list(label_encoder.classes_), confusion_matrix(y_total_test, y_total_observed))
    print()
    print(classification_report(y_total_test, y_total_observed, target_names=languages))
    print()

    # If requested, test on a separate testset
    if args.evaluate:
        print('Testing on given test set:')
        print('Fitting classifier...')
        pipeline = Pipeline([('transformer', TfidfTransformer()), ('clf', LinearSVC(class_weight='balanced'))])
        pipeline.fit(x, y)
        show_most_informative_features(vectorizer, label_encoder, pipeline)
        eval_files = []
        eval_labels = []
        for language in languages:
            files = glob.glob('{}/{}/*{}'.format(args.evaluate, language, args.extension))
            eval_files += files
            eval_labels += [language] * len(files)
        eval_x = vectorizer.transform(eval_files)
        eval_y = label_encoder.transform(eval_labels)
        eval_obs = pipeline.predict(eval_x)
        print(classification_report(eval_y, eval_obs, target_names=languages))
        print()


if __name__ == '__main__':
    # Ignore some numpy warnings
    warnings.filterwarnings("ignore")
    # Parse command line arguments
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('-b', '--balance', help='Balance the training set', action='store_true')
    argument_parser.add_argument('-e', '--evaluate',
                                 help='Test the system on the given dataset after cross-validating.\n'
                                      'This dataset should have the same directory structure as the training set.',
                                 metavar=('PATH',), type=str)
    argument_parser.add_argument('-f', '--features', default='POS',
                                 help='The type of features to use (default: %(default)s)',
                                 choices=['tokens', 'POS', 'POS-universal'])
    argument_parser.add_argument('path', help='The location of the preprocessed training data', type=str)
    args = argument_parser.parse_args()
    # Format paths as required
    if args.path and args.path[-1] == '/':
        args.path = args.path[:-1]
    if args.evaluate and args.evaluate[-1] == '/':
        args.evaluate = args.evaluate[:-1]
    if args.features:
        extensions = {'tokens': '.txt', 'POS': '.pos', 'POS-universal': '.uni'}
        args.extension = extensions[args.features]
    # Run the main function
    main()
