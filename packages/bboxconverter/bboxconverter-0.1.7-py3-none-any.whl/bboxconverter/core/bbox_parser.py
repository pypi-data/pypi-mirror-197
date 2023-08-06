"""

Attributes
----------
FORMAT : list
    List of supported formats. Can be one of the following: 'voc', 'coco', 'yolo', 'jsonlines'

TYPES : list
    List of supported bounding box types. Can be one of the following: 'tlbr', 'tlwh', 'cwh'
"""
from pandas.core.frame import DataFrame
from sklearn.model_selection import GroupShuffleSplit
from bboxconverter.core.bbox import BBox, TLBR_BBox, TLWH_BBox, CWH_BBox
from bboxconverter.io.writer_coco import to_coco
from bboxconverter.io.writer_yolo import to_yolo
from bboxconverter.io.writer_pascal_voc import to_pascal_voc
from pathlib import Path
from shutil import copy

FORMAT = ['voc', 'coco', 'yolo', 'jsonlines']
TYPES = ['tlbr', 'tlwh', 'cwh']


class BboxParser():
    """
    The BboxParser class is used to ingest bounding boxes from various format into a pandas dataframe and output them in various formats.
    """

    data: DataFrame = None
    bbox_type: str = None

    def __init__(self, data: DataFrame, bbox_type) -> None:
        """
        Initialize BboxParser object

        Parameters
        ----------
        data : DataFrame
            Dataframe containing generic bounding boxes. Could contains some of the following columns:
                -'class_name'
                -'file_path'
                -'x_min'
                -'y_min'
                -'x_max'
                -'y_max'
                -'x_center'
                -'y_center'
                -'width'
                -'height'
                -'confidence'
                -'image_height'
                -'image_width'
                -'image_channels'

        bbox_type : str
            Type of bounding box. Can be one of the following: 'tlbr', 'tlwh', 'cwh'
        """
        self.data = data
        self.bbox_type = bbox_type

    def create_bbox(self, bbox_type: str, **kwargs) -> BBox:
        """
        Create bounding box object from a dictionary of parameters

        Parameters
        ----------
        bbox_type : str
            Type of bounding box. Can be one of the following: 'tlbr', 'tlwh', 'cwh'
        **kwargs : dict
            Dictionary of parameters for bounding box
        """
        if bbox_type == 'tlbr':
            return TLBR_BBox(**kwargs)
        if bbox_type == 'tlwh':
            return TLWH_BBox(**kwargs)
        if bbox_type == 'cwh':
            return CWH_BBox(**kwargs)
        return None

    def create_data_splits(self,
                           output_path,
                           train_size=0.8,
                           test_size=0.2,
                           save_func=to_coco):
        # Group split
        splitter = GroupShuffleSplit(
            train_size=train_size,
            test_size=test_size,
            n_splits=1,
            random_state=7
        )
        split = splitter.split(self.data, groups=self.data['file_path'])
        train_inds, test_inds = next(split)
        train = self.data.iloc[train_inds]
        test = self.data.iloc[test_inds]

        # Directory management
        annotation_file_name = Path(output_path).name
        train_folder = Path(output_path).parent / 'train'
        test_folder = Path(output_path).parent / 'test'
        train_image_folder = train_folder / 'images'
        test_image_folder = test_folder / 'images'
        for folder in [
                train_folder, test_folder, train_image_folder,
                test_image_folder
        ]:
            folder.mkdir(parents=True, exist_ok=True)

        # Copy images
        train['file_path'].apply(
            lambda x:
            copy(
                Path(output_path).parent / x,
                train_image_folder / Path(x).name
            )
        )
        test['file_path'].apply(
            lambda x:
            copy(
                Path(output_path).parent / x,
                test_image_folder / Path(x).name
            )
        )

        # Save annotations
        save_func(train, str(train_folder / annotation_file_name))
        save_func(test, str(test_folder / annotation_file_name))

    def export(self,
               output_path: "str | Path",
               format: str,
               split=False,
               train_size=0.8,
               test_size=0.2) -> None:
        """
        Export bounding boxes to a popular file format:

        - "voc" => Pascal VOC 
        - "coco" => COCO
        - "yolo" => YOLO
        - "jsonlines" => Sagemaker

        If split is False, the output file will contain all bounding boxes. If split is True, the output file will contain the train and test split of the dataset.

        Parameters
        ----------
        output_path : str | Path
            Path to output file. The path should include the file name and extension.
        format : str
            Format of output file. Can be one of the following: 'voc', 'coco', 'yolo', 'sagemaker'
        type : str
            Type of bounding box. Can be one of the following: 'tlbr', 'tlwh', 'cwh'
        split : bool
            Split the dataset into train and test using scikit-learn train_test_split function.
        train_size : float
            If float, should be between 0.0 and 1.0 and represent the proportion of the dataset to include in the test split. If int, represents the absolute number of test samples. If None, the value is set to the complement of the train size.
        test_size : float
            If float, should be between 0.0 and 1.0 and represent the proportion of the dataset to include in the train split. If int, represents the absolute number of train samples. If None, the value is automatically set to the complement of the test size.

        """
        # Check if bounding box type is set
        type = self.bbox_type
        assert type is not None
        if type not in TYPES:
            raise ValueError(f"Invalid bbox type: {type}")

        # Set export to file function
        save_func = {
            'coco': to_coco,
            'voc': to_pascal_voc,
            'yolo': to_yolo
        }.get(format, None)
        if save_func is None:
            raise ValueError(f"Invalid save function: {format}")

        format_type = {'coco': 'tlwh', 'voc': 'tlbr', 'yolo': 'cwh'}

        # Check if conversion is needed
        if type == format_type[format]:
            if split:
                self.create_data_splits(output_path, train_size, test_size,
                                        save_func)
            else:
                save_func(self.data, output_path)
            return

        # Set conversion function
        format_map = {
            ('voc', 'tlwh'): TLBR_BBox.from_TLWH,
            ('voc', 'cwh'): TLBR_BBox.from_CWH,
            ('coco', 'tlbr'): TLWH_BBox.from_TLBR,
            ('coco', 'cwh'): TLWH_BBox.from_CWH,
            ('yolo', 'tlbr'): CWH_BBox.from_TLBR,
            ('yolo', 'tlwh'): CWH_BBox.from_TLWH,
        }

        # Get conversion function
        convert_func = format_map.get((format.lower(), self.bbox_type))
        if convert_func is None:
            raise ValueError(f"Invalid export format: {format}")

        # Transform data to bounding boxes
        bboxes = self.data.drop(
            columns=['image_channel'], errors='ignore').apply(
                lambda x: self.create_bbox(self.bbox_type, **x.to_dict()),
                axis=1)

        # Serialize bounding boxes
        bboxes = bboxes.apply(lambda x: convert_func(x).to_dict())
        df_bbox = DataFrame.from_records(bboxes)

        # Save to file
        if split:
            self.create_data_splits(output_path, train_size, test_size,
                                    save_func)
        else:
            save_func(df_bbox, output_path)

    def to_csv(self, output_path: "str | Path", type) -> None:
        """
        Export bounding boxes to a csv file.

        Parameters
        ----------
        output_path : str | Path
            Path to output file
        type : str
            Type of bounding box. Can be one of the following: 'tlbr', 'tlwh', 'cwh'
        """
        assert self.bbox_type is not None
        if type not in TYPES:
            raise ValueError(f"Invalid bbox type: {type}")

        # Conversion function map (output_type, input_bbox_type)
        # Each type should have two functions to convert from TLBR, TLWH, CWH
        type_map = {
            ('tlbr', 'tlwh'): TLBR_BBox.from_TLWH,
            ('tlbr', 'cwh'): TLBR_BBox.from_CWH,
            ('tlwh', 'tlbr'): TLWH_BBox.from_TLBR,
            ('tlwh', 'cwh'): TLWH_BBox.from_CWH,
            ('cwh', 'tlbr'): CWH_BBox.from_TLBR,
            ('cwh', 'tlwh'): CWH_BBox.from_TLWH,
        }

        if type == self.bbox_type:
            # No conversion needed
            self.data.to_csv(output_path, index=False)
            return

        # Get conversion function
        convert_func = type_map.get((type, self.bbox_type))

        if convert_func is None:
            raise ValueError(f"Invalid bbox type: {type}")

        # Transform data to bounding boxes
        bboxes = self.data.drop(
            columns=['image_channel'], errors='ignore').apply(
                lambda x: self.create_bbox(self.bbox_type, **x.to_dict()),
                axis=1)

        # Serialize bounding boxes
        bboxes = bboxes.apply(lambda x: convert_func(x).to_dict())

        # Save to file
        DataFrame.from_records(bboxes).to_csv(output_path, index=False)

    def __str__(self) -> str:
        return self.data.to_string()
