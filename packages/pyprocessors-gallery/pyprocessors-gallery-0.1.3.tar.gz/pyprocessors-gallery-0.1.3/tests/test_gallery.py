
from typing import List
from pyprocessors_gallery.gallery import GalleryProcessor, GalleryParameters
from pymultirole_plugins.v1.schema import Document


def test_gallery():
    model = GalleryProcessor.get_model()
    model_class = model.construct().__class__
    assert model_class == GalleryParameters
    processor = GalleryProcessor()
    parameters = GalleryParameters()
    docs: List[Document] = processor.process([Document(text="Test gallery", metadata=parameters.dict())], parameters)
    assert len(docs[0].annotations) > 0
