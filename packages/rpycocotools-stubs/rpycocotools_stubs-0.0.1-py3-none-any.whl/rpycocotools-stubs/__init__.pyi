__version__ = "0.0.1"

class Category:
    id: int
    name: str
    supercategory: str

    def __init__(self, id: int, name: str, supercategory: str) -> None: ...

class COCO:
    # anns: dict[int, Annotation]
    # dataset: Dataset
    cats: dict[int, Category]
    # imgs: dict[int, Image]
    # imgToAnns: dict[int, list[Annotation]]

    def __init__(self, annotation_path: str, image_folder_path: str) -> None: ...
    def visualize_img(self, img_id: int) -> None: ...
