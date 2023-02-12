# Voice Gender Changer

This tool changes the gender of an input audio file from a man to woman and vice versa. It can also detect utterance's gender automatically.

## How it works

On average, women speak at an octave higher (twice the frequency) than men. An adult man's average pitch range is from 165 to 255 Hz, and a man's is 85 to 155 Hz [1]. Hence, we can discriminate utterance's gender by comparing their average pitch with160 Hz. Finally, the pitch is doubled or halved (given the gender) to generate the output file. 

To estimate pitch at each time frame, we use the [`librosa.pyin`](https://librosa.org/doc/main/generated/librosa.pyin.html) method. To shift pitch, TD-PSOLA algorithm from [psola](https://github.com/maxrmorrison/psola) package is used.



[1] https://leader.pubs.asha.org/doi/10.1044/leader.FTR1.24022019.44

## How to use

Use `-h` switch to see available options.

```bash
$ python change.py -h
usage: change.py [-h] [-o OUTPUT] [-g {male,female}] input

positional arguments:
  input                 input file rlative file

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        output file relative path
  -g {male,female}, --gender {male,female}
                        input file utterance gender - empty to detect gender automatically
```

For example, to change the gender of the sample file at `./samples/man-3000-15664-0009.flac` and write it to `woman.mp3` execute the following command:

```bash
$ python change.py -o woman.mp3 './samples/man-3000-15664-0009.flac'
```

