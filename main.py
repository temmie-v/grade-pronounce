#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# https://docs.microsoft.com/ja-jp/azure/cognitive-services/speech-service/how-to-pronunciation-assessment
# https://github.com/Azure-Samples/cognitive-services-speech-sdk

from pathlib import Path
import csv
import difflib
import glob
import json
import string
import os
import time
try:
    import azure.cognitiveservices.speech as speechsdk
except ImportError:
    print('Speech SDK for Python could not import.')
    import sys
    sys.exit(1)


def gradePronunciation(tokenpath, audiopath, textpath):
    #
    # preparation
    with open(tokenpath) as tokenfile:
        token = json.load(tokenfile)

    with open(textpath) as texifile:
        reference_text = texifile.read()

    # for output
    f = open('./output/grade-{}.csv'.format(Path(audiopath).stem), 'w', newline='')
    writer = csv.writer(f)
    writer.writerow(['File:', Path(audiopath).stem])

    speech_config = speechsdk.SpeechConfig(
        subscription=token['key1'], region=token['region'])
    audio_config = speechsdk.AudioConfig(filename=audiopath)

    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config,
        language='en-us',
        audio_config=audio_config)

    pronunciation_config = speechsdk.PronunciationAssessmentConfig(reference_text=reference_text,
                                                                   grading_system=speechsdk.PronunciationAssessmentGradingSystem.FivePoint,
                                                                   granularity=speechsdk.PronunciationAssessmentGranularity.Phoneme,
                                                                   enable_miscue=True)

    pronunciation_config.apply_to(speech_recognizer)

    #
    # execution
    done = False
    recognized_words = []
    accuracy_scores = []
    pronunciation_scores = []
    durations = []
    valid_durations = []
    start_offset, end_offset = None, None
    results = []

    def stop_cb(evt):
        print('CLOSING on {}'.format(evt))
        nonlocal done
        done = True

    def recognized(evt):
        pronunciation_result = speechsdk.PronunciationAssessmentResult(
            evt.result)
        nonlocal recognized_words, accuracy_scores, pronunciation_scores, durations, valid_durations, start_offset, end_offset, results
        results.append({'sentence': evt.result.text, 'accuracy': pronunciation_result.accuracy_score, 'pronunciation': pronunciation_result.pronunciation_score,
                        'completeness': pronunciation_result.completeness_score, 'fluency': pronunciation_result.fluency_score})
        recognized_words += pronunciation_result.words
        accuracy_scores.append(pronunciation_result.accuracy_score)
        pronunciation_scores.append(pronunciation_result.pronunciation_score)
        json_result = evt.result.properties.get(
            speechsdk.PropertyId.SpeechServiceResponse_JsonResult)
        jo = json.loads(json_result)
        nb = jo['NBest'][0]
        durations.append(sum([int(w['Duration']) for w in nb['Words']]))
        if start_offset is None:
            start_offset = nb['Words'][0]['Offset']
        end_offset = nb['Words'][-1]['Offset'] + \
            nb['Words'][-1]['Duration'] + 100000
        for w, d in zip(pronunciation_result.words, nb['Words']):
            if w.error_type == 'None':
                valid_durations.append(d['Duration'] + 100000)

    speech_recognizer.recognized.connect(recognized)
    speech_recognizer.session_started.connect(
        lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(
        lambda evt: print('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(
        lambda evt: print('CANCELED {}'.format(evt)))
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # main part
    speech_recognizer.start_continuous_recognition()
    # Important: continuous_recognition_async removes 15sec limit
    while not done:
        time.sleep(0.5)

    speech_recognizer.stop_continuous_recognition()
    # main part end

    _accuracy_score = sum(i[0] * i[1]
                          for i in zip(accuracy_scores, durations)) / sum(durations)
    _pronunciation_score = sum(i[0] * i[1]
                               for i in zip(pronunciation_scores, durations)) / sum(durations)

    if start_offset is not None:
        _fluency_score = sum(valid_durations) / \
            (end_offset - start_offset) * 5

    reference_words = [w.strip(string.punctuation)
                       for w in reference_text.lower().split()]

    # for detecting miscue
    diff = difflib.SequenceMatcher(None, reference_words, [
                                   x.word for x in recognized_words])
    final_words = []
    for tag, i1, i2, j1, j2 in diff.get_opcodes():
        if tag in ['insert', 'replace']:
            for word in recognized_words[j1:j2]:
                if word.error_type == 'None':
                    word._error_type = 'Insertion'
                final_words.append(word)
        if tag in ['delete', 'replace']:
            for word_text in reference_words[i1:i2]:
                word = speechsdk.PronunciationAssessmentWordResult({
                    'Word': word_text,
                    'PronunciationAssessment': {
                        'ErrorType': 'Omission',
                    }
                })
                final_words.append(word)
        if tag == 'equal':
            final_words += recognized_words[j1:j2]

    _completeness_score = len(
        [w for w in final_words if w.error_type == 'None']) / len(reference_words) * 5

    writer.writerows([['', 'Accuracy', 'Pronunciation', 'Completeness', 'Fluency'],
                     ['Summary', _accuracy_score, _pronunciation_score,
                         _completeness_score, _fluency_score],
                     []])
    # accuracy_score etc. are grades for one sentence
    # _accuracy_score etc. summarize the score of each sentence
    writer.writerow(['Sentence', 'Accuracy', 'Pronunciation',
                    'Completeness', 'Fluency', 'recognized'])
    for i, result in enumerate(results):
        writer.writerow(['No.' + str(i + 1), result['accuracy'], result['pronunciation'],
                        result['completeness'], result['fluency'], result['sentence']])

    writer.writerows([[],
                     ['Word', 'Phoneme', 'Accuracy', 'error type']])
    for word in final_words:
        writer.writerow([word.word, '', word.accuracy_score, word.error_type])
        if word.error_type == 'None':
            for ph in word.phonemes:
                writer.writerow(['', ph.phoneme, ph.accuracy_score])

    f.close()


# main
azuretokenpath = './token.json'
if not os.path.isfile(azuretokenpath):
    print('speech service key not found')
    import sys
    sys.exit(1)

audionames = glob.glob('./submit/*.wav')

for audioname in audionames:
    textname = os.path.dirname(audioname) + '/' + Path(audioname).stem + '.txt'
    if not os.path.isfile(textname):
        print(Path(audioname).stem, ': speech script not found')
        import sys
        sys.exit(1)
    else:
        print('-', Path(audioname).stem)
        gradePronunciation(azuretokenpath, audioname, textname)
