# CSCI 3725: M6
## Quaint Poet
Quaint Poet is a system that generates cinquain poems that relate to a given prompt and polarity. Given a search term, it uses the Guardian API to find articles related to that term and uses the one with highest proportion of text with the desired polarity (positive or negative) as the corpus of words for the poems. Each poem's line is generated according to bigrams and a template of Penn Treebank part-of-speech tags. The system uses a genetic algorithm where the fitness of a poem is determined by how similar it is the search term and the proportion of words that have the specified polarity. The best poem that is produced when running the genetic algorithm is saved to an output file and read aloud using text-to-speech.
<br />
<br />

## Running The Code
Download the files in this repository and navigate to where they were saved. Note: You will need a developer key from the Guardian API to run this code. (One can be requested [here](https://bonobo.capi.gutools.co.uk/register/developer)).

To generate a poem and have it be read aloud, navigate to where the files are located in the command prompt and run the following:

`python3 poem_generator.py <search term> <polarity> <output file>`

where:  
* `search term` is a prompt for the topic of the poem and what will be used to find an article for the corpus
* `polarity` is equal to either `positive` or `negative` and indicates the desired polarity of the poem to be generated
* `output file` is where the generated poem should be saved to


To have the program speak a poem that was previously generated, run the following in the command prompt:
`python3 poem_generator.py <poem file>`

where `poem file` is the file containing the poem to be read.
<br />
<br />

## Reflection
I found coming up with an interesting but feasible idea was one of the most challenging parts of this project. I knew I wanted to incorporate user input in some way and generally wanted the poems that the sytem generates to make sense. I played around with multiple ideas before deciding on having templates for the part-of-speech tags for each line. Another aspect that challenged me was finding the correct tools/libraries to implement what I had planned. There are numerous resources for NLP, and some were more useful for this project than otheres. Specifically, I learned more about spaCy, part-of-speech tagging, and sentiment analysis while designing and implementing this system.
<br />
<br />


## Papers that Inspired my Approach
### Full-FACE Poetry Generation (Simon Colton, Jacob Goodwin, Tony Veale)
#### http://computationalcreativity.net/iccc2012/wp-content/uploads/2012/05/095-Colton.pdf
This paper inspired me to create a corpus-based poetry generation system. This approach seems to produce poems that generally make more sense gramatically and that are more coherent, which were priorities for my system. In addition, I liked how their system used key phrases from a newspaper article to determine which phrases should be included in the poem. Furthermore, their system determines a mood for the given day to be used for the poem that is being generated. I wanted to do something similar by having a target polarity.
<br />
<br />

### An evolutionary algorithm approach to poetry generation (Hisar Maruli Manurung)
#### https://era.ed.ac.uk/bitstream/handle/1842/314/IP040022.pdf
This paper describes McGonagall, a genetic algorithm used to generate poems. For McGonagall, an individual is represented as an LTAG derivation tree and uses operations to modify the trees while adhering to the grammar. While the approach that Quaint Poet uses for its genetic algorithm is very different from McGonogall's, this paper gave me the idea to have a "grammar" defined for each of the five lines in the poem so there would be fewer grammatical errors overall.
<br />
<br />

### Corpus-Based Generation of Content and Form in Poetry (Jukka M. Toivanen, Hannu Toivonen, Alessandro Valitutti, Oskar Gross)
#### https://helda.helsinki.fi/bitstream/handle/10138/37269/toivanen_iccc_2012.pdf?sequence=2&isAllowed=y
This paper describes a system that uses one corpus to provide semantic content for new poems and the other to generate a specific grammatical structure for the poems. Their system can take a topic as a prompt for the new poem and uses word associations to gather a collection of similar words. While I did not use word associations in my system, I did have the system use an article that relates to the prompt with the hope that that article would contain more phrases that relate to it. In addition, their system substitutes words from the semantic corpus into a randomly selected text according and tries to maintain the initial grammar by accounting for part-of-speech, verb tense, etc. Similar to this idea, I used spaCy and a cinquain poem dataset from Kaggle to find the more common tags that were used for each of the five lines. These were then added as a template that is used for generating a poem.
<br />
<br />

## Sources
* spaCy (https://spacy.io/)
* Poem dataset (https://www.kaggle.com/datasets/michaelarman/poemsdataset)
* VADER sentiment analysis (https://github.com/cjhutto/vaderSentiment)

    Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.
* textacy (https://pypi.org/project/textacy/)
* The Guardian API (https://open-platform.theguardian.com/)
* The CMU Pronouncing Dictionary (http://www.speech.cs.cmu.edu/cgi-bin/cmudict)