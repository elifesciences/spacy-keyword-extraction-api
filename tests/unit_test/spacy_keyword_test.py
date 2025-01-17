from unittest.mock import MagicMock

import pytest

from spacy.language import Language
from spacy.tokens import Span

from spacy_keyword_extraction_api.spacy_keyword import (
    get_span_without_apostrophe,
    get_normalized_span_text,
    is_conjunction_token,
    join_spans,
    get_text_list,
    get_noun_chunk_for_noun_token,
    get_noun_chunks,
    iter_split_noun_chunk_conjunctions,
    get_conjuction_noun_chunks,
    iter_individual_keyword_spans,
    iter_shorter_keyword_spans,
    lstrip_stop_words_and_punct,
    rstrip_punct,
    strip_stop_words_and_punct,
    normalize_text,
    SpacyExclusion,
    SpacyKeywordList,
    SpacyKeywordDocumentParser
)


@pytest.fixture(name="spacy_keyword_document_parser", scope="session")
def _spacy_keyword_document_parser(spacy_language_en: Language):
    return SpacyKeywordDocumentParser(spacy_language_en)


@pytest.fixture(name="spacy_keyword_document_parser_full", scope="session")
def _spacy_keyword_document_parser_full(spacy_language_en_full: Language):
    return SpacyKeywordDocumentParser(spacy_language_en_full)


@pytest.fixture(name="spacy_language_mock")
def _spacy_language_mock():
    return MagicMock(name="language")


class TestGetSpanWithoutApostrophe:
    def test_should_remove_apostrophe(
            self, spacy_language_en: Language):
        assert get_span_without_apostrophe(spacy_language_en(
            "Johnson's"
        )).text == "Johnson"


class TestGetNormalizedSpanText:
    def test_should_convert_plural_to_singular(
            self, spacy_language_en: Language):
        assert get_normalized_span_text(spacy_language_en(
            "technologies"
        )) == 'technology'

    def test_should_normalize_remove_apostrophe(
            self, spacy_language_en: Language):
        assert get_normalized_span_text(spacy_language_en(
            "Parkinson's"
        )) == 'parkinson'

    def test_should_convert_single_token_to_lower_case(
            self, spacy_language_en: Language):
        assert get_normalized_span_text(spacy_language_en(
            "fMRI"
        )) == 'fmri'

    def test_should_convert_multiple_token_span_to_lower_case(
            self, spacy_language_en: Language):
        assert get_normalized_span_text(spacy_language_en(
            "Advanced Technology"
        )) == 'advanced technology'

    def test_should_use_lemma_if_norm_equals_text_case_insensitive(
            self, spacy_language_en: Language):
        assert get_normalized_span_text(spacy_language_en(
            "Technologies"
        )) == 'technology'


class TestIsConjunctionToken:
    def test_should_return_true_for_and_token_only(
            self, spacy_language_en: Language):
        assert [
            is_conjunction_token(token)
            for token in spacy_language_en('this and that')
        ] == [False, True, False]


class TestJoinSpans:
    def test_should_join_two_spans(
            self, spacy_language_en: Language):
        assert join_spans(
            [
                spacy_language_en('the joined'),
                spacy_language_en('span')
            ],
            language=spacy_language_en
        ).text == 'the joined span'


class TestGetNounChunkForNounToken:
    def test_should_return_span_for_noun_token(
            self, spacy_language_en: Language):
        doc = spacy_language_en('using technology')
        technology_token = doc[-1]
        noun_chunk = get_noun_chunk_for_noun_token(technology_token)
        assert noun_chunk.text == 'technology'
        assert isinstance(noun_chunk, Span)


class TestGetNounChunks:
    def test_should_return_simple_noun_chunk(
            self, spacy_language_en: Language):
        assert get_text_list(get_noun_chunks(spacy_language_en(
            'using technology'
        ))) == ['technology']

    def test_should_return_two_noun_chunk_separated_by_and(
            self, spacy_language_en: Language):
        assert get_text_list(get_noun_chunks(spacy_language_en(
            'using technology and approach'
        ))) == ['technology', 'approach']

    def test_should_return_two_noun_chunk_separated_by_comma_in_sentence(
            self, spacy_language_en: Language):
        assert get_text_list(get_noun_chunks(spacy_language_en(
            'using technology, approach'
        ))) == ['technology', 'approach']

    @pytest.mark.slow
    def test_should_return_two_noun_chunk_separated_by_comma_no_sentence(
            self, spacy_language_en_full: Language):
        assert get_text_list(get_noun_chunks(spacy_language_en_full(
            'technology, approach'
        ))) == ['technology', 'approach']


class TestIterSplitNounChunkConjunctions:
    def test_should_not_split_noun_chunk_without_conjunctions(
            self, spacy_language_en: Language):
        assert [span.text for span in iter_split_noun_chunk_conjunctions(
            spacy_language_en('advanced technology'),
            language=spacy_language_en
        )] == ['advanced technology']

    def test_should_split_and_join_noun_chunk_on_conjunction(
            self, spacy_language_en: Language):
        assert [span.text for span in iter_split_noun_chunk_conjunctions(
            spacy_language_en('advanced and special technology'),
            language=spacy_language_en
        )] == ['advanced technology', 'special technology']

    def test_should_not_split_hyphenated_noun_chunk_on_conjunction(
            self, spacy_language_en: Language):
        assert [span.text for span in iter_split_noun_chunk_conjunctions(
            spacy_language_en('advanced-and-special technology'),
            language=spacy_language_en
        )] == ['advanced-and-special technology']


class TestGetConjuctionNounChunks:
    def test_should_not_split_noun_chunk_without_conjunctions(
            self, spacy_language_en: Language):
        assert [span.text for span in get_conjuction_noun_chunks(
            spacy_language_en('advanced technology'),
            language=spacy_language_en
        )] == ['advanced technology']

    def test_should_split_and_join_noun_chunk_on_conjunction_without_comma(
            self, spacy_language_en: Language):
        assert [span.text for span in get_conjuction_noun_chunks(
            spacy_language_en('advanced and special technology'),
            language=spacy_language_en
        )] == ['advanced technology', 'special technology']

    def test_should_split_and_join_noun_chunk_on_conjunction_with_comma(
            self, spacy_language_en: Language):
        assert {span.text for span in get_conjuction_noun_chunks(
            spacy_language_en('advanced, and special technology'),
            language=spacy_language_en
        )} == {'advanced technology', 'special technology'}

    def test_should_return_two_noun_chunk_separated_by_comma_no_sentence(
            self, spacy_language_en: Language):
        assert {span.text for span in get_conjuction_noun_chunks(
            spacy_language_en('advanced technology, special approach'),
            language=spacy_language_en
        )} == {'advanced technology', 'special approach'}


class TestIterIndividualKeywordSpans:
    def test_should_return_no_results_if_keyword_is_not_compound(
            self, spacy_language_en: Language):
        assert [span.text for span in iter_individual_keyword_spans(
            spacy_language_en('technology'),
            language=spacy_language_en
        )] == []

    def test_should_return_individual_words_from_compound_keyword(
            self, spacy_language_en: Language):
        assert [span.text for span in iter_individual_keyword_spans(
            spacy_language_en('advanced technology'),
            language=spacy_language_en
        )] == ['advanced', 'technology']

    def test_should_only_return_individual_words_from_larger_compound_keyword(
            self, spacy_language_en: Language):
        assert [span.text for span in iter_individual_keyword_spans(
            spacy_language_en('very advanced technology'),
            language=spacy_language_en
        )] == ['very', 'advanced', 'technology']

    def test_should_ignore_single_word_words(
            self, spacy_language_en: Language):
        assert [span.text for span in iter_individual_keyword_spans(
            spacy_language_en('M strain'),
            language=spacy_language_en
        )] == ['strain']

    def test_should_not_split_hyphenated_keyword(
            self, spacy_language_en: Language):
        assert [span.text for span in iter_individual_keyword_spans(
            spacy_language_en('simple-and-advanced technology'),
            language=spacy_language_en
        )] == ['simple-and-advanced', 'technology']


class TestIterShorterKeywordSpans:
    def test_should_return_no_results_if_keyword_is_not_compound(
            self, spacy_language_en: Language):
        assert [span.text for span in iter_shorter_keyword_spans(
            spacy_language_en('technology'),
            language=spacy_language_en
        )] == []

    def test_should_return_no_results_for_two_word_keyword(
            self, spacy_language_en: Language):
        assert [span.text for span in iter_shorter_keyword_spans(
            spacy_language_en('advanced technology'),
            language=spacy_language_en
        )] == []

    def test_should_return_last_two_words_for_three_word_keyword(
            self, spacy_language_en: Language):
        assert [span.text for span in iter_shorter_keyword_spans(
            spacy_language_en('very advanced technology'),
            language=spacy_language_en
        )] == ['advanced technology']

    def test_should_return_last_three_and_two_words_for_four_word_keyword(
            self, spacy_language_en: Language):
        assert [span.text for span in iter_shorter_keyword_spans(
            spacy_language_en('very extra advanced technology'),
            language=spacy_language_en
        )] == ['extra advanced technology', 'advanced technology']


class TestLstripStopWordsAndPunct:
    def test_should_strip_leading_stop_words(
            self, spacy_language_en: Language):
        assert lstrip_stop_words_and_punct(spacy_language_en(
            'the advanced technology'
        )).text == 'advanced technology'

    def test_should_not_strip_non_stop_words(
            self, spacy_language_en: Language):
        assert lstrip_stop_words_and_punct(spacy_language_en(
            'advanced technology'
        )).text == 'advanced technology'

    def test_should_strip_comma(
            self, spacy_language_en: Language):
        assert lstrip_stop_words_and_punct(spacy_language_en(
            ', advanced technology'
        )).text == 'advanced technology'

    def test_should_strip_brackets(
            self, spacy_language_en: Language):
        assert lstrip_stop_words_and_punct(spacy_language_en(
            '(1) advanced technology'
        )).text == 'advanced technology'

    def test_should_not_strip_apostrophe(
            self, spacy_language_en: Language):
        assert lstrip_stop_words_and_punct(spacy_language_en(
            "Pakinsons's disease"
        )).text == "Pakinsons's disease"

    def test_should_not_strip_hyphen_i(
            self, spacy_language_en: Language):
        # "I" is considered a stop word but that is not what is meant here
        assert lstrip_stop_words_and_punct(spacy_language_en(
            "MHC-I molecule"
        )).text == "MHC-I molecule"

    def test_should_not_strip_stop_word_within_hyphenated_keyword(
            self, spacy_language_en: Language):
        # "and" is considered a stop word but we don't want to
        # break apart the hyphenated keyword
        assert lstrip_stop_words_and_punct(spacy_language_en(
            "simple-and-advanced technology"
        )).text == "simple-and-advanced technology"

    def test_should_strip_eg(
            self, spacy_language_en: Language):
        assert lstrip_stop_words_and_punct(spacy_language_en(
            "e.g. technology"
        )).text == "technology"


class TestRstripPunct:
    def test_should_strip_leading_stop_words(
            self, spacy_language_en: Language):
        assert strip_stop_words_and_punct(spacy_language_en(
            'the technology'
        )).text == 'technology'

    def test_should_strip_tailing_closing_bracket(
            self, spacy_language_en: Language):
        assert rstrip_punct(spacy_language_en(
            'technology)'
        )).text == 'technology'


class TestStripStopWordsAndPunct:
    def test_should_strip_tailing_closing_bracket(
            self, spacy_language_en: Language):
        assert rstrip_punct(spacy_language_en(
            'technology)'
        )).text == 'technology'


class TestNormalizeText:
    def test_should_replace_line_feed_with_space(self):
        assert normalize_text('the\nkeyword') == 'the keyword'

    def test_should_replace_muliple_whitepace_with_single_space(self):
        assert normalize_text('the \t\n\t keyword') == 'the keyword'

    def test_should_strip_surrounding_whitespace(self):
        assert normalize_text(' \nthe keyword\n ') == 'the keyword'

    def test_should_replace_slash_with_comma(self):
        assert normalize_text('the/keyword') == 'the, keyword'


class TestSpacyExclusion:
    def test_should_not_match_different_word(
            self, spacy_language_en: Language):
        assert not SpacyExclusion({'interest'}).should_exclude(
            spacy_language_en('technology')
        )

    def test_should_match_exact_word(
            self, spacy_language_en: Language):
        assert SpacyExclusion({'interest'}).should_exclude(
            spacy_language_en('interest')
        )

    def test_should_match_last_word(
            self, spacy_language_en: Language):
        assert SpacyExclusion({'interest'}).should_exclude(
            spacy_language_en('research interest')
        )

    def test_should_match_normalized_word(
            self, spacy_language_en: Language):
        assert SpacyExclusion({'technology'}).should_exclude(
            spacy_language_en('technologies')
        )

    def test_should_exclude_if_word_length_below_minimum(
            self, spacy_language_en: Language):
        assert SpacyExclusion(min_word_length=3).should_exclude(
            spacy_language_en('xy')
        )

    def test_should_not_exclude_if_word_length_at_minimum(
            self, spacy_language_en: Language):
        assert not SpacyExclusion(min_word_length=2).should_exclude(
            spacy_language_en('xy')
        )


class TestSpacyKeywordList:
    def test_should_extract_individual_tokens_from_single_keyword_span(
            self, spacy_language_en: Language):
        assert set(
            SpacyKeywordList(
                language=spacy_language_en,
                keyword_spans=[
                    spacy_language_en('advanced technology')
                ]
            )
            .with_individual_tokens
            .text_list
        ) == {'advanced technology', 'advanced', 'technology'}

    def test_should_extract_individual_tokens_from_multiple_keyword_spans(
            self, spacy_language_en: Language):
        assert set(
            SpacyKeywordList(
                language=spacy_language_en,
                keyword_spans=[
                    spacy_language_en('advanced technology'),
                    spacy_language_en('special approach')
                ]
            )
            .with_individual_tokens
            .text_list
        ) == {
            'advanced technology',
            'special approach',
            'advanced',
            'technology',
            'special',
            'approach'
        }

    def test_should_extract_shorter_keywords_from_single_keyword_span(
            self, spacy_language_en: Language):
        assert set(
            SpacyKeywordList(
                language=spacy_language_en,
                keyword_spans=[
                    spacy_language_en('very advanced technology')
                ]
            )
            .with_shorter_keywords
            .text_list
        ) == {'very advanced technology', 'advanced technology'}

    def test_should_extract_shorter_keywords_from_multiple_keyword_spans(
            self, spacy_language_en: Language):
        assert set(
            SpacyKeywordList(
                language=spacy_language_en,
                keyword_spans=[
                    spacy_language_en('very advanced technology'),
                    spacy_language_en('super special approach')
                ]
            )
            .with_shorter_keywords
            .text_list
        ) == {
            'very advanced technology',
            'super special approach',
            'advanced technology',
            'special approach'
        }

    def test_should_strip_leading_stop_words(
            self, spacy_language_en: Language):
        assert (
            SpacyKeywordList(
                language=spacy_language_en,
                keyword_spans=[
                    spacy_language_en('the advanced technology')
                ]
            )
            .with_stripped_stop_words_and_punct
            .text_list
        ) == ['advanced technology']

    def test_should_exclude_keywords(
            self, spacy_language_en: Language):
        assert (
            SpacyKeywordList(
                language=spacy_language_en,
                keyword_spans=[
                    spacy_language_en('technology'),
                    spacy_language_en('lab')
                ]
            )
            .exclude(SpacyExclusion({'lab'}))
            .text_list
        ) == ['technology']


class TestSpacyKeywordDocument:
    def test_should_extract_single_word_noun(
            self, spacy_keyword_document_parser: SpacyKeywordDocumentParser):
        assert (
            spacy_keyword_document_parser.parse_text('using technology')
            .compound_keywords
            .text_list
        ) == ['technology']

    def test_should_extract_single_noun_with_adjective(
            self, spacy_keyword_document_parser: SpacyKeywordDocumentParser):
        assert (
            spacy_keyword_document_parser.parse_text(
                'using advanced technology'
            )
            .compound_keywords
            .text_list
        ) == ['advanced technology']

    def test_should_extract_single_noun_with_hyphenated_adjective(
            self, spacy_keyword_document_parser: SpacyKeywordDocumentParser):
        assert (
            spacy_keyword_document_parser.parse_text(
                'using simple-and-advanced technology'
            )
            .compound_keywords
            .text_list
        ) == ['simple-and-advanced technology']

    def test_should_normalize_text(
            self, spacy_keyword_document_parser: SpacyKeywordDocumentParser):
        assert (
            spacy_keyword_document_parser.parse_text(
                'use advanced \n\n technology'
            )
            .compound_keywords
            .text_list
        ) == ['advanced technology']

    def test_should_extract_individual_tokens(
            self, spacy_keyword_document_parser: SpacyKeywordDocumentParser):
        assert set(
            spacy_keyword_document_parser.parse_text(
                'using advanced technology'
            )
            .compound_keywords
            .with_individual_tokens
            .text_list
        ) == {'advanced technology', 'advanced', 'technology'}

    def test_should_extract_short_keywords(
            self, spacy_keyword_document_parser: SpacyKeywordDocumentParser):
        assert set(
            spacy_keyword_document_parser.parse_text(
                'using very advanced technology'
            )
            .compound_keywords
            .with_shorter_keywords
            .text_list
        ) == {'very advanced technology', 'advanced technology'}

    def test_should_extract_individual_tokens_and_short_keywords(
            self, spacy_keyword_document_parser: SpacyKeywordDocumentParser):
        assert set(
            spacy_keyword_document_parser.parse_text(
                'using very advanced technology'
            )
            .compound_keywords
            .with_individual_tokens
            .with_shorter_keywords
            .text_list
        ) == {
            'very advanced technology', 'advanced technology',
            'very', 'advanced', 'technology'
        }

    @pytest.mark.slow
    def test_should_extract_conjunction_nouns_with_adjective_with_comma(
            self,
            spacy_keyword_document_parser_full: SpacyKeywordDocumentParser):
        # using "full" model,
        # the dependency tree is not complete using small model
        assert set(
            spacy_keyword_document_parser_full.parse_text(
                'we use advanced technique, advanced, and special technology'
            )
            .get_keyword_str_list(individual_tokens=False)
        ) == {
            'advanced technique', 'advanced technology', 'special technology'
        }

    @pytest.mark.slow
    def test_should_extract_conjunction_nouns_with_adjective_without_comma(
            self,
            spacy_keyword_document_parser_full: SpacyKeywordDocumentParser):
        # using "full" model,
        # the dependency tree is not complete using small model
        assert set(
            spacy_keyword_document_parser_full.parse_text(
                'we use advanced technique, advanced and special technology'
            )
            .get_keyword_str_list(individual_tokens=False)
        ) == {
            'advanced technique', 'advanced technology', 'special technology'
        }

    @pytest.mark.slow
    def test_should_not_combine_two_separate_nouns_with_conjunction(
            self,
            spacy_keyword_document_parser_full: SpacyKeywordDocumentParser):
        # using "full" model,
        # the dependency tree is not complete using small model
        assert set(
            spacy_keyword_document_parser_full.parse_text(
                'we use technique and technology'
            )
            .get_keyword_str_list()
        ) == {
            'technique', 'technology'
        }

    @pytest.mark.slow
    def test_should_extract_multiple_keywords_separated_by_comma_as_list(
            self,
            spacy_keyword_document_parser_full: SpacyKeywordDocumentParser):
        assert (
            spacy_keyword_document_parser_full
            .parse_text('technology, approach')
            .compound_keywords
            .text_list
        ) == ['technology', 'approach']

    def test_should_get_keyword_str_list_with_defaults(
            self,
            spacy_keyword_document_parser: SpacyKeywordDocumentParser):
        document = spacy_keyword_document_parser.parse_text(
            'using technology'
        )
        assert document.get_keyword_str_list() == ['technology']

    def test_can_pass_exclusion_set_to_get_keyword_str_list(
            self,
            spacy_keyword_document_parser: SpacyKeywordDocumentParser):
        document = spacy_keyword_document_parser.parse_text(
            'using technology'
        )
        assert document.get_keyword_str_list(
            exclude=SpacyExclusion({'technology'})
        ) == []

    def test_should_exclude_numbers_from_individual_token_of_compound_keyword(
            self, spacy_keyword_document_parser: SpacyKeywordDocumentParser):
        assert set(
            spacy_keyword_document_parser.parse_text(
                r'using 123 technology'
            )
            .get_keyword_str_list(individual_tokens=True)
        ) == {'123 technology', 'technology'}

    def test_should_exclude_numbers(
            self, spacy_keyword_document_parser: SpacyKeywordDocumentParser):
        assert (
            spacy_keyword_document_parser.parse_text(
                r'technology that account for 123'
            )
            .get_keyword_str_list()
        ) == ['technology']

    def test_should_number_of_years(
            self, spacy_keyword_document_parser: SpacyKeywordDocumentParser):
        assert (
            spacy_keyword_document_parser.parse_text(
                r'technology is 10 years old'
            )
            .get_keyword_str_list()
        ) == ['technology']

    def test_should_exclude_percentage(
            self, spacy_keyword_document_parser: SpacyKeywordDocumentParser):
        assert (
            spacy_keyword_document_parser.parse_text(
                r'technology that account for 95%'
            )
            .get_keyword_str_list()
        ) == ['technology']

    def test_should_exclude_greater_than_percentage(
            self, spacy_keyword_document_parser: SpacyKeywordDocumentParser):
        assert (
            spacy_keyword_document_parser.parse_text(
                r'technology that account for >95%'
            )
            .get_keyword_str_list()
        ) == ['technology']

    def test_should_exclude_pronouns(
            self, spacy_keyword_document_parser: SpacyKeywordDocumentParser):
        assert (
            spacy_keyword_document_parser.parse_text('we use technology')
            .get_keyword_str_list()
        ) == ['technology']

    def test_should_exclude_person_name(
            self, spacy_keyword_document_parser: SpacyKeywordDocumentParser):
        assert (
            spacy_keyword_document_parser.parse_text(
                'In collaboration with John Smith'
            )
            .get_keyword_str_list()
        ) == ['collaboration']

    def test_should_exclude_country_name(
            self, spacy_keyword_document_parser: SpacyKeywordDocumentParser):
        assert (
            spacy_keyword_document_parser.parse_text(
                'We research technology in the United Kingdom'
            )
            .get_keyword_str_list()
        ) == ['technology']

    def test_should_convert_plural_to_singular_keyword(
            self, spacy_keyword_document_parser: SpacyKeywordDocumentParser):
        assert (
            spacy_keyword_document_parser.parse_text(
                'we investigate technologies'
            )
            .get_keyword_str_list(normalize_text=True)
        ) == ['technology']

    def test_should_normalize_keyword_spelling(
            self, spacy_keyword_document_parser: SpacyKeywordDocumentParser):
        assert (
            # need to use a word that is in the small spacy model
            spacy_keyword_document_parser.parse_text(
                'we investigate somethin'
            )
            .get_keyword_str_list(normalize_text=True)
        ) == ['something']


class TestSpacyKeywordDocumentParser:
    def test_should_parse_multiple_documents(
            self, spacy_keyword_document_parser: SpacyKeywordDocumentParser):
        assert [
            keyword_document.doc.text
            for keyword_document in (
                spacy_keyword_document_parser
                .iter_parse_text_list(['using technology', 'using approach'])
            )
        ] == ['using technology', 'using approach']

    def test_should_call_language_pipe(
            self, spacy_language_mock: MagicMock):
        text_list = ['using technology', 'using approach']
        list(SpacyKeywordDocumentParser(
            language=spacy_language_mock
        ).iter_parse_text_list(text_list))
        spacy_language_mock.pipe.assert_called()

    def test_should_strip_tags(
            self, spacy_keyword_document_parser: SpacyKeywordDocumentParser):
        assert (
            spacy_keyword_document_parser
            .parse_text('<i>italic</i>')
            .doc.text == 'italic'
        )
