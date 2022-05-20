import json
import glob
import azure.cognitiveservices.speech as speech_sdk

token = json.load(open("./token.json", "r"))
speech_config = speech_sdk.SpeechConfig(
    subscription=token["key1"], region=token["region"])

submitaudio = glob.glob("./submit/*.wav")
audio_config = speech_sdk.AudioConfig(filename=submitaudio[0])

speech_recognizer = speech_sdk.SpeechRecognizer(
    speech_config=speech_config,
    audio_config=audio_config)

scriptfiles = glob.glob("./submit/*.txt")
scriptfile = open(scriptfiles[0], "r")
script = scriptfile.read()

pronunciation_config = speech_sdk.PronunciationAssessmentConfig(reference_text=script,
                                                                grading_system=speech_sdk.PronunciationAssessmentGradingSystem.HundredMark,
                                                                granularity=speech_sdk.PronunciationAssessmentGranularity.Phoneme)

pronunciation_config.apply_to(speech_recognizer)
result = speech_recognizer.recognize_once()
pronunciation_result = speech_sdk.PronunciationAssessmentResult(result)

f = open('./output/grade.txt', 'w')

f.write('Accuracy score: {}, fluency score: {}, completeness score : {}, pronunciation score: {}\n\n'.format(
    pronunciation_result.accuracy_score, pronunciation_result.fluency_score,
    pronunciation_result.completeness_score, pronunciation_result.pronunciation_score
))

for word in pronunciation_result.words:
    f.write('Word : {}, Score : {}\n'.format(
        word.word, word.accuracy_score))
    for phoneme in word.phonemes: 
        f.write('\tPhoneme : {}, Score : {}\n'.format(
            phoneme.phoneme, phoneme.accuracy_score))
    f.write('\n')

f.close()
