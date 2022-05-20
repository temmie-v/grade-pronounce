# grade-pronounce

## specification

Required
- `token.json` ... example: `{"key1":"*********", "region":"eastasia"}`
- `submit/` ... includes **one** script(.txt, no break lines) and **one** voice(.wav)

Result
- `output/{audioname}.txt`

## example
- input: [Sample Informative Speech (7min)](https://www.youtube.com/watch?v=SRKrbXEbEvU)
    - 7min.wav
    - script.txt
- output: 7min.txt
```
pronunciation assessment for: Six months ago my 78 young grandmother was...
Result
    Accuracy score: 88.0, pronunciation score: 89.4, completeness score : 94.0, fluency score: 89.0
pronunciation assessment for: Than her doctor suggested acupuncture...
Result
    Accuracy score: 91.0, pronunciation score: 92.4, completeness score : 97.0, fluency score: 92.0
...
...
In whole paragraph:
    Accuracy score: 89.6, completeness score: 83.8, fluency score: 85.4

1: word: six	accuracy score: 100.0	error type: None
    Phoneme : s, Score : 100.0;
    Phoneme : ih, Score : 100.0;
    Phoneme : k, Score : 100.0;
    Phoneme : s, Score : 100.0;
2: word: months	accuracy score: 100.0	error type: None
    Phoneme : m, Score : 100.0;
...
7: word: young	accuracy score: 1.0	error type: Mispronunciation
8: word: grandmother	accuracy score: 91.0	error type: None
    Phoneme : g, Score : 100.0;
    Phoneme : r, Score : 100.0;
    Phoneme : ae, Score : 100.0;
    Phoneme : n, Score : 32.0;
    Phoneme : m, Score : 100.0;
    Phoneme : ah, Score : 86.0;
    Phoneme : dh, Score : 91.0;
    Phoneme : ax, Score : 100.0;
    Phoneme : r, Score : 100.0;
9: word: was	accuracy score: 100.0	error type: None
    Phoneme : w, Score : 100.0;
    Phoneme : ax, Score : 100.0;
    Phoneme : z, Score : 100.0;
10: word: clear	accuracy score: 8.0	error type: Mispronunciation
11: word: use	accuracy score: 28.0	error type: Mispronunciation
12: word: in	accuracy score: 40.0	error type: Insertion
13: word: her	accuracy score: 86.0	error type: Insertion
14: word: independence	accuracy score: 100.0	error type: Insertion
15: word: creeping	accuracy score: 0	error type: Omission
16: word: this	accuracy score: 0	error type: Omission
17: word: anger	accuracy score: 0	error type: Omission
18: word: independents	accuracy score: 0	error type: Omission
19: word: severe	accuracy score: 67.0	error type: None
    Phoneme : s, Score : 31.0;
...
...
```
