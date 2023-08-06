import json
import re
from pathlib import Path

import pytest
from dirty_equals import HasLen, IsPartialDict, IsStr, IsList
from pymultirole_plugins.v1.schema import Document, Annotation

from pyprocessors_afp_entities.afp_entities import (
    AFPEntitiesProcessor,
    AFPEntitiesParameters,
    ConsolidationType,
    group_annotations,
    is_suspicious,
)


def test_model():
    model = AFPEntitiesProcessor.get_model()
    model_class = model.construct().__class__
    assert model_class == AFPEntitiesParameters


# Arrange
@pytest.fixture
def original_doc():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/afp_ner_fr-document-test.json")
    with source.open("r") as fin:
        doc = json.load(fin)
        original_doc = Document(**doc)
        return original_doc


# Arrange
@pytest.fixture
def original_doc2():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/afp_ner_fr-document-test2.json")
    with source.open("r") as fin:
        doc = json.load(fin)
        original_doc = Document(**doc)
        return original_doc


# Arrange
@pytest.fixture
def original_doc_en():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/afp_ner_en-document-test.json")
    with source.open("r") as fin:
        doc = json.load(fin)
        original_doc = Document(**doc)
        return original_doc


def by_linking(a: Annotation):
    if a.terms:
        links = sorted({t.lexicon.split("_")[0] for t in a.terms})
        return "+".join(links)
    else:
        return "candidate"


def test_afp_entities_linker(original_doc):
    # linker
    doc = original_doc.copy(deep=True)
    processor = AFPEntitiesProcessor()
    parameters = AFPEntitiesParameters(type=ConsolidationType.linker)
    docs = processor.process([doc], parameters)
    conso: Document = docs[0]
    assert conso.altTexts == HasLen(1)
    altText = conso.altTexts[0]
    FINGERPRINT = re.compile(r"([QE]\d+[ ]?)+")
    assert altText.dict() == IsPartialDict(
        name="fingerprint", text=IsStr(regex=FINGERPRINT)
    )
    assert len(conso.annotations) < len(original_doc.annotations)
    conso_groups = group_annotations(conso, by_linking)
    assert len(conso_groups["candidate"]) == 8
    assert len(conso_groups["person"]) == 2
    persons = [r.value.dict() for r in conso_groups["person"].ranges()]
    assert persons == IsList(
        IsPartialDict(
            label="AFPPerson",
            text="Frank Garnier",
            terms=IsList(
                IsPartialDict(identifier=IsStr(regex=r"^afpperson.*")), length=1
            ),
        ),
        IsPartialDict(
            label="AFPPerson",
            text="Werner Baumann",
            terms=IsList(
                IsPartialDict(identifier=IsStr(regex=r"^afpperson.*")), length=1
            ),
        ),
        length=2,
    )
    assert len(conso_groups["wikidata"]) == 10
    assert len(conso_groups["location+wikidata"]) == 1
    assert len(conso_groups["organization+wikidata"]) == 2


def test_afp_entities_linker2(original_doc2):
    # linker
    doc = original_doc2.copy(deep=True)
    processor = AFPEntitiesProcessor()
    parameters = AFPEntitiesParameters(type=ConsolidationType.linker)
    docs = processor.process([doc], parameters)
    conso: Document = docs[0]
    assert conso.altTexts == HasLen(1)
    altText = conso.altTexts[0]
    FINGERPRINT = re.compile(r"([QE]\d+[ ]?)+")
    assert altText.dict() == IsPartialDict(
        name="fingerprint", text=IsStr(regex=FINGERPRINT)
    )
    assert len(conso.annotations) < len(original_doc2.annotations)
    conso_groups = group_annotations(conso, by_linking)
    assert len(conso_groups["candidate"]) == 1
    assert len(conso_groups["person"]) == 1
    persons = [r.value.dict() for r in conso_groups["person"].ranges()]
    assert persons == IsList(
        IsPartialDict(
            label="AFPPerson",
            text="Jean-Marc Berthon",
            terms=IsList(
                IsPartialDict(identifier=IsStr(regex=r"^afpperson.*")), length=1
            ),
        ),
        length=1,
    )
    assert len(conso_groups["location+wikidata"]) == 1
    locations = [r.value.dict() for r in conso_groups["location+wikidata"].ranges()]
    assert locations == IsList(
        IsPartialDict(
            label="AFPLocation",
            text="France",
            terms=IsList(
                IsPartialDict(identifier=IsStr(regex=r"^afplocation.*")),
                IsPartialDict(identifier=IsStr(regex=r"^Q.*")), length=2
            ),
        ),
        length=1,
    )
    assert len(conso_groups["person+wikidata"]) == 1
    persons = [r.value.dict() for r in conso_groups["person+wikidata"].ranges()]
    assert persons == IsList(
        IsPartialDict(
            label="AFPPerson",
            text="Elisabeth Borne",
            terms=IsList(
                IsPartialDict(identifier=IsStr(regex=r"^afpperson.*")),
                IsPartialDict(identifier=IsStr(regex=r"^Q.*")), length=2
            ),
        ),
        length=1,
    )


def test_afp_entities_whitelist():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/afp_ner_fr-document-test-whitelist2.json")
    with source.open("r") as fin:
        doc = json.load(fin)
        original_doc = Document(**doc)
    # linker
    doc = original_doc.copy(deep=True)
    processor = AFPEntitiesProcessor()
    parameters = AFPEntitiesParameters()
    docs = processor.process([doc], parameters)
    conso: Document = docs[0]
    assert conso.altTexts == HasLen(1)
    altText = conso.altTexts[0]
    FINGERPRINT = re.compile(r"([QE]\d+[ ]?)+")
    assert altText.dict() == IsPartialDict(
        name="fingerprint", text=IsStr(regex=FINGERPRINT)
    )
    assert len(conso.annotations) < len(original_doc.annotations)
    conso_groups = group_annotations(conso, by_linking)
    assert len(conso_groups["candidate"]) == 2
    assert len(conso_groups["person"]) == 2
    persons = [r.value.dict() for r in conso_groups["person"].ranges()]
    assert persons == IsList(
        IsPartialDict(
            label="AFPPerson",
            text="Máxima des Pays-Bas",
            terms=IsList(
                IsPartialDict(identifier=IsStr(regex=r"^afpperson.*")), length=1
            ),
        ),
        IsPartialDict(
            label="AFPPerson",
            text="Lil Nas X",
            terms=IsList(
                IsPartialDict(identifier=IsStr(regex=r"^afpperson.*")), length=1
            ),
        ),
        length=2,
    )
    assert len(conso_groups["location+wikidata"]) == 10
    assert len(conso_groups["organization+wikidata"]) == 3
    assert len(conso_groups["person+wikidata"]) == 1
    assert len(conso_groups["wikidata"]) == 1
    assert len(conso_groups["location"]) == 2


def test_afp_entities_suspicious():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/afp_ner_es-document-test.json")
    with source.open("r") as fin:
        doc = json.load(fin)
        original_doc = Document(**doc)
    # linker
    doc = original_doc.copy(deep=True)
    processor = AFPEntitiesProcessor()
    parameters = AFPEntitiesParameters()
    docs = processor.process([doc], parameters)
    conso: Document = docs[0]
    assert len(conso.annotations) < len(original_doc.annotations)
    for a in conso.annotations:
        assert not is_suspicious(a)


def test_afp_entities_linker_en(original_doc_en):
    # linker
    doc = original_doc_en.copy(deep=True)
    processor = AFPEntitiesProcessor()
    parameters = AFPEntitiesParameters(type=ConsolidationType.linker)
    docs = processor.process([doc], parameters)
    conso: Document = docs[0]
    assert conso.altTexts == HasLen(1)
    altText = conso.altTexts[0]
    FINGERPRINT = re.compile(r"([QE]\d+[ ]?)+")
    assert altText.dict() == IsPartialDict(
        name="fingerprint", text=IsStr(regex=FINGERPRINT)
    )
