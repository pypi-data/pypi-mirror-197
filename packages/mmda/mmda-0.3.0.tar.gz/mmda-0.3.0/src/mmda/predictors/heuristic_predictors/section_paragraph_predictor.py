"""

SectionParagraphPredictor. Returns output like:
    [
        {"section": ..., "text": ...},
        ...
    ]

@kylel

"""


from functools import partial
from typing import Dict, List, Tuple

from mmda.predictors.base_predictors.base_predictor import BasePredictor
from mmda.types import *


class SectionParagraphPredictor(BasePredictor):

    REQUIRED_BACKENDS = None
    REQUIRED_DOCUMENT_FIELDS = ["blocks", "vila_span_groups"]

    def predict(self, document: Document) -> List[SpanGroup]:
        """Get paragraphs in a Document as a list of SpanGroup.

        Args:
            doc (Document): The document to process

        Returns:
            list[SpanGroup]: SpanGroups that appear to be paragraphs.
        """
        self._doc_field_checker(document)

        return NotImplementedError



def make_paragraphs_and_sections_from_vila(vila_span_groups: List[SpanGroup]) -> Tuple[List[SpanGroup], List[SpanGroup]]:

    def _make_sg(vila_span_group: SpanGroup, id: int) -> SpanGroup:
        return SpanGroup(
            # TODO: merge adjacent spans
            # from/to_json() because we need the boxes for hierarchy predictor
            spans=[Span.from_json(span.to_json()) for span in vila_span_group.spans],
            id=id
        )

    # Extract sections from VILA predictions and re-add boxes
    vila_sections = []
    vila_paragraphs = []
    i_section = -1
    i_paragraph = -1

    for vila_span_group in vila_span_groups:

        if vila_span_group.type == 'Section':
            i_section += 1
            section_sg = _make_sg(vila_span_group=vila_span_group, id=i_section)
            section_sg.metadata.text = vila_span_group.text.replace('\n', ' ')
            vila_sections.append(section_sg)
        # TODO: use `blocks` to partition paragraph finer-grained. handle indexing redundacy.
        elif vila_span_group.type == 'Paragraph':
            if len(vila_span_group.blocks) == 1:
                continue
            else:
                # TODO: stopped here -- split para based on blocks. if para is smaller than a block, that's ok.
                raise Exception
            i_paragraph += 1
            paragraph_sg = _make_sg(vila_span_group=vila_span_group, id=i_paragraph)
            paragraph_sg.metadata['section_id'] = i_section if i_section >= 0 else None
            vila_paragraphs.append(paragraph_sg)
        else:
            continue
    return vila_paragraphs, vila_sections

#
#
# paragraphs, sections = make_paragraphs_and_sections_from_vila(vila_span_groups=document.vila_span_groups)
# document.annotate(paragraphs=paragraphs, is_overwrite=True)
# document.annotate(sections=sections, is_overwrite=True)
# for paragraph in paragraphs:
#     section_id = paragraph.metadata.section_id
#     print(f'{paragraph.id}\t{section_id}\t{sections[section_id].text}\t{paragraph.text[:50]}')
#
