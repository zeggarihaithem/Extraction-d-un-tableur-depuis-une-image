# Tesseract usage
## Command
```bash
tesseract <file> <output> [options]... [configfile]...
```

## File
Name of the input file. The file must be an image file or a text file.

### Supported formats
- jpg;
- png;
- tiff;
- webp;
- jp2;
- bmp;
- pnm;
- gif;
- ps;
- pdf

A text file shall be the list of image files to be processed. The list shall be separated by new line. The results will be combined in a single file for each output file format (txt, pdf, hocr, xml).

If file is `stdin` or `-`, then the image is read from standard input.

## Output
The output's file basename (extension will be .txt unless otherwise specified). \
If outpupt is `stdout` or `-`, then the result will be written to standard output.

## Options
- -c CONFIGVAR=VALUE: Set value for configvar.
- --dpi N: Specify the resolution of the input image in dots per inch.
- -l LANG, -l SCRIPT: Specify language(s) used for OCR. If none is specified, eng (English) is assumed. Multiple languages may be specified, separated by '+'. Tesseract uses 3-character ISO 639-2 language codes.
- --psm N: Only run a subset of layout analysis and assume a certain form of image. N can be:
    - 0 = Orientation and script detection (OSD) only.
    - 1 = Automatic page segmentation with OSD.
    - 2 = Automatic page segmentation, but no OSD, or OCR.
    - 3 = Fully automatic page segmentation, but no OSD. (Default)
    - 4 = Assume a single column of text of variable sizes.
    - 5 = Assume a single uniform block of vertically aligned text.
    - 6 = Assume a single uniform block of text.
    - 7 = Treat the image as a single text line.
    - 8 = Treat the image as a single word.
    - 9 = Treat the image as a single word in a circle.
    - 10 = Treat the image as a single character.
    - 11 = Sparse text. Find as much text as possible in no particular order.
    - 12 = Sparse text with OSD.
    - 13 = Raw line. Treat the image as a single text line, bypassing hacks that are Tesseract-specific.
    $$$ Use 4 for table (drawn rows and columns) -- Use 6 for others. (4 works best with all)$$$
- --oem N: Specify the OCR Engine mode.
    - 0 = Legacy engine only
    - 1 = Neural nets LSTM engine only
    - 2 = Legacy + LSTM engines
    - 3 = Default, based on what is available

## Configfile
Name of a config to use. A config is a plain text file which contains a list of parameters and their values, one per line, with a space separating parameter from value. \
Interesting config file include:
- alto: Output in ALTO format.
- hocr: Output in hOCR format.
- pdf: Output in PDF format.
- tsv: Output in TSV format.
- txt: Output in plain text format.
- get.images: Write processed input images to file (tessinput.tif).
- logfile: Redirect debug messages to file (tesseract.log).
- lstm.train: Output files used by LSTM training (<output>.lstmf).
- makebox: Write box file (<output>.box).
- quiet: Suppress all messages except errors.

It is possible to select several config files, for example tesseacr image.png demo alto hocr pdf txt will create four output files demo.alto, demo.hocr, demo.pdf and demo.txt with the OCR results.

nB: Options -l LANG, -l SCRIPT, --psm N must occur before any config file.

## Single options
- -h, --help: Show help message and exit.
- --help-extra: Show extra help for advanced users.
- --help-psm: Show page segmentation modes.
- --help-oem: Show OCR Engine modes.
- -v, --version: Show version information and exit.
- --list-langs: List available languages for tesseract engine.
- --print-parameters: Print tesseract parameters to stdout.

## Languages and scripts
More than one language or script may be specified by using '+'. For example, to recognize French and English text, use `tesseract myimage.png myimage -l fra+eng`. \
https://github.com/tesseract-ocr/tessdata_fast provides fast language and script models which are also part of Linux distributions. \
Here is a list of available languages for Tesseract 4 provided by the tessdata_fast repository:
- afr (Afrikaans)
- amh (Amharic)
- ara (Arabic)
- asm (Assamese)
- aze (Azerbaijani)
- aze_cyrl (Azerbaijani - Cyrilic)
- bel (Belarusian)
- ben (Bengali)
- bod (Tibetan)
- bos (Bosnian)
- bre (Breton)
- bul (Bulgarian)
- cat (Catalan; Valencian)
- ceb (Cebuano)
- ces (Czech)
- chi_sim (Chinese simplified)
- chi_tra (Chinese traditional)
- chr (Cherokee)
- cym (Welsh)
- dan (Danish)
- deu (German)
- dzo (Dzongkha)
- ell (Greek, Modern, 1453-)
- eng (English)
- enm (English, Middle, 1100-1500)
- epo (Esperanto)
- equ (Math / equation detection module)
- est (Estonian)
- eus (Basque)
- fas (Persian)
- fin (Finnish)
- fra (French)
- frk (Frankish)
- frm (French, Middle, ca.1400-1600)
- gle (Irish)
- glg (Galician)
- grc (Greek, Ancient, to 1453)
- guj (Gujarati)
- hat (Haitian; Haitian Creole)
- heb (Hebrew)
- hin (Hindi)
- hrv (Croatian)
- hun (Hungarian)
- iku (Inuktitut)
- ind (Indonesian)
- isl (Icelandic)
- ita (Italian)
- ita_old (Italian - Old)
- jav (Javanese)
- jpn (Japanese)
- kan (Kannada)
- kat (Georgian)
- kat_old (Georgian - Old)
- kaz (Kazakh)
- khm (Central Khmer)
- kir (Kirghiz; Kyrgyz)
- kmr (Kurdish Kurmanji)
- kor (Korean), kor_vert (Korean vertical)
- kur (Kurdish)
- lao (Lao)
- lat (Latin)
- lav (Latvian)
- lit (Lithuanian)
- ltz (Luxembourgish)
- mal (Malayalam)
- mar (Marathi)
- mkd (Macedonian)
- mlt (Maltese)
- mon (Mongolian)
- mri (Maori)
- msa (Malay)
- mya (Burmese)
- nep (Nepali)
- nld (Dutch; Flemish)
- nor (Norwegian)
- oci (Occitan post 1500)
- ori (Oriya)
- osd (Orientation and script detection module)
- pan (Panjabi; Punjabi)
- pol (Polish)
- por (Portuguese)
- pus (Pushto; Pashto)
- que (Quechua)
- ron (Romanian; Moldavian; Moldovan)
- rus (Russian)
- san (Sanskrit)
- sin (Sinhala; Sinhalese)
- slk (Slovak)
- slv (Slovenian)
- snd (Sindhi)
- spa (Spanish; Castilian), spa_old (Spanish; Castilian - Old)
- sqi (Albanian)
- srp (Serbian)
- srp_latn (Serbian - Latin)
- sun (Sundanese)
- swa (Swahili)
- swe (Swedish)
- syr (Syriac)
- tam (Tamil)
- tat (Tatar)
- tel (Telugu)
- tgk (Tajik)
- tgl (Tagalog)
- tha (Thai)
- tir (Tigrinya)
- ton (Tonga)
- tur (Turkish)
- uig (Uighur; Uyghur)
- ukr (Ukrainian)
- urd (Urdu)
- uzb (Uzbek)
- uzb_cyrl (Uzbek - Cyrilic)
- vie (Vietnamese)
- yid (Yiddish)
- yor (Yoruba)

For Tesseract 4, the following scripts are also available:
- Arabic
- Armenian
- Bengali
- Canadian_Aboriginal
- Cherokee
- Cyrillic
- Devanagari
- Ethiopic
- Fraktur
- Georgian
- Greek
- Gujarati
- Gurmukhi
- HanS (Han simplified)
- HanS_vert (Han simplified, vertical)
- HanT (Han traditional)
- HanT_vert (Han traditional, vertical)
- Hangul
- Hangul_vert (Hangul vertical)
- Hebrew
- Japanese
- Japanese_vert (Japanese vertical)
- Kannada
- Khmer
- Lao
- Latin
- Malayalam
- Myanmar
- Oriya (Odia)
- Sinhala
- Syriac
- Tamil
- Telugu
- Thaana
- Thai
- Tibetan
- Vietnamese

## Examples
- `tesseract image.png output`: Recognize image.png and write output to output.txt.
- `tesseract image.png output -l eng`: Recognize image.png using the English language.
- `tesseract image.png output -l eng+fra`: Recognize image.png using the English and French languages.
- `tesseract image.png output -l eng --oem 1`: Recognize image.png using the English language and the legacy engine.
- `tesseract image.png output -l eng --oem 2`: Recognize image.png using the English language and the LSTM engine.
- `tesseract image.png output -l eng --oem 3`: Recognize image.png using the English language and the default engine.
- `tesseract image.png output -l eng --oem 1 --psm 6`: Recognize image.png using the English language, the legacy engine and page segmentation mode 6.
- `tesseract image.png output -l eng --oem 1 --psm 6 --dpi 300`: Recognize image.png using the English language, the legacy engine, page segmentation mode 6 and a DPI of 300.
- `tesseract image.png output -l eng --oem 1 --psm 6 --dpi 300 --tessdata-dir /path/to/tessdata`: Recognize image.png using the English language, the legacy engine, page segmentation mode 6, a DPI of 300 and a custom tessdata directory.
- `tesseract image.png output -l eng --oem 1 --psm 6 --dpi 300 --tessdata-dir /path/to/tessdata --user-words /path/to/words.txt`: Recognize image.png using the English language, the legacy engine, page segmentation mode 6, a DPI of 300, a custom tessdata directory and a custom words file.
- `tesseract image.png output -l eng --oem 1 --psm 6 --dpi 300 --tessdata-dir /path/to/tessdata --user-patterns /path/to/patterns.txt`: Recognize image.png using the English language, the legacy engine, page segmentation mode 6, a DPI of 300, a custom tessdata directory and a custom patterns file.
- `tesseract image.png output -l eng --oem 1 --psm 6 --dpi 300 --tessdata-dir /path/to/tessdata --user-words /path/to/words.txt --user-patterns /path/to/patterns.txt`: Recognize image.png using the English language, the legacy engine, page segmentation mode 6, a DPI of 300, a custom tessdata directory, a custom words file and a custom patterns file.
...

## Docs
https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_thresholding/py_thresholding.html