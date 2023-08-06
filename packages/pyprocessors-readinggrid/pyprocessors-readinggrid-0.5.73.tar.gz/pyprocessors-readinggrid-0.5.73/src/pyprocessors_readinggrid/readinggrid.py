from typing import Type, List, cast, Optional

from collections_extended import RangeMap
from pydantic import BaseModel, Field
from pymultirole_plugins.v1.processor import ProcessorBase, ProcessorParameters
from pymultirole_plugins.v1.schema import Document, Sentence, AltText


class ReadingGridParameters(ProcessorParameters):
    separator: str = Field(
        "", description="Separator to append to the remaining sentences"
    )
    keep: bool = Field(True,
                       description="If checked, keep the sentence if it contains one of the labels. if not remove it.",
                       extra="label")
    labels: Optional[List[str]] = Field(None,
                                        description="Keep/remove the sentence if it contains one of these labels.",
                                        extra="label")
    as_altText: str = Field(
        None,
        description="""If defined generate the output as an alternative text of the input document,
    if not replace the text of the input document.""",
    )


class ReadingGridProcessor(ProcessorBase):
    """ "A processor that generate a reduced/focussed version of the document filtering somes sentences according to
    their annotations
    """

    def process(
            self, documents: List[Document], parameters: ProcessorParameters
    ) -> List[Document]:
        params: ReadingGridParameters = cast(ReadingGridParameters, parameters)
        for document in documents:
            sentences = []
            annotations = []
            start = 0
            text = ""
            separator = params.separator
            labels = params.labels or None
            use_altText = params.as_altText is not None and len(params.as_altText) > 0
            if not separator.startswith("\n"):
                separator = "\n" + separator
            if not separator.endswith("\n"):
                separator = separator + "\n"
            if document.sentences is not None and document.annotations is not None:
                sentence_map = RangeMap()
                for s in document.sentences:
                    if s.end > s.start:
                        sentence_map[s.start: s.end] = []
                for a in document.annotations:
                    sentence_map[a.start].append(a)
                for sent in sentence_map.ranges():
                    ann_list = sent.value
                    keep = keep_or_remove(ann_list, labels, params.keep)
                    if keep:
                        sstart = start
                        send = sstart + (sent.stop - sent.start)
                        sentences.append(Sentence(start=sstart, end=send))
                        text += document.text[sent.start: sent.stop] + separator
                        if not use_altText:
                            for a in ann_list:
                                astart = a.start - sent.start
                                aend = a.end - sent.start
                                a.start = sstart + astart
                                a.end = sstart + aend
                                annotations.append(a)
                        start = len(text)
            if text.endswith(separator):
                text = text[: -len(separator)]
            if use_altText:
                document.altTexts = document.altTexts or []
                altTexts = [
                    alt for alt in document.altTexts if alt.name != params.as_altText
                ]
                altTexts.append(AltText(name=params.as_altText, text=text))
                document.altTexts = altTexts
            else:
                document.sentences = sentences
                document.annotations = annotations
                document.text = text
        return documents

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return ReadingGridParameters


def keep_or_remove(ann_list, labels, keep):
    if labels is not None and len(labels) > 0:
        anns = [a for a in ann_list if a.labelName in labels]
        if len(anns) >= 1:
            return keep
        else:
            return not keep
    return len(ann_list) >= 1
