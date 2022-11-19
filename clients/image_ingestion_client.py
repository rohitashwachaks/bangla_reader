import os
from common.config import LOCAL_PATH, LEGEND_FILENAME
import pandas as pd


class ImageReader_Client:
    def __init__(self) -> None:
        self._image_root_path = os.path.join(LOCAL_PATH, 'img')

        self.__load_legend__()
        return

    def __load_legend__(self)->None:
        legend_file = os.path.join(LOCAL_PATH, LEGEND_FILENAME)
        print(legend_file)
        self._legend = None
        try:
            self._legend = pd.read_csv(legend_file, header=None, names=['index', 'district_bn']).set_index('index').to_dict()
            self._legend = self._legend['district_bn']
        except Exception as ex:
            print(f'Failed to load legend file.\n {ex}')

    @property
    def legend(self):
        return self._legend




