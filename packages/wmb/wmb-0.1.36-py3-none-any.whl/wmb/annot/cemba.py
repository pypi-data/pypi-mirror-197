import numpy as np
import pandas as pd

from .annot import CellAnnotation
from ..brain_region import brain


def add_reads_fc_per_plate(cell_meta, plate_col='Plate', reads_col='FinalmCReads'):
    # fold to plate median final reads
    total_fc = []
    for plate, plate_df in cell_meta.groupby(plate_col):
        fc = plate_df[reads_col] / plate_df[reads_col].median()
        total_fc.append(fc)
    total_fc = pd.concat(total_fc)
    return np.log2(total_fc)


class CEMBAmCCellAnnotation(CellAnnotation):
    __slots__ = ()

    def __init__(self, annot_path, metadata):
        super().__init__(annot_path)

        self['FinalReadsFoldToPlate'] = add_reads_fc_per_plate(
            metadata, reads_col='FinalmCReads')

        # add snmC specific attributes
        self['DissectionRegion'] = self.get_index('cell').map(metadata['DissectionRegion'])

        metadata['MajorRegion'] = metadata['DissectionRegion'].map(
            brain.map_dissection_region_to_major_region(region_type='CEMBA'))
        self['MajorRegion'] = self.get_index('cell').map(metadata['MajorRegion'])

        metadata['SubRegion'] = metadata['DissectionRegion'].map(
            brain.map_dissection_region_to_sub_region(region_type='CEMBA'))
        self['SubRegion'] = self.get_index('cell').map(metadata['SubRegion'])
        return


class CEMBAm3CCellAnnotation(CellAnnotation):
    __slots__ = ()

    def __init__(self, annot_path, metadata):
        super().__init__(annot_path)

        self['FinalReadsFoldToPlate'] = add_reads_fc_per_plate(
            metadata, reads_col='FinalmCReads')

        # add snm3C specific attributes
        self['DissectionRegion'] = self.get_index('cell').map(metadata['DissectionRegion'])

        metadata['MajorRegion'] = metadata['DissectionRegion'].map(
            brain.map_dissection_region_to_major_region(region_type='CEMBA_3C'))
        self['MajorRegion'] = self.get_index('cell').map(metadata['MajorRegion'])

        metadata['SubRegion'] = metadata['DissectionRegion'].map(
            brain.map_dissection_region_to_sub_region(region_type='CEMBA_3C'))
        self['SubRegion'] = self.get_index('cell').map(metadata['SubRegion'])
        return


class CEMBAATACCellAnnotation(CellAnnotation):
    __slots__ = ()

    def __init__(self, annot_path):
        super().__init__(annot_path)

        cemba_ids = self.get_index('cell').map(lambda i: i.split('_')[1])
        cemba_id_to_dr = brain.map_cemba_id_to_dissection_region('CEMBA')
        dissection_regions = cemba_ids.map(cemba_id_to_dr)
        self['DissectionRegion'] = dissection_regions

        major_map = brain.map_dissection_region_to_major_region(region_type='CEMBA')
        self['MajorRegion'] = dissection_regions.map(major_map)

        sub_map = brain.map_dissection_region_to_sub_region(region_type='CEMBA')
        self['SubRegion'] = dissection_regions.map(sub_map)
        return


class CEMBAEpiRetroCellAnnotation(CellAnnotation):
    __slots__ = ()

    def __init__(self, annot_path, metadata):
        super().__init__(annot_path)

        return
