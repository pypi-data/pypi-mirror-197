import json
import os
import re
from typing import List

import pysbd
from sentence_splitter import SentenceSplitter


class Exciton_SBD(object):
    def __init__(self, language: str) -> None:
        HOME = os.path.expanduser("~")
        MODEL_DIR = "exciton/models/nlp/sentence_tokenizer"
        with open(f"{HOME}/{MODEL_DIR}/exciton_eos.json") as fp:
            self.eos = json.load(fp)
        self.pattern = re.compile("|".join(self.eos[language]))

    def split(self, text: str) -> List[str]:
        sents = []
        last_pos = 0
        for itm in self.pattern.finditer(text):
            if itm.span()[1] < len(text):
                wd = text[itm.span()[1]]
                if wd != " ":
                    continue
            sen = text[last_pos : itm.span()[1]].strip()
            sents.append(sen)
            last_pos = itm.span()[1]
        if last_pos < len(text):
            sen = text[last_pos:].strip()
            sents.append(sen)
        return sents


class Sentence_Tokenizer(object):
    def __init__(self) -> None:
        HOME = os.path.expanduser("~")
        MODEL_DIR = "exciton/models/nlp/sentence_tokenizer"
        with open(f"{HOME}/{MODEL_DIR}/support_languages.json") as fp:
            self.support_languages = json.load(fp)
        self.worker = {}
        lang_pysbd = [
            sen["code"] for sen in self.support_languages if sen["sbd"] == "pysbd"
        ]
        for lang in lang_pysbd:
            self.worker[lang] = pysbd.Segmenter(language=lang, clean=False).segment
        lang_ss = [
            sen["code"] for sen in self.support_languages if sen["sbd"] == "sentsplit"
        ]
        for lang in lang_ss:
            self.worker[lang] = SentenceSplitter(language=lang).split
        lang_exciton = [
            sen["code"] for sen in self.support_languages if sen["sbd"] == "exciton"
        ]
        for lang in lang_exciton:
            self.worker[lang] = Exciton_SBD(language=lang).split

    def get_support_languages(self):
        langs = [
            {"code": itm["code"], "name": itm["name"]} for itm in self.support_languages
        ]
        return langs

    def predict(self, source: str, source_lang: str) -> List[str]:
        self.worker[source_lang](source)
        return [sen.strip() for sen in self.worker[source_lang](source)]
