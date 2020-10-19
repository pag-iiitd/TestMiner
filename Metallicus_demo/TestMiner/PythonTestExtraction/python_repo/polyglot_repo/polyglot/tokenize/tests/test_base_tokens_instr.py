# -*- coding: latin-1 -*-
import unittest

' Test basic tokenization utilities.'
import unittest
from ..base import SentenceTokenizer, WordTokenizer
from ...base import Sequence
en_text = 'A Ukrainian separatist leader is calling on Russia to "absorb" the eastern region of Donetsk after Sunday\'s referendum on self rule. Self-declared Donetsk People\'s Republic leader Denis Pushilin urged Moscow to listen to the "will of the people". In neighbouring Luhansk, where a vote was also held, rebels declared independence. Ukraine, the EU and US have declared the referendums illegal but Russia says the results should be "implemented". Moscow has so far not commented on the call for Donetsk to become part of Russia but has appealed for dialogue between the militants and Kiev, with the participation of the Organisation for Security and Co-operation in Europe.\n'
ar_text = 'Ø¹Ø¨Ø± Ø£Ø\xadØ¯ Ù\x82Ø§Ø¯Ø© Ø§Ù\x84Ù\x85ØªÙ\x85Ø±Ø¯Ù\x8aÙ\x86 Ø§Ù\x84Ù\x85Ù\x88Ø§Ù\x84Ù\x8aÙ\x86 Ù\x84Ø±Ù\x88Ø³Ù\x8aØ§ Ù\x81Ù\x8a Ø£Ù\x88Ù\x83Ø±Ø§Ù\x86Ù\x8aØ§ Ø¹Ù\x86 Ù\x85Ø³Ø§Ù\x86Ø¯ØªÙ\x87 Ù\x84Ù\x81Ù\x83Ø±Ø© Ø§Ù\x84Ù\x88Ø\xadØ¯Ø© Ù\x85Ø¹ Ø±Ù\x88Ø³Ù\x8aØ§ Ù\x81Ù\x8a Ø£Ø¹Ù\x82Ø§Ø¨ Ø§Ù\x84Ø¥Ø¹Ù\x84Ø§Ù\x86 Ø¹Ù\x86 Ù\x86ØªØ§Ø¦Ø¬ Ø§Ù\x84Ø§Ø³ØªÙ\x81ØªØ§Ø¡ Ø§Ù\x84Ù\x85Ø«Ù\x8aØ± Ù\x84Ù\x84Ø¬Ø¯Ù\x84 Ù\x81Ù\x8a Ø´Ø±Ù\x82 Ø§Ù\x84Ø¨Ù\x84Ø§Ø¯. Ù\x88Ù\x82Ø§Ù\x84 Ø±Ù\x88Ù\x85Ø§Ù\x86 Ù\x84Ù\x8aØ§Ø¬Ù\x8aÙ\x86Ø\x8c Ø±Ø¦Ù\x8aØ³ Ù\x84Ø¬Ù\x86Ø© Ø§Ù\x84Ù\x85ØªÙ\x85Ø±Ø¯Ù\x8aÙ\x86 Ù\x84Ù\x84Ø§Ù\x86ØªØ®Ø§Ø¨Ø§Øª Ù\x81Ù\x8a Ø¯Ù\x88Ù\x86Ù\x8aØªØ³Ù\x83 Ø¥Ù\x86 Ø§Ù\x84Ø§Ù\x86Ø¶Ù\x85Ø§Ù\x85 Ù\x84Ø±Ù\x88Ø³Ù\x8aØ§ "Ù\x82Ø¯ Ù\x8aÙ\x83Ù\x88Ù\x86 Ø®Ø·Ù\x88Ø© Ù\x85Ù\x86Ø§Ø³Ø¨Ø©".\n'
ja_text = 'ã\x82\x84ã\x81£ã\x81\x9f!'

class BaseTest(unittest.TestCase):

    def setUp(self):
        self.en_seq = Sequence(en_text)
        self.ar_seq = Sequence(ar_text)
        self.ja_seq = Sequence(ja_text)
        self.en_sent = SentenceTokenizer(locale='en')
        self.ar_sent = SentenceTokenizer(locale='ar')
        self.ja_sent = SentenceTokenizer(locale='ja')
        self.en_word = WordTokenizer(locale='en')
        self.ar_word = WordTokenizer(locale='ar')
        self.ja_word = WordTokenizer(locale='ja')
        self.en_sents = self.en_sent.transform(self.en_seq)
        self.ar_sents = self.ar_sent.transform(self.ar_seq)
        self.ja_sents = self.ja_sent.transform(self.ja_seq)
        self.en_words = self.en_word.transform(self.en_seq)
        self.ar_words = self.ar_word.transform(self.ar_seq)
        self.ja_words = self.ja_word.transform(self.ja_seq)

    def tearDown(self):
        pass

    def test_sentences_count(self):
        ' Sentence segmentation produces correct number of sentences.'
        self.assertEqual(5, len(self.en_sents))
        self.assertEqual(2, len(self.ar_sents))
        self.assertEqual(1, len(self.ja_sents))

    def test_redundant_idx(self):
        ' Test if there are redundant indices.'
        self.assertEqual(len(self.en_sents.idx), len(set(self.en_sents.idx)))
        self.assertEqual(len(self.ar_sents.idx), len(set(self.ar_sents.idx)))
        self.assertEqual(len(self.ja_sents.idx), len(set(self.ja_sents.idx)))
        self.assertEqual(len(self.en_words.idx), len(set(self.en_words.idx)))
        self.assertEqual(len(self.ar_words.idx), len(set(self.ar_words.idx)))
        self.assertEqual(len(self.ja_words.idx), len(set(self.ja_words.idx)))

    def test_boundaries(self):
        ' Sentence boundaries should be also word boundaries.'
        self.assertTrue(set(self.en_sents.idx).issubset(set(self.en_words.idx)))
        self.assertTrue(set(self.ar_sents.idx).issubset(set(self.ar_words.idx)))
        self.assertTrue(set(self.ja_sents.idx).issubset(set(self.ja_words.idx)))

    def test_transformations_equal(self):
        ' Word toeknization over text is equal to over sentences.'
        idx1 = self.en_words.idx
        idx2 = self.en_word.transform(self.en_sents).idx
        self.assertListEqual(idx1, idx2)
        idx1 = self.ar_words.idx
        idx2 = self.ar_word.transform(self.ar_sents).idx
        self.assertListEqual(idx1, idx2)
        idx1 = self.ja_words.idx
        idx2 = self.ja_word.transform(self.ja_sents).idx
        self.assertListEqual(idx1, idx2)
if (__name__ == '__main__'):
    unittest.main()

