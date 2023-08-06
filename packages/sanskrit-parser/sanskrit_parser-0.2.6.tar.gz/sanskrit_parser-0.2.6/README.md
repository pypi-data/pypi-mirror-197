# sanskrit_parser
Parsers for Sanskrit / संस्कृतम्

![example workflow](https://github.com/kmadathil/sanskrit_parser/actions/workflows/build_and_test.yml/badge.svg)

**NOTE:** This project is still under development. Both over-generation (invalid forms/splits) and under-generation (missing valid forms/splits) are quite likely. Please see the Sanskrit Parser Stack section below for detailed status. Report any issues [here](https://github.com/kmadathil/sanskrit_parser/issues).

Please feel free to ping us if you would like to collaborate on this project.

## Try it out!
- A simple web interface is available at https://sanskrit-parser.appspot.com/
- Launch the [example notebook](https://github.com/kmadathil/sanskrit_parser/blob/master/examples/basic_example.ipynb) on Binder - [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/kmadathil/sanskrit_parser/HEAD?filepath=examples%2Fbasic_example.ipynb)
- Launch the [example notebook](https://github.com/kmadathil/sanskrit_parser/blob/master/examples/basic_example.ipynb) on Google colab - [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kmadathil/sanskrit_parser/blob/master/examples/basic_example.ipynb)

## Installation

This project has been tested and developed using Python 3.7 - 3.9. To install the package:
```
pip install sanskrit_parser
```
To enable statistical scoring based on DCS, please also install gensim and sentencepiece:
```
pip install gensim sentencepiece
```
See next section for some options if gensim installation fails, and you need the scoring feature.

### Gensim installation: Alternate options if `pip install` fails
The scoring implementation in `sanskrit_parser` depends on [`gensim`](https://radimrehurek.com/gensim/) for scoring,
which requires the capability to [build C extensions for Python](https://docs.python.org/3/extending/building.html). If you have an appropriate C compiler for your system, `gensim` should be installed automatically during `pip install`. We have seen some cases where `pip install` is unable to install `gensim` on Windows, and the following instructions are for those situations.

On Windows, `gensim` typically requires the installation of Microsoft build tools for Visual studio 2019 as documented [here](https://wiki.python.org/moin/WindowsCompilers). If you cannot, or do not want to install MS build tools to compile extensions, some alternate options are:
1. Install the pre-built Windows library from https://www.lfd.uci.edu/~gohlke/pythonlibs/. (Please follow the instructions on the website to install the dependencies first.)
2. Run your code in the cloud (either on Binder or Colab) - See links in the `Try it out` section
3. Use the REST API of sanskrit-parser.appspot.com documented here - https://sanskrit-parser.appspot.com/sanskrit_parser/docs. You can use the try it out option under the default version -> splits -> Try it out. It will show you the sample commands for CURL or the URL itself, as well as the response.


## Usage
- For a tour of the basic features, check out the [example notebook](https://github.com/kmadathil/sanskrit_parser/blob/master/examples/basic_example.ipynb).
- For more detailed documentation, see [generated sphynx docs](https://kmadathil.github.io/sanskrit_parser/build/html/).
- PS: Command line usage is also documented there.

### Deploying REST API server
Run:
```
sudo mkdir /var/www/.sanskrit_parser
sudo chmod a+rwx /var/www/.sanskrit_parser
```

## Contribution
- Generate docs: `cd docs; make html`


## Sanskrit Parser Stack

Stack of parsing tools

### Level 0
Sandhi splitting subroutine
       Input: Phoneme sequence and Phoneme number to split at
       Action: Perform a sandhi split at given input phoneme number
       Output:  left and right sequences (multiple options will be output).
       No semantic validation will be performed (up to higher levels)

#### Current Status
Module that performs sandhi split/join and convenient rule definition is at `parser/sandhi.py`.

Rule definitions (human readable!) are at `lexical_analyzer/sandhi_rules/*.txt`

This is not accessed standalone from the command line.

### Level 1
* From dhatu + lakAra + puruSha + vachana to pada and vice versa
* From prAtipadika + vibhakti + vachana to pada and vice versa
* Upasarga + dhAtu forms - forward and backwards
* nAmadhAtu forms
* Krt forms  - forwards and backwards
* Taddhita forms  - forwards and backwards

#### Current Status
Bootstrapped using a lexical lookup module built from
1. inriaxmlwrapper + Prof. Gerard Huet's forms database
1. the sanskrit_data project, suitably wrapped

(Either or both of these can be enabled at runtime)

That gives us the minimum we need from Level 1, so Level 2 can work.  As the [generator sub-project](#sanskrit-generator) matures, that will take over the role of this Level

Use `sanskrit_parser tags` on the command line to access this

### Level 2

#### Input
Sanskrit Sentence
#### Action
*   Traverse the sentence, splitting it (or not) at each location to determine all possible valid splits
*   Traverse from left to right
*   Using dynamic programming, assemble the results of all choices

      To split or not to split at each phoneme

      If split, all possible left/right combination of phonemes that can result

      Once split, check if the left section is a valid pada (use level 1 tools to pick pada type and tag morphologically)

      If left section is valid, proceed to split the right section
* At the end of this step, we will have all possible syntactically valid splits with morphological tags

#### Output
All semantically valid sandhi split sequences

#### Current Status
Module at `parser/sandhi_analyer.py`

Use `sanskrit_parser sandhi` on the command line


###    Level 3
#### Input
Semantically valid sequence of tagged padas (output of Level 1)
#### Action:
* Assemble graphs of morphological constraints

    viseShaNa - viseShya

    karaka/vibhakti

    vachana/puruSha constraints on tiGantas and subantas
* Check validity of graphs
#### Output
1.  Is the input sequence a morphologically valid sentence?
1.  Enhanced sequence of tagged padas, with karakas tagged, and a dependency graph associated

#### Current Status
Module at `parser/vakya_analyer.py`

Use `sanskrit_parser vakya` on the command line

## Sanskrit Generator

Generate any valid sanskrit pada using Ashtadhyayi rules, plus vartikas where necessary.

Rules are input in a high level meta-language (currently yaml with imposed semantics - this may change), and the internal rule engine executes rules till a valid pada form is output. Input may be

1. prakriti + pratyaya
1. prakriti + sentence semantics

subantas of ajanta prAtipadikas are currently implemented. Other features are being rolled in.

Use `sanskrit_generator` on the command line

## Seq2Seq based Sanskrit Parser

See: Grammar as a Foreign Language : Vinyals & Kaiser et. al. Google
http://arxiv.org/abs/1412.7449

* Method: Seq2Seq Neural Network (n? layers)
* Input Embedding with word2vec (optional)

### Input
Sanskrit sentence
### Output
Sentence split into padas with tags
### Train/Test data
DCS corpus, converted by Vishvas Vasuki

#### Current Status
Not begun

