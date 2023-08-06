from functools import lru_cache

import numpy as np
import pandas as pd
import xarray as xr
from ALLCools.mcds import MCDS

from wmb.files import *
from ..annot import CEMBAmCCellAnnotation, CEMBAm3CCellAnnotation
from ..brain_region import brain
from ..genome import mm10


def _get_mapping_metric(path, pass_basic_qc_only=True):
    df = pd.read_csv(path, index_col=0)
    df.index.name = 'cell'
    if pass_basic_qc_only:
        df = df[df['PassBasicQC']].copy()
    return df


def _add_brain_region(df, region_type):
    df['CEMBARegion'] = df['DissectionRegion'].copy()
    df['DissectionRegion'] = df['DissectionRegion'].map(
        brain.map_cemba_id_to_dissection_region(region_type=region_type))
    df['MajorRegion'] = df['DissectionRegion'].map(
        brain.map_dissection_region_to_major_region(region_type=region_type))
    df['SubRegion'] = df['DissectionRegion'].map(
        brain.map_dissection_region_to_sub_region(region_type=region_type))
    return df


class CEMBASnmCAndSnm3C(AutoPathMixIn):
    def __init__(self):
        # mapping metric
        self.CEMBA_SNMC_MAPPING_METRIC_PATH = CEMBA_SNMC_MAPPING_METRIC_PATH
        self.CEMBA_SNMC_FULL_MAPPING_METRIC_PATH = CEMBA_SNMC_FULL_MAPPING_METRIC_PATH
        self.CEMBA_SNM3C_MAPPING_METRIC_PATH = CEMBA_SNM3C_MAPPING_METRIC_PATH
        self.CEMBA_SNM3C_FULL_MAPPING_METRIC_PATH = CEMBA_SNM3C_FULL_MAPPING_METRIC_PATH

        # cell level raw files
        self.CEMBA_SNMC_ALLC_PATH = CEMBA_SNMC_ALLC_PATH
        self.CEMBA_SNMC_MCG_ALLC_PATH = CEMBA_SNMC_MCG_ALLC_PATH
        self.CEMBA_SNM3C_ALLC_PATH = CEMBA_SNM3C_ALLC_PATH
        self.CEMBA_SNM3C_MCG_ALLC_PATH = CEMBA_SNM3C_MCG_ALLC_PATH
        self.CEMBA_SNM3C_CONTACT_PATH = CEMBA_SNM3C_CONTACT_PATH
        self.CEMBA_SNM3C_10K_RAW_COOL_PATH = CEMBA_SNM3C_10K_RAW_COOL_PATH
        self.CEMBA_SNM3C_25K_RAW_COOL_PATH = CEMBA_SNM3C_25K_RAW_COOL_PATH
        self.CEMBA_SNM3C_100K_RAW_COOL_PATH = CEMBA_SNM3C_100K_RAW_COOL_PATH
        self.CEMBA_SNM3C_10K_IMPUTED_COOL_PATH = CEMBA_SNM3C_10K_IMPUTED_COOL_PATH
        self.CEMBA_SNM3C_25K_IMPUTED_COOL_PATH = CEMBA_SNM3C_25K_IMPUTED_COOL_PATH
        self.CEMBA_SNM3C_100K_IMPUTED_COOL_PATH = CEMBA_SNM3C_100K_IMPUTED_COOL_PATH

        # CoolDS snm3C multi-sample zarr dataset
        self.CEMBA_SNM3C_L4REGION_COOL_DS_PATH_LIST = CEMBA_SNM3C_L4REGION_COOL_DS_PATH_LIST
        self.CEMBA_SNM3C_L4REGION_COOL_DS_SAMPLE_WEIGHTS_PATH = CEMBA_SNM3C_L4REGION_COOL_DS_SAMPLE_WEIGHTS_PATH
        self.CEMBA_SNM3C_L4REGION_COOL_DS_CHROMS_SIZES_PATH = CEMBA_SNM3C_L4REGION_COOL_DS_CHROMS_SIZES_PATH
        self.CEMBA_SNM3C_L4REGION_CHROM_25K_COOL_DS_PATH = CEMBA_SNM3C_L4REGION_CHROM_25K_COOL_DS_PATH
        self.CEMBA_SNM3C_L4REGION_CHROM_100K_COOL_DS_PATH = CEMBA_SNM3C_L4REGION_CHROM_100K_COOL_DS_PATH

        # dataset paths
        self.CEMBA_SNMC_MCDS_PATH = CEMBA_SNMC_MCDS_PATH
        self.CEMBA_SNM3C_MCDS_PATH = CEMBA_SNM3C_MCDS_PATH

        # CEMBA snm3C chromatin conformation matrix paths
        self.CEMBA_SNM3C_3C_CHROM100K_RAW_ZARR_PATH = CEMBA_SNM3C_3C_CHROM100K_RAW_ZARR_PATH
        self.CEMBA_SNM3C_3C_COMPARTMENT_ZARR_PATH = CEMBA_SNM3C_3C_COMPARTMENT_ZARR_PATH
        self.CEMBA_SNM3C_3C_DOMAIN_INSULATION_ZARR_PATH = CEMBA_SNM3C_3C_DOMAIN_INSULATION_ZARR_PATH
        self.CEMBA_SNM3C_LOOP_VALUES_AND_STATS_DS_PATH = CEMBA_SNM3C_LOOP_VALUES_AND_STATS_V2_DS_PATH
        self.CEMBA_SNM3C_CELL_TYPE_10K_MATRIX_ANOVA_PATH = CEMBA_SNM3C_CELL_TYPE_10K_MATRIX_ANOVA_PATH
        self.CEMBA_SNM3C_CELL_CLUSTER_10K_MATRIX_ANOVA_PATH = CEMBA_SNM3C_CELL_CLUSTER_10K_MATRIX_ANOVA_PATH

        self.CEMBA_SNM3C_LOOP_VALUES_DS_PATH = CEMBA_SNM3C_LOOP_VALUES_DS_PATH
        self.CEMBA_SNM3C_DOMAIN_BOUNDARY_AND_CHI2_DS_PATH = CEMBA_SNM3C_DOMAIN_BOUNDARY_AND_CHI2_DS_PATH
        self.CEMBA_SNM3C_DOMAIN_INSULATION_SCORE_DS_PATH = CEMBA_SNM3C_DOMAIN_INSULATION_SCORE_DS_PATH

        # other metadata
        self.CEMBA_LIU_2021_NATURE_SNMC_METADATA_PATH = CEMBA_LIU_2021_NATURE_SNMC_METADATA_PATH
        self.CEMBA_SNMC_OUTLIER_IDS_PATH = CEMBA_SNMC_OUTLIER_IDS_PATH
        self.CEMBA_SNM3C_OUTLIER_IDS_PATH = CEMBA_SNM3C_OUTLIER_IDS_PATH

        # annotation
        self.CEMBA_SNMC_CELL_TYPE_ANNOTATION_PATH = CEMBA_SNMC_CELL_TYPE_ANNOTATION_PATH
        self.CEMBA_SNM3C_CELL_TYPE_ANNOTATION_PATH = CEMBA_SNM3C_CELL_TYPE_ANNOTATION_PATH

        # gene chunk zarr path
        self.CEMBA_SNMC_GENE_CHUNK_ZARR_PATH = CEMBA_SNMC_GENE_CHUNK_ZARR_PATH
        self.CEMBA_SNM3C_GENE_CHUNK_ZARR_PATH = CEMBA_SNM3C_GENE_CHUNK_ZARR_PATH

        # cluster aggregate zarr path
        self.CEMBA_SNMC_CLUSTER_L4_SUM_ZARR_PATH = CEMBA_SNMC_CLUSTER_L4_SUM_ZARR_PATH
        self.CEMBA_SNM3C_CLUSTER_L4_SUM_ZARR_PATH = CEMBA_SNM3C_CLUSTER_L4_SUM_ZARR_PATH
        self.CEMBA_SNMC_CLUSTER_L4Region_SUM_ZARR_PATH = CEMBA_SNMC_CLUSTER_L4Region_SUM_ZARR_PATH
        self.CEMBA_SNM3C_CLUSTER_L4Region_SUM_ZARR_PATH = CEMBA_SNM3C_CLUSTER_L4Region_SUM_ZARR_PATH

        # BaseDS
        self.CEMBA_SNMC_BASE_DS_PATH_LIST = CEMBA_SNMC_BASE_DS_REMOTE_PATH_LIST
        self.CEMBA_SNM3C_BASE_DS_PATH_LIST = CEMBA_SNM3C_BASE_DS_REMOTE_PATH_LIST
        self.MM10_MC_TYPE_CODEBOOK_PATH = MM10_MC_TYPE_CODEBOOK_REMOTE_PATH

        # snmC DMR and Annotation
        self.CEMBA_SNMC_DMR_REGION_DS_PATH = CEMBA_SNMC_DMR_REGION_DS_REMOTE_PATH
        self.CEMBA_SNMC_DMR_MOTIF_SCAN_REGION_DS_PATH = CEMBA_SNMC_DMR_MOTIF_SCAN_REGION_DS_REMOTE_PATH
        self.CEMBA_SNMC_DMR_TF_AND_MOTIF_HITS_DS_REMOTE_PATH = CEMBA_SNMC_DMR_TF_AND_MOTIF_HITS_DS_REMOTE_PATH
        self.CEMBA_SNMC_DMR_REGION_DS_SAMPLE_CHUNK_PATH = CEMBA_SNMC_DMR_REGION_DS_SAMPLE_CHUNK_REMOTE_PATH
        self.CEMBA_SNMC_GROUPED_DMR_MC_REGION_DS_PATH = CEMBA_SNMC_GROUPED_DMR_MC_REGION_DS_PATH
        self.CEMBA_SNMC_GROUPED_DMR_ATAC_REGION_DS_PATH = CEMBA_SNMC_GROUPED_DMR_ATAC_REGION_DS_PATH
        self.CEMBA_SNMC_GROUPED_DMR_MOTIF_REGION_DS_PATH = CEMBA_SNMC_GROUPED_DMR_MOTIF_REGION_DS_PATH

        # Integration based other modalities at cluster level
        self.CEMBA_SNMC_TO_SNM3C_CLUSTER_MAP_PATH = CEMBA_SNMC_TO_SNM3C_CLUSTER_MAP_PATH
        self.CEMBA_SNMC_L4REGION_AIBS_TENX_COUNTS_ZARR_PATH = CEMBA_SNMC_L4REGION_AIBS_TENX_COUNTS_ZARR_PATH
        self.CEMBA_SNMC_DMR_ATAC_COUNT_ZARR_PATH = CEMBA_SNMC_DMR_ATAC_COUNT_ZARR_PATH
        self.CEMBA_SNMC_CHROM_10BP_ATAC_COUNT_ZARR_PATH = CEMBA_SNMC_CHROM_10BP_ATAC_COUNT_ZARR_PATH

        # snm3C DMR (regions are the same as snmC)
        self.CEMBA_SNM3C_DMR_REGION_DS_PATH = CEMBA_SNM3C_DMR_REGION_DS_REMOTE_PATH
        self.CEMBA_SNM3C_DMR_REGION_DS_SAMPLE_CHUNK_PATH = CEMBA_SNM3C_DMR_REGION_DS_SAMPLE_CHUNK_REMOTE_PATH

        # Palette
        self.CEMBA_CELL_TYPE_ANNOT_PALETTE_PATH = CEMBA_CELL_TYPE_ANNOT_PALETTE_PATH

        # internal variables
        self._mc_gene_mcds = None
        self._mc_cluster_gene_ds = None
        self._mc_cluster_gene_rna_ds = None
        self._m3c_gene_mcds = None
        self._m3c_cluster_gene_ds = None

        self._mc_annot = None
        self._m3c_annot = None

        # validate path or auto change prefix
        self._check_file_path_attrs()
        return

    def _open_mc_gene_mcds(self):
        self._mc_gene_mcds = MCDS.open(self.CEMBA_SNMC_GENE_CHUNK_ZARR_PATH)

    def _open_m3c_gene_mcds(self):
        self._m3c_gene_mcds = MCDS.open(self.CEMBA_SNM3C_GENE_CHUNK_ZARR_PATH)

    def _open_mc_cluster_gene_ds(self):
        ds = xr.open_zarr(self.CEMBA_SNMC_CLUSTER_L4Region_SUM_ZARR_PATH)
        self._mc_cluster_gene_ds = ds['geneslop2k-vm23_da']

        genome_sum = ds['chrom100k_da'].sum(dim='chrom100k')
        frac = (genome_sum.sel(count_type='mc') / genome_sum.sel(count_type='cov')).load()
        self._mc_cluster_gene_ds['cluster_overall_frac'] = frac
        return

    def _open_mc_cluster_gene_rna_ds(self):
        self._mc_cluster_gene_rna_ds = xr.open_zarr(self.CEMBA_SNMC_L4REGION_AIBS_TENX_COUNTS_ZARR_PATH)
        return

    def _open_m3c_cluster_gene_ds(self):
        ds = xr.open_zarr(self.CEMBA_SNM3C_CLUSTER_L4Region_SUM_ZARR_PATH)
        self._m3c_cluster_gene_ds = ds['geneslop2k-vm23_da']

        genome_sum = ds['chrom100k_da'].sum(dim='chrom100k')
        frac = (genome_sum.sel(count_type='mc') / genome_sum.sel(count_type='cov')).load()
        self._m3c_cluster_gene_ds['cluster_overall_frac'] = frac
        return

    def get_mc_mapping_metric(self, pass_basic_qc_only=True, remove_outlier_ids=True, select_cells=None):
        """
        Load the mapping metric for CEMBA snmC cells.

        Parameters
        ----------
        pass_basic_qc_only
            Only cells that pass basic QC are returned.
        remove_outlier_ids
            Remove cells that are outliers.
        select_cells
            Select cells with a list of id or path to a file containing a list of id.

        Returns
        -------
        pd.DataFrame
        """
        df = _get_mapping_metric(self.CEMBA_SNMC_MAPPING_METRIC_PATH, pass_basic_qc_only)
        if remove_outlier_ids:
            outlier_ids = pd.read_csv(self.CEMBA_SNMC_OUTLIER_IDS_PATH,
                                      index_col=0, header=None).index
            df = df[~df.index.isin(outlier_ids)].copy()
        if select_cells is not None:
            if isinstance(select_cells, (str, pathlib.Path)):
                select_cells = pd.read_csv(select_cells, index_col=0, header=None).index
            df = df[df.index.isin(select_cells)].copy()

        # add brain region
        df = _add_brain_region(df, region_type='CEMBA')
        return df

    def get_m3c_mapping_metric(self, pass_basic_qc_only=True, remove_outlier_ids=True, select_cells=None):
        """
        Load the mapping metric for CEMBA snm3C cells.

        Parameters
        ----------
        pass_basic_qc_only
            Only cells that pass basic QC are returned.
        remove_outlier_ids
            Remove cells that are outliers.
        select_cells
            Select cells with a list of id or path to a file containing a list of id.

        Returns
        -------
        pd.DataFrame
        """
        df = _get_mapping_metric(self.CEMBA_SNM3C_MAPPING_METRIC_PATH, pass_basic_qc_only)
        if remove_outlier_ids:
            outlier_ids = pd.read_csv(self.CEMBA_SNM3C_OUTLIER_IDS_PATH,
                                      index_col=0, header=None).squeeze().index
            df = df[~df.index.isin(outlier_ids)].copy()
        if select_cells is not None:
            if isinstance(select_cells, (str, pathlib.Path)):
                select_cells = pd.read_csv(select_cells, index_col=0, header=None).index
            df = df[df.index.isin(select_cells)].copy()

        # add brain region
        df = _add_brain_region(df, region_type='CEMBA_3C')
        return df

    def get_mc_m3c_mapping_metric(self, pass_basic_qc_only=True, remove_outlier_ids=True, select_cells=None):
        """
        Load the mapping metric for CEMBA snmC and snm3C cells.

        Parameters
        ----------
        pass_basic_qc_only
            Only cells that pass basic QC are returned.
        remove_outlier_ids
            Remove cells that are outliers.
        select_cells
            Select cells with a list of id or path to a file containing a list of id.

        Returns
        -------
        pd.DataFrame
        """
        df1 = self.get_mc_mapping_metric(pass_basic_qc_only, remove_outlier_ids)
        df2 = self.get_m3c_mapping_metric(pass_basic_qc_only, remove_outlier_ids)
        df = pd.concat([df1, df2])
        if 'Technology' in df:
            name_map = {i: i for i in df['Technology'].unique()}
            name_map['snmC-seq2'] = 'snmC-seq2&3'
            name_map['snmC-seq3'] = 'snmC-seq2&3'
            df['Technology2'] = df['Technology'].map(name_map)

        if select_cells is not None:
            if isinstance(select_cells, (str, pathlib.Path)):
                select_cells = pd.read_csv(select_cells, index_col=0, header=None).index
            df = df[df.index.isin(select_cells)].copy()
        return df

    def get_allc_path(self, dataset, allc_type):
        """
        read ALLC path series for certain dataset and allc_type

        Parameters
        ----------
        dataset
            Can be "mc", "m3c"
        allc_type
            Can be "full", "mcg". The mCG ALLC contains CpG only

        Returns
        -------
        Series of cell-id by ALLC path on GALE
        """
        dataset = dataset.lower()
        allc_type = allc_type.lower()

        def _read_file_paths(p):
            s = pd.read_csv(p, index_col=0).squeeze()
            s.index.name = 'cell'
            return s

        if dataset == 'mc' and allc_type == 'full':
            allc_paths = _read_file_paths(self.CEMBA_SNMC_ALLC_PATH)
        elif dataset == 'm3c' and allc_type == 'full':
            allc_paths = _read_file_paths(self.CEMBA_SNM3C_ALLC_PATH)
        elif dataset == 'mc' and allc_type == 'mcg':
            allc_paths = _read_file_paths(self.CEMBA_SNMC_MCG_ALLC_PATH)
        elif dataset == 'mc' and allc_type == 'mcg':
            allc_paths = _read_file_paths(self.CEMBA_SNM3C_MCG_ALLC_PATH)
        else:
            raise ValueError('Got invalid value for dataset or allc_type. '
                             'Check doc string for allowed values.')
        return allc_paths

    def get_m3c_contact_path(self):
        s = pd.read_csv(self.CEMBA_SNM3C_CONTACT_PATH, index_col=0).squeeze()
        s.index.name = 'cell'
        return s

    def get_m3c_cool_path(self, resolution, cool_type='imputed'):
        """
        read ALLC path series for certain dataset and allc_type

        Parameters
        ----------
        resolution
            Can be "10K", "25K", "100K"
        cool_type
            Can be "raw", "imputed". The mCG ALLC contains CpG only

        Returns
        -------
        Series of cell-id by COOL path on GALE
        """
        resolution = resolution.upper()
        cool_type = cool_type.lower()

        def _read_file_paths(p):
            s = pd.read_csv(p, index_col=0).squeeze()
            s.index.name = 'cell'
            return s

        if resolution == '10K':
            if cool_type == 'raw':
                cool_paths = _read_file_paths(self.CEMBA_SNM3C_10K_RAW_COOL_PATH)
            else:
                cool_paths = _read_file_paths(self.CEMBA_SNM3C_10K_IMPUTED_COOL_PATH)
        elif resolution == '25K':
            if cool_type == 'raw':
                cool_paths = _read_file_paths(self.CEMBA_SNM3C_25K_RAW_COOL_PATH)
            else:
                cool_paths = _read_file_paths(self.CEMBA_SNM3C_25K_IMPUTED_COOL_PATH)
        elif resolution == '100K':
            if cool_type == 'raw':
                cool_paths = _read_file_paths(self.CEMBA_SNM3C_100K_RAW_COOL_PATH)
            else:
                cool_paths = _read_file_paths(self.CEMBA_SNM3C_100K_IMPUTED_COOL_PATH)
        else:
            raise ValueError('Got invalid value for resolution or cool_type. '
                             'Check doc string for allowed values.')
        return cool_paths

    def get_liu_2021_mc_metadata(self):
        return pd.read_csv(self.CEMBA_LIU_2021_NATURE_SNMC_METADATA_PATH, index_col=0)

    def get_mc_annot(self):
        if self._mc_annot is None:
            annot = CEMBAmCCellAnnotation(self.CEMBA_SNMC_CELL_TYPE_ANNOTATION_PATH,
                                          self.get_mc_mapping_metric())
            self._mc_annot = annot
        return self._mc_annot

    def get_m3c_annot(self):
        if self._m3c_annot is None:
            annot = CEMBAm3CCellAnnotation(self.CEMBA_SNM3C_CELL_TYPE_ANNOTATION_PATH,
                                           self.get_m3c_mapping_metric())
            self._m3c_annot = annot
        return self._m3c_annot

    @lru_cache(maxsize=200)
    def get_mc_gene_frac(self, gene, mc_type='CHN'):
        if self._mc_gene_mcds is None:
            self._open_mc_gene_mcds()

        # check if gene is gene name:
        try:
            gene_id = mm10.gene_name_to_id(gene)
        except KeyError:
            gene_id = gene

        gene_data = self._mc_gene_mcds['geneslop2k-vm23_da_frac_fc'].sel(
            {'mc_type': mc_type, 'geneslop2k-vm23': gene_id}
        ).to_pandas()
        return gene_data

    @lru_cache(maxsize=200)
    def _get_cluster_gene_frac(self, dataset, gene, mc_type, value_type, alpha, norm_frac):
        if dataset == 'mc':
            if self._mc_cluster_gene_ds is None:
                self._open_mc_cluster_gene_ds()
            ds = self._mc_cluster_gene_ds
        elif dataset == 'm3c':
            if self._m3c_cluster_gene_ds is None:
                self._open_m3c_cluster_gene_ds()
            ds = self._m3c_cluster_gene_ds
        else:
            raise ValueError('dataset must be "mc" or "m3c"')

        # check if gene is gene name:
        try:
            gene_id = mm10.gene_name_to_id(gene)
        except KeyError:
            gene_id = gene

        count_table = ds.sel(
            {'mc_type': mc_type, 'geneslop2k-vm23': gene_id}
        ).to_pandas()

        mc = count_table['mc']
        cov = count_table['cov']
        if value_type == 'frac':
            frac = mc / (cov + alpha)
            if norm_frac:
                global_frac = ds['cluster_overall_frac'].sel(mc_type=mc_type).to_pandas()
                data = frac / global_frac
            else:
                data = frac
        elif value_type == 'mvalue':
            import numpy as np
            data = np.log2((mc + alpha) / (cov - mc + alpha))
        else:
            raise ValueError('value_type must be "frac" or "mvalue"')

        return data

    def get_mc_cluster_gene_frac(self, gene, mc_type='CHN', value_type='frac', alpha=0.001, norm_frac=True):
        return self._get_cluster_gene_frac('mc', gene, mc_type, value_type, alpha, norm_frac)

    def get_m3c_cluster_gene_frac(self, gene, mc_type='CHN', value_type='frac', alpha=0.001, norm_frac=True):
        return self._get_cluster_gene_frac('m3c', gene, mc_type, value_type, alpha, norm_frac)

    def get_mc_cluster_gene_rna(self, gene, cluster_level='L4Region', norm=True, log1p=True):
        """
        Get RNA expression of a gene in a cluster

        Parameters
        ----------
        gene :
            gene name or gene id
        cluster_level :
            cluster level to get expression for
        norm :
            if True, normalize expression by CPM
        log1p :
            if True, log1p transform expression

        Returns
        -------
        pandas.Series
        """

        if self._mc_cluster_gene_rna_ds is None:
            self._open_mc_cluster_gene_rna_ds()
        da = self._mc_cluster_gene_rna_ds[f'{cluster_level}_da']

        # check if gene is gene name:
        try:
            gene_id = mm10.gene_name_to_id(gene)
        except KeyError:
            gene_id = gene

        gene_data = da.sel(gene=gene_id).to_pandas()
        if norm:
            gene_data = gene_data * 1000000 / da[f'{cluster_level}_umi_count']
        if log1p:
            gene_data = np.log1p(gene_data)
        return gene_data

    @lru_cache(maxsize=200)
    def get_m3c_gene_frac(self, gene, mc_type='CHN'):
        if self._m3c_gene_mcds is None:
            self._open_m3c_gene_mcds()

        # check if gene is gene name:
        try:
            gene_id = mm10.gene_name_to_id(gene)
        except KeyError:
            gene_id = gene

        gene_data = self._m3c_gene_mcds['geneslop2k-vm23_da_frac_fc'].sel(
            {'mc_type': mc_type, 'geneslop2k-vm23': gene_id}
        ).to_pandas()
        return gene_data

    def get_base_ds(self, dataset='snmc'):
        from ALLCools.mcds import BaseDS
        if dataset.lower() in ('snmc', 'mc'):
            return BaseDS(self.CEMBA_SNMC_BASE_DS_PATH_LIST,
                          codebook_path=self.MM10_MC_TYPE_CODEBOOK_PATH,
                          chrom_sizes_path=mm10.MAIN_CHROM_NOCHRM_SIZES_PATH)
        elif dataset.lower() in ('snm3c', 'm3c'):
            return BaseDS(self.CEMBA_SNM3C_BASE_DS_PATH_LIST,
                          codebook_path=self.MM10_MC_TYPE_CODEBOOK_PATH,
                          chrom_sizes_path=mm10.MAIN_CHROM_NOCHRM_SIZES_PATH)
        else:
            raise ValueError(f'Got invalid value for dataset {dataset}.')

    def get_mc_dmr_ds(self, *args, **kwargs):
        return self.get_dmr_ds(dataset='mc', *args, **kwargs)

    def get_grouped_dmr_ds(self, add_atac=False, add_motif=False):
        from ALLCools.mcds import RegionDS

        mc_ds = xr.open_zarr(self.CEMBA_SNMC_GROUPED_DMR_MC_REGION_DS_PATH)
        _ds = [mc_ds]
        if add_atac:
            atac_ds = xr.open_zarr(self.CEMBA_SNMC_GROUPED_DMR_ATAC_REGION_DS_PATH)
            _ds.append(atac_ds)
        if add_motif:
            motif_ds = xr.open_zarr(self.CEMBA_SNMC_GROUPED_DMR_MOTIF_REGION_DS_PATH)
            _ds.append(motif_ds)
        region_ds = RegionDS(xr.merge(_ds))
        region_ds.region_dim = 'dmr'
        return region_ds

    def get_dmr_ds(self, dataset='mc', chunk_type='region', add_motif=False, add_motif_hits=False, add_atac=False):
        from ALLCools.mcds import RegionDS

        if chunk_type == 'region':
            if dataset.lower() in ('snmc', 'mc'):
                path = self.CEMBA_SNMC_DMR_REGION_DS_PATH
            elif dataset.lower() in ('snm3c', 'm3c'):
                path = self.CEMBA_SNM3C_DMR_REGION_DS_PATH
            else:
                raise ValueError(f'Got invalid value for dataset {dataset}.')
        elif chunk_type == 'sample':
            if dataset.lower() in ('snmc', 'mc'):
                path = self.CEMBA_SNMC_DMR_REGION_DS_SAMPLE_CHUNK_PATH
            elif dataset.lower() in ('snm3c', 'm3c'):
                path = self.CEMBA_SNM3C_DMR_REGION_DS_SAMPLE_CHUNK_PATH
            else:
                raise ValueError(f'Got invalid value for dataset {dataset}.')
        else:
            raise ValueError(f'Got invalid value for chunk_type {chunk_type}.')

        ds_list = []
        dmr_ds = RegionDS(
            xr.open_zarr(path),
            region_dim='dmr', chrom_size_path=MM10_MAIN_CHROM_SIZES_PATH
        )
        ds_list.append(dmr_ds)

        if add_motif:
            motif_ds = RegionDS(
                xr.open_zarr(self.CEMBA_SNMC_DMR_MOTIF_SCAN_REGION_DS_PATH),
                region_dim='dmr', chrom_size_path=MM10_MAIN_CHROM_SIZES_PATH
            )
            ds_list.append(motif_ds)

        if add_motif_hits:
            motif_hits_ds = xr.open_zarr(self.CEMBA_SNMC_DMR_TF_AND_MOTIF_HITS_DS_REMOTE_PATH)
            ds_list.append(motif_hits_ds)

        if add_atac:
            atac_ds = xr.open_zarr(self.CEMBA_SNMC_DMR_ATAC_COUNT_ZARR_PATH)
            atac_ds = atac_ds.assign_coords(dmr=dmr_ds.coords['dmr'].values).rename({'L4Region': 'sample_id'})
            ds_list.append(atac_ds)

        if len(ds_list) == 1:
            return ds_list[0]
        else:
            return xr.merge(ds_list)

    def get_cell_type_palette(self):
        p = pd.read_csv(self.CEMBA_CELL_TYPE_ANNOT_PALETTE_PATH, index_col=0, header=None).squeeze().to_dict()
        return p

    def get_cool_ds(self, resolution='10K'):
        if resolution == '10K':
            path = self.CEMBA_SNM3C_L4REGION_COOL_DS_PATH_LIST
        elif resolution == '100K':
            path = self.CEMBA_SNM3C_L4REGION_CHROM_100K_COOL_DS_PATH
        elif resolution == '25K':
            path = self.CEMBA_SNM3C_L4REGION_CHROM_25K_COOL_DS_PATH
        else:
            raise ValueError(f'Got invalid value for resolution {resolution}.')

        from ALLCools.mcds.cool_ds import CoolDS
        sample_weights = pd.read_csv(
            self.CEMBA_SNM3C_L4REGION_COOL_DS_SAMPLE_WEIGHTS_PATH, index_col=0
        ).squeeze()

        cool_ds = CoolDS(
            cool_ds_paths=path,
            chrom_sizes_path=self.CEMBA_SNM3C_L4REGION_COOL_DS_CHROMS_SIZES_PATH,
            sample_weights=sample_weights,
            sample_dim='sample_id'
        )
        return cool_ds

    def get_m3c_matrix_anova(self, group_level='CellType'):
        from ALLCools.mcds.cool_ds import CoolDS
        if group_level == 'CellType':
            path = self.CEMBA_SNM3C_CELL_TYPE_10K_MATRIX_ANOVA_PATH
        else:
            path = self.CEMBA_SNM3C_CELL_CLUSTER_10K_MATRIX_ANOVA_PATH

        cool_ds = CoolDS(
            cool_ds_paths=path,
            chrom_sizes_path=self.CEMBA_SNM3C_L4REGION_COOL_DS_CHROMS_SIZES_PATH,
            sample_weights=None,
        )
        return cool_ds

    def get_mc_cluster_to_m3c_cluster_map(self):
        import joblib
        return joblib.load(self.CEMBA_SNMC_TO_SNM3C_CLUSTER_MAP_PATH)

    def get_mc_cell_type_to_m3c_cluster_map(self):
        cluster_map = self.get_mc_cluster_to_m3c_cluster_map()
        mc_annot = self.get_mc_annot()
        l4r_to_cell_type = mc_annot["L4Region_cat_annot"].to_pandas()

        cell_type_to_cluster_map = {}
        for cell_type in l4r_to_cell_type.unique():
            all_m3c_clusters = set()
            for mc_cluster in l4r_to_cell_type[l4r_to_cell_type == cell_type].index:
                all_m3c_clusters.update(cluster_map.get(mc_cluster, []))
            cell_type_to_cluster_map[cell_type] = all_m3c_clusters

        return cell_type_to_cluster_map
