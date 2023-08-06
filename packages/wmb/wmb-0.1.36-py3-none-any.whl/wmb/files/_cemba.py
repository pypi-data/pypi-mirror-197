import pathlib

import wmb

PACKAGE_DIR = pathlib.Path(wmb.__path__[0])

# =================================
# CEMBA RS1.1
# =================================

# the code to prepare cemba metadata is in
# /home/hanliu/project/cemba/study/BasicFilteringAndPrepareMetadata 04/20/2022
CEMBA_SNMC_MAPPING_METRIC_PATH = PACKAGE_DIR / 'files/CEMBA.CellMetadata.snmC-seq.small.csv.gz'
CEMBA_SNM3C_MAPPING_METRIC_PATH = PACKAGE_DIR / 'files/CEMBA.CellMetadata.snm3C-seq.small.csv.gz'
CEMBA_SNMC_FULL_MAPPING_METRIC_PATH = '/gale/netapp/cemba3c/BICCN/wmb/cemba/CEMBA.CellMetadata.snmC-seq.hdf'
CEMBA_SNM3C_FULL_MAPPING_METRIC_PATH = '/gale/netapp/cemba3c/BICCN/wmb/cemba/CEMBA.CellMetadata.snm3C-seq.hdf'

# the code to prepare cemba file path is in
# /home/hanliu/cemba3c/BICCN/wmb/file_path 04/20/2022
CEMBA_SNMC_ALLC_PATH = PACKAGE_DIR / 'files/CEMBA.snmC.ALLCPaths.csv.gz'
CEMBA_SNM3C_ALLC_PATH = PACKAGE_DIR / 'files/CEMBA.snm3C.ALLCPaths.csv.gz'
CEMBA_SNMC_MCG_ALLC_PATH = PACKAGE_DIR / 'files/CEMBA.snmC.mCGALLCPaths.csv.gz'
CEMBA_SNM3C_MCG_ALLC_PATH = PACKAGE_DIR / 'files/CEMBA.snmC.mCGALLCPaths.csv.gz'

# snm3C contact related
# /home/hanliu/cemba3c/BICCN/wmb/file_path 04/20/2022
CEMBA_SNM3C_CONTACT_PATH = PACKAGE_DIR / 'files/CEMBA.snm3C.ContactPaths.csv.gz'
CEMBA_SNM3C_10K_RAW_COOL_PATH = PACKAGE_DIR / 'files/CEMBA.snm3C.10KRawCoolURLs.csv.gz'
CEMBA_SNM3C_25K_RAW_COOL_PATH = PACKAGE_DIR / 'files/CEMBA.snm3C.25KRawCoolURLs.csv.gz'
CEMBA_SNM3C_100K_RAW_COOL_PATH = PACKAGE_DIR / 'files/CEMBA.snm3C.100KRawCoolURLs.csv.gz'
CEMBA_SNM3C_10K_IMPUTED_COOL_PATH = PACKAGE_DIR / 'files/CEMBA.snm3C.10KImputedCoolURLs.csv.gz'
CEMBA_SNM3C_25K_IMPUTED_COOL_PATH = PACKAGE_DIR / 'files/CEMBA.snm3C.25KImputedCoolURLs.csv.gz'
CEMBA_SNM3C_100K_IMPUTED_COOL_PATH = PACKAGE_DIR / 'files/CEMBA.snm3C.100KImputedCoolURLs.csv.gz'

# snm3C multi-sample zarr dataset
CEMBA_SNM3C_L4REGION_COOL_DS_PATH_LIST = [f'/cemba/m3c-CoolDS/group{i}.coolds' for i in range(48)]
CEMBA_SNM3C_L4REGION_COOL_DS_SAMPLE_WEIGHTS_PATH = '/cemba/m3c-CoolDS/CEMBA.snm3C.L4Region.CellCounts.csv'
CEMBA_SNM3C_L4REGION_COOL_DS_CHROMS_SIZES_PATH = '/cemba/m3c-CoolDS/mm10.main.nochrY.nochrM.chrom.sizes'
CEMBA_SNM3C_L4REGION_CHROM_25K_COOL_DS_PATH = '/cemba/CEMBA_3C/CEMBA.snm3C.chrom25k.L4Region.Q.coolds'
CEMBA_SNM3C_L4REGION_CHROM_100K_COOL_DS_PATH = '/cemba/CEMBA_3C/CEMBA.snm3C.chrom100k.L4Region.Q+Raw.coolds'


# MCDS Path 04/20/2022
# MCDS is ordered according to the first pass clustering, data type is standardized
CEMBA_SNMC_MCDS_PATH = '/gale/netapp/cemba3c/BICCN/CEMBA_RS1/dataset/CEMBA.snmC.mcds'
CEMBA_SNM3C_MCDS_PATH = '/gale/netapp/cemba3c/BICCN/CEMBA_3C/mcds/CEMBA.snm3C.mcds'


# snm3C compartment, embedding, domain
# prepared in /gale/netapp/cemba3c/BICCN/CEMBA_3C/mcds/prepare_3c_matrix 05/15/2022
CEMBA_SNM3C_3C_COMPARTMENT_ZARR_PATH = '/gale/netapp/cemba3c/BICCN/CEMBA_3C/mcds/CEMBA.snm3C.3C.mcds/chrom100k'
CEMBA_SNM3C_3C_DOMAIN_INSULATION_ZARR_PATH = '/gale/netapp/cemba3c/BICCN/CEMBA_3C/mcds/CEMBA.snm3C.3C.mcds/chrom25k'
CEMBA_SNM3C_3C_CHROM100K_RAW_ZARR_PATH = '/gale/netapp/cemba3c/BICCN/CEMBA_3C/mcds/CEMBA.snm3C.chrom100k_raw.zarr'
CEMBA_SNM3C_LOOP_AND_SUMMIT_DS_PATH = '/cemba/CEMBA_3C/loop/CEMBA.snm3C.LoopAndSummit.ds'

CEMBA_SNM3C_CELL_TYPE_10K_MATRIX_ANOVA_PATH = "/cemba/CEMBA_3C/loop/CEMBA.snm3C.CellTypeMatrixANOVA.10Kb.coolds/"
CEMBA_SNM3C_CELL_CLUSTER_10K_MATRIX_ANOVA_PATH = "/cemba/CEMBA_3C/loop/CEMBA.snm3C.CellClusterMatrixANOVA.10Kb.coolds/"
CEMBA_SNM3C_LOOP_VALUES_DS_PATH = '/cemba/CEMBA_3C/loop/CEMBA.snm3C.LoopValues_total.ds'
CEMBA_SNM3C_LOOP_ANOVA_DS_PATH = '/cemba/CEMBA_3C/loop/CEMBA.snm3C.LoopANOVAStats.ds'
CEMBA_SNM3C_LOOP_VALUES_AND_STATS_V2_DS_PATH = '/cemba/CEMBA_3C/loop/CEMBA.snm3C.HighFstatsLoops.DataAndStats.zarr'
CEMBA_SNM3C_DOMAIN_BOUNDARY_AND_CHI2_DS_PATH = '/cemba/CEMBA_3C/domain/CEMBA.snm3C.L4Region.DomainBoundaryAndChi2.ds'
CEMBA_SNM3C_DOMAIN_INSULATION_SCORE_DS_PATH = '/cemba/CEMBA_3C/domain/CEMBA.snm3C.chrom25k.InsulationScore.coolds'


# cluster assignments
# cell class, major type, subtype
CEMBA_SNMC_CELL_TYPE_ANNOTATION_PATH = '/gale/netapp/cemba3c/BICCN/wmb/cemba/CEMBA.snmC.Annotations.zarr'
CEMBA_SNM3C_CELL_TYPE_ANNOTATION_PATH = '/gale/netapp/cemba3c/BICCN/wmb/cemba/CEMBA.snm3C.Annotations.zarr'

# Outlier IDs
# /home/hanliu/project/cemba/study/MarkOutlier 05/12/2022
CEMBA_SNMC_OUTLIER_IDS_PATH = PACKAGE_DIR / 'files/CEMBA.snmC.DoubletsID.txt.gz'
CEMBA_SNM3C_OUTLIER_IDS_PATH = PACKAGE_DIR / 'files/CEMBA.snm3C.DoubletsID.txt.gz'

# Liu 2021 Nature metadata
CEMBA_LIU_2021_NATURE_SNMC_METADATA_PATH = PACKAGE_DIR / 'files/CEMBA.Liu2021Nature.snmC.metadata.csv.gz'

# Gene chunk zarr path
CEMBA_SNMC_GENE_CHUNK_ZARR_PATH = '/gale/netapp/cemba3c/BICCN/wmb/GeneChunks/CEMBA.snmC'
CEMBA_SNM3C_GENE_CHUNK_ZARR_PATH = '/gale/netapp/cemba3c/BICCN/wmb/GeneChunks/CEMBA.snm3C'

# Cluster Aggregation
CEMBA_SNMC_CLUSTER_L4_SUM_ZARR_PATH = '/gale/netapp/cemba3c/BICCN/wmb/cemba/CEMBA.snmC.L4Agg.zarr'
CEMBA_SNM3C_CLUSTER_L4_SUM_ZARR_PATH = '/gale/netapp/cemba3c/BICCN/wmb/cemba/CEMBA.snm3C.L4Agg.zarr'

CEMBA_SNMC_CLUSTER_L4Region_SUM_ZARR_PATH = '/gale/netapp/cemba3c/BICCN/wmb/cemba/CEMBA.snmC.L4RegionAgg.zarr'
CEMBA_SNM3C_CLUSTER_L4Region_SUM_ZARR_PATH = '/gale/netapp/cemba3c/BICCN/wmb/cemba/CEMBA.snm3C.L4RegionAgg.zarr'

CEMBA_SNMC_BASE_DS_REMOTE_PATH_LIST = [f'/cemba/BaseDS/group{i}.baseds' for i in range(24)]
CEMBA_SNM3C_BASE_DS_REMOTE_PATH_LIST = [f'/cemba/m3c-BaseDS/group{i}.baseds' for i in range(12)]
MM10_MC_TYPE_CODEBOOK_REMOTE_PATH = '/cemba/BaseDS/mm10_codebook'

CEMBA_SNMC_DMR_REGION_DS_REMOTE_PATH = '/cemba/wmb/genome/CEMBA.snmC.L4Region-by-DMR.order.zarr'
CEMBA_SNMC_DMR_REGION_DS_SAMPLE_CHUNK_REMOTE_PATH = \
    '/cemba/wmb/genome/CEMBA.snmC.L4Region-by-DMR.sample_chunk.order.zarr'
CEMBA_SNMC_DMR_MOTIF_SCAN_REGION_DS_REMOTE_PATH = '/cemba/wmb/genome/CEMBA.snmC.DMR.motif_scan.order.ds'
CEMBA_SNMC_DMR_TF_AND_MOTIF_HITS_DS_REMOTE_PATH = \
    '/cemba/wmb/genome/CEMBA.snmC.DMR.tf_motif_enrichment_and_hits.order.ds'
CEMBA_SNMC_GROUPED_DMR_MC_REGION_DS_PATH = '/cemba/wmb/genome/DMR/CEMBA.snmC.AllGroupedDMRs.mC.zarr'
CEMBA_SNMC_GROUPED_DMR_ATAC_REGION_DS_PATH = '/cemba/wmb/genome/DMR/CEMBA.AllGroupedDMRs.ATAC.zarr'
CEMBA_SNMC_GROUPED_DMR_MOTIF_REGION_DS_PATH = '/cemba/wmb/genome/DMR/CEMBA.DMRAllGroupedDMRs.Motif.zarr'

CEMBA_SNMC_DMR_ATAC_COUNT_ZARR_PATH = '/cemba/wmb/cemba/CEMBA.snmC.L4Region.DMR.ATAC.zarr'
CEMBA_SNMC_CHROM_10BP_ATAC_COUNT_ZARR_PATH = '/cemba/wmb/cemba/CEMBA.snmC.L4Region.ATACCounts.zarr'

# snmC and snm3C Integration
CEMBA_SNMC_TO_SNM3C_CLUSTER_MAP_PATH = PACKAGE_DIR / 'files/CEMBA.snmC-to-snm3C.L4RegionMap.221110.dict'

# Integration based other modalities at cluster level
CEMBA_SNMC_L4REGION_AIBS_TENX_COUNTS_ZARR_PATH = '/cemba/wmb/cemba/CEMBA.snmC.L4Region.AIBS_TENX_COUNTS.zarr'


# the same DMR regions as SNMC
CEMBA_SNM3C_DMR_REGION_DS_REMOTE_PATH = '/cemba/wmb/genome/CEMBA.snm3C.L4Region-by-DMR.zarr'
CEMBA_SNM3C_DMR_REGION_DS_SAMPLE_CHUNK_REMOTE_PATH = \
    '/cemba/wmb/genome/CEMBA.snm3C.L4Region-by-DMR.sample_chunk.zarr'

# palette
CEMBA_CELL_TYPE_ANNOT_PALETTE_PATH = PACKAGE_DIR / 'files/palette/CEMBA.CellTypeAnnot.csv'

# =================================
# CEMBA ATAC
# =================================

CEMBA_ATAC_ZARR_PATH = '/gale/netapp/cemba3c/BICCN/CEMBA_ATAC/zarr/CEMBA.snATAC.zarr'
CEMBA_ATAC_CLUSTER_FULL_NAME_PATH = PACKAGE_DIR / 'files/CEMBA.snATAC.ClusterDescription.tsv'
CEMBA_ATAC_MAPPING_METRIC_PATH = '/gale/netapp/cemba3c/BICCN/CEMBA_ATAC/meta/CEMBA.snATAC.Metadata.hdf'

# gene chunk
CEMBA_ATAC_GENE_CHUNK_PATH = '/gale/netapp/cemba3c/BICCN/wmb/GeneChunks/CEMBA.ATAC'

# annotation
CEMBA_ATAC_CELL_TYPE_ANNOTATION_PATH = '/gale/netapp/cemba3c/BICCN/wmb/cemba_atac/CEMBA.snATAC.Annotations.zarr'
CEMBA_ATAC_CELL_TYPE_ANNOTATION_V2_PATH = '/gale/netapp/cemba3c/BICCN/wmb/cemba_atac/CEMBA.snATAC.Annotations.v2.zarr'

# Cluster Aggregation
CEMBA_ATAC_CLUSTER_L4_SUM_ZARR_PATH = '/gale/netapp/cemba3c/BICCN/wmb/cemba_atac/CEMBA.ATAC.L4Agg.zarr/'

CEMBA_ATAC_CLUSTER_L4Region_SUM_ZARR_PATH = '/gale/netapp/cemba3c/BICCN/wmb/cemba_atac/CEMBA.ATAC.L4RegionAgg.zarr/'
