# docker needs sudo
sudo screen -R root
# inside screen, all commands are run as root

# pull higlass docker image
docker pull higlass/higlass-docker:latest

# run higlass docker image
docker run --detach \
--publish 8989:80 \
--volume ~/hg-data:/data \
--volume ~/tmp:/tmp \
--volume /cemba:/cemba \
--name higlass-container \
higlass/higlass-docker:latest

# interactive shell into higlass docker image
docker exec -it higlass-container /bin/bash

# inside docker image
# /cemba/higlass is the actual bucket location for store all tileset files,
# /data/media inside docker image is the location for expose to higlass server
ln -s /cemba/higlass /data/media

# add tileset files to higlass server
# outside docker image, on any machine, when file is ready
cp /ANY/TILESET/FILE /cemba/higlass/ANY/SUB_DIR/FILE

# NOTE: if exec higlass manage command outside docker image or root screen, you can use
sudo docker exec higlass-container python higlass-server/manage.py OTHER_PARAMS
# to replace
/home/higlass/projects/higlass-server/manage.py OTHER_PARAMS

# list all tilesets
/home/higlass/projects/higlass-server/manage.py list_tilesets

# rename tileset
/home/higlass/projects/higlass-server/manage.py modify_tileset \
--uuid UUID --name NEW_NAME

# delete tileset
/home/higlass/projects/higlass-server/manage.py delete_tileset \
--uuid UUID

# coordSystem must associated with chrom sizes file, ingest this before any tilesets
# remember to add --no-upload to avoid copy files, since files already in the /data/media
/home/higlass/projects/higlass-server/manage.py ingest_tileset \
--filename /data/media/mm10.main.chrom.sizes \
--filetype chromsizes-tsv \
--datatype chromsizes \
--coordSystem mm10 \
--no-upload

# ingest bigwig file
/home/higlass/projects/higlass-server/manage.py ingest_tileset \
--filename /data/media/CEMBA.snmC.CellType.ATAC.CPM.50bp/Sst_Gaba.ATAC_CPM.bw \
--name "Sst Gaba ATAC CPM" \
--project-name "CEMBA" \
--filetype bigwig \
--datatype vector \
--coordSystem mm10 \
--no-upload

