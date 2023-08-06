"""
"""

import pathlib

import wmb

PACKAGE_DIR = pathlib.Path(wmb.__path__[0])

# =================================
# BROAD 10X
# =================================

BROAD_TENX_SAMPLE_METADATA_PATH = PACKAGE_DIR / 'files/BROAD.TENX.SampleMetadata.csv.gz'
BROAD_TENX_ZARR_PATH = '/gale/netapp/cemba3c/BICCN/BROAD_TENX/BROAD.TENX.ordered.zarr'
BROAD_TENX_V2_ZARR_PATH = '/gale/netapp/cemba3c/BICCN/BROAD_TENX/BROAD.TENX.v2.ordered.zarr'
BROAD_TENX_CELL_TYPE_ANNOTATION_PATH = '/gale/netapp/cemba3c/BICCN/wmb/broad/BROAD.TENX.Annotations.zarr'
BROAD_TENX_CELL_TYPE_V2_ANNOTATION_PATH = '/gale/netapp/cemba3c/BICCN/wmb/broad/BROAD.TENX.v2.Annotations.zarr'
BROAD_TENX_OUTLIER_IDS_PATH = PACKAGE_DIR / 'files/BROAD.TENX.DoubletsID.txt.gz'

# gene metadata
BROAD_TENX_GENE_MAP_PATH = PACKAGE_DIR / 'files/BROAD.TENX.GeneMap.csv'

# Gene chunk zarr path
BROAD_TENX_GENE_CHUNK_ZARR_PATH = '/gale/netapp/cemba3c/BICCN/wmb/GeneChunks/BROAD.TENX'
BROAD_TENX_GENE_CHUNK_V2_ZARR_PATH = '/gale/netapp/cemba3c/BICCN/wmb/GeneChunks/BROAD.TENX.v2'

# Cluster Aggregation
BROAD_TENX_CLUSTER_L4_SUM_ZARR_PATH = '/gale/netapp/cemba3c/BICCN/wmb/broad/BROAD.TENX.L4Agg.zarr'
BROAD_TENX_CLUSTER_L4Region_SUM_ZARR_PATH = '/gale/netapp/cemba3c/BICCN/wmb/broad/BROAD.TENX.L4RegionAgg.zarr'
