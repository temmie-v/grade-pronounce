# grade-pronounce

## specification

Required
- `token.json` ... example: `{"key1":"*********", "region":"eastasia"}`
- a folder `submit` ... includes scripts(.txt) and voices(.wav) \
    corresponding voice and script should have the same file name, like `sample.wav` and `sample.txt`
- create a folder `output` ... grade will be written in this folder

Run
```
python ./main.py
```

Result
- `output/grade-{audioname}.txt`

## grading
Azure Cognitive Services grades voices *sentence-by-sentence*. For the evaluation of the whole paragraph, this program re-calculates grades:
- Accuracy score: weighted average of each sentence's accuracy score
- pronunciation score: weighted average of each sentence's pronunciation score
- completeness score: percentage of words with error_type `None`
- fluency score: percentage of time actually spoken

## example
- input
    - submit/sample.wav: saying `What time is it? (20sec no sound) What time is it?`\
    ref: [Sample Voice](https://github.com/MicrosoftLearning/AI-102-AIEngineer/tree/master/07-speech/Python/speaking-clock)
    - submit/sample.txt > "What time is it now in Japan? What time is it?"
- output: grade-sample.txt
```
speech script: What time is it now in Japan? What time is it?

pronunciation assessment for each sentence:
- What time is it?
    Accuracy score: 5.0, pronunciation score: 5.0, completeness score : 5.0, fluency score: 5.0
- What time is it?
    Accuracy score: 5.0, pronunciation score: 5.0, completeness score : 5.0, fluency score: 5.0

In whole paragraph:
    Accuracy score: 5.00, pronunciation score: 5.00, completeness score: 3.64, fluency score: 0.45

pronunciation assessment for each word:
1: word: what	accuracy score: 5.0	error type: None
    Phoneme : w, Score : 4.5;
    Phoneme : aa, Score : 3.5;
    Phoneme : t, Score : 5.0;
2: word: time	accuracy score: 5.0	error type: None
    Phoneme : t, Score : 5.0;
    Phoneme : ay, Score : 5.0;
    Phoneme : m, Score : 5.0;
3: word: is	accuracy score: 5.0	error type: None
    Phoneme : ih, Score : 5.0;
    Phoneme : z, Score : 5.0;
4: word: it	accuracy score: 5.0	error type: None
    Phoneme : ih, Score : 5.0;
    Phoneme : t, Score : 5.0;
5: word: now	accuracy score: 0	error type: Omission
6: word: in	accuracy score: 0	error type: Omission
7: word: japan	accuracy score: 0	error type: Omission
8: word: what	accuracy score: 4.5	error type: None
    Phoneme : w, Score : 4.0;
    Phoneme : aa, Score : 2.0;
    Phoneme : t, Score : 5.0;
9: word: time	accuracy score: 5.0	error type: None
    Phoneme : t, Score : 5.0;
    Phoneme : ay, Score : 5.0;
    Phoneme : m, Score : 5.0;
10: word: is	accuracy score: 5.0	error type: None
    Phoneme : ih, Score : 5.0;
    Phoneme : z, Score : 5.0;
11: word: it	accuracy score: 5.0	error type: None
    Phoneme : ih, Score : 5.0;
    Phoneme : t, Score : 5.0;
```

## references
- [発音評価の使用方法 - Azure Cognitive Services](https://docs.microsoft.com/ja-jp/azure/cognitive-services/speech-service/how-to-pronunciation-assessment)
- [Sample Repository for the Microsoft Cognitive Services Speech SDK](https://github.com/Azure-Samples/cognitive-services-speech-sdk)
