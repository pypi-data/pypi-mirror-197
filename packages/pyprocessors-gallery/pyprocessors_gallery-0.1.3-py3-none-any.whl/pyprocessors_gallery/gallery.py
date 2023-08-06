from enum import Enum
from typing import Type, List, cast, Dict, Optional
from pydantic import BaseModel, Field
from pymultirole_plugins.v1.processor import ProcessorParameters, ProcessorBase
from pymultirole_plugins.v1.schema import Document


class GalleryEnum(str, Enum):
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'
    E = 'E'
    F = 'F'


class GalleryOptions(BaseModel):
    foo: str = Field("foo", description="String value")
    bar: float = Field(1.2345, description="Float value")


class GalleryParameters(ProcessorParameters):
    options_val: GalleryOptions = Field(None, description="Options value")
    str_value: str = Field("string", description="String value")
    float_value: float = Field(1.2345, description="Float value")
    int_value: int = Field(1, description="Integer value")
    bool_value: bool = Field(True, description="Boolean value")
    advanced: str = Field(None,
                          description="Advanced parameter (Hidden by default)",
                          extra="advanced")
    internal: str = Field(None,
                          description="Internal parameter (Always hidden)",
                          extra="internal")
    one_json: Optional[str] = Field(None, description="""Json array with a very long description with [markdown](https://www.markdownguide.org)<ol>
        <li>text in **bold**
        <li>text in <em>italic</em>
        <li>block of `code`
        </ol>""", extra="json")
    one_label: Optional[str] = Field(None, description="One label", extra="label")
    label2json_mapping: Dict[str, str] = Field(None, description="Label to json mapping", extra="key:label,val:json")
    one_lang: Optional[str] = Field(None, description="One language", extra="language")
    lang2json_mapping: Dict[str, str] = Field(None, description="Language to json mapping",
                                              extra="key:language,val:json")
    many_labels: List[str] = Field(None, description="List of labels", extra="label")
    one_lexicon: str = Field(None, description="One lexicon", extra="lexicon")
    one_enum: GalleryEnum = Field(GalleryEnum.A,
                                  description="One enum with default value")
    lexicon2enum_mapping: Dict[str, GalleryEnum] = Field(None,
                                                         description="Lexicon to component enum",
                                                         extra="key:lexicon")
    many_enums: List[GalleryEnum] = Field(None,
                                  description="List of values from enum")
    label2many_enums_mapping: Dict[str, List[GalleryEnum]] = Field(None, description="Label to json mapping", extra="key:label")


class GalleryProcessor(ProcessorBase):
    """[Gallery](https://fr.wikipedia.org/wiki/Gallery) processor .
    #languages:en,fr,de
    #needs-segments
    """

    def process(self, documents: List[Document], parameters: ProcessorParameters) \
            -> List[Document]:
        params: GalleryParameters = \
            cast(GalleryParameters, parameters)
        return documents

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return GalleryParameters
