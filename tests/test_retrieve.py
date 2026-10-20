from src.corpus import load_chunks, split_document
from src.retrieve import THRESHOLD, default_index, tokenize


def test_corpus_splits_on_headings_and_skips_readme():
    chunks = load_chunks()
    ids = {c.id for c in chunks}
    assert "time-off.md#how-to-request-time-off" in ids
    assert all(c.doc != "README.md" for c in chunks)
    assert all(c.text for c in chunks)


def test_split_document_ignores_title_and_empty_sections():
    chunks = split_document("x.md", "# Title\n\n## One\nfirst line\nsecond line\n\n## Empty\n\n## Two\nmore")
    assert [(c.id, c.text) for c in chunks] == [("x.md#one", "first line second line"), ("x.md#two", "more")]


def test_tokenize_drops_stopwords_and_plural_s():
    assert tokenize("How do I request the days?") == ["request", "day"]


def test_time_off_question_finds_the_request_section_above_threshold():
    hits = default_index().search("How do I request time off?")
    assert hits[0].chunk.id == "time-off.md#how-to-request-time-off"
    assert hits[0].score >= THRESHOLD


def test_off_topic_questions_stay_below_threshold():
    for question in ["Does Brightpath pay for a gym membership?", "What is the dress code?", "Who is the CEO?"]:
        hits = default_index().search(question)
        assert not hits or hits[0].score < THRESHOLD, question
