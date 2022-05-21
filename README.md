# grade-pronounce

This program allows pronunciation assessment via asynchronous communication from [Azure Speech SDK](https://docs.microsoft.com/ja-jp/azure/cognitive-services/speech-service/speech-sdk).

It supports audio (WAV format) longer than 15 seconds. It processes multiple files at once, and outputs each assessment in CSV format.

[Azure Cognitive Services](https://azure.microsoft.com/ja-jp/services/cognitive-services/)' resource is required.

---

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
- `output/grade-{audioname}.csv `

## grading

Azure Cognitive Services grades voices *sentence-by-sentence*. For the evaluation of the **whole paragraph**, this program re-calculates grading:
- Accuracy score: weighted average of each sentence's accuracy score
- pronunciation score: weighted average of each sentence's pronunciation score
- completeness score: percentage of words with error_type `None`, instead of `Insertion` and `Omission`
- fluency score: percentage of time actually spoken

---

## example

- input
    - submit/sample.wav: saying  `What time is it?`\
    ref: [Sample Voice](https://github.com/MicrosoftLearning/AI-102-AIEngineer/tree/master/07-speech/Python/speaking-clock)
    - submit/sample.txt > "What time is it now in Japan?" (deliberate mistake)
- output: grade-sample.csv

|File:|sample| | | | |
|:----|:----|:----|:----|:----|:----|
| |Accuracy|Pronunciation|Completeness|Fluency| |
|Summary|5|5|2.857142857|5| |
| | | | | | |
|Sentence|Accuracy|Pronunciation|Completeness|Fluency|recognized|
|No.1|5|5|5|5|What time is it?|
| | | | | | |
|Word|Phoneme|Accuracy|error type| | |
|what| |5|None| | |
| |w|5| | | |
| |aa|3.5| | | |
| |t|5| | | |
|time| |5|None| | |
| |t|5| | | |
| |ay|5| | | |
| |m|5| | | |
|is| |5|None| | |
| |ih|5| | | |
| |z|5| | | |
|it| |5|None| | |
| |ih|5| | | |
| |t|5| | | |
|now| |0|Omission| | |
|in| |0|Omission| | |
|japan| |0|Omission| | |




## references

- [発音評価の使用方法 - Azure Cognitive Services](https://docs.microsoft.com/ja-jp/azure/cognitive-services/speech-service/how-to-pronunciation-assessment)
- [Sample Repository for the Microsoft Cognitive Services Speech SDK](https://github.com/Azure-Samples/cognitive-services-speech-sdk)
