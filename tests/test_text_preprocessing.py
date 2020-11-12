
import pytest
from tokenization import sentence_tokenize

passing_sentences = [
    ("How's your        day going???!It's     going...\n actually it's going \t bad.",
     ["How's your day going???!", "It's going... actually it's going bad."]),
    ("Hello.Goodbye.",
     ["Hello.", "Goodbye."]),
    ("Mr. Elster looked worried. We didn't know why.",
     ["Mr. Elster looked worried.", "We didn't know why."]),
    ("London, capital of U.K., is quite expensive.",
     ["London, capital of U.K., is quite expensive"]),
    ("I was born in 02.28.1980 in N.Y. It's been quite some time!",
     ["I was born in 02.28.1980 in N.Y.", "It's been quite some time!"]),
    ("She asked \"How's it going?\", and I said \"Great!\"",
     ["She asked \"How's it going?\", and I said \"Great!\""]),
    ("\"Everyone will be famous for 15 minutes.\" - Andy Warhol",
     ["\"Everyone will be famous for 15 minutes.\" - Andy Warhol"]),
    ("As we can see in Figure 1.1. the model will eventually converge.",
     ["As we can see in Figure 1.1. the model will eventually converge."]),
    ("NLP (i.e. Natural Language Processing) is great!!!No kidding!",
     ["NLP (i.e. Natural Language Processing) is great!!!", "No kidding!"]),
    ("Tomorrow I can't. I work the morning shift, i.e., from 6 am to 1 pm.",
     ["Tomorrow I can't.", "I work the morning shift, i.e., from 6 am to 1 pm."]),
    ("First: grab the ingredients;don't get the salt just yet. Then, preheat oven.",
     ["First: grab the ingredients; don't get the salt just yet.", "Then, preheat oven."]),
    ("I don't like Voldemort,A.K.A.\"he-who-must-not-be-named.\"",
     ["I don't like Voldemort, A.K.A. \"he-who-must-not-be-named.\""]),
    ("Whitespaces ??!Honestly   ,not my thing ; that is , I don't get them !",
     ["Whitespaces??!", "Honesty, not my thing; that is, I don't get them!"])
] 

failing_sentences = [
    ("I should be considered two sencentes!but I'm not.",
     ["I should be considered two sentences!", "but I'm not."])
]

@pytest.mark.parametrize("input_sentences, expected", passing_sentences)
def test_sentence_tokenize(input_sentences, expected):
    assert sentence_tokenize(input_sentences) == expected


@pytest.mark.xfail(condition="failing-tests", reason="For now, this errors cannot be solved.")
@pytest.mark.parametrize("input_sentences, expected", failing_sentences)
def test_sentence_tokenize_fail(input_sentences, expected):
    assert sentence_tokenize(input_sentences) == expected