cmd="${1:-jupyter notebook --port 8080 --ip 0.0.0.0}"

docker run \
-e HOME=/data \
-e PYTHONPATH=/opt/callc/rt \
-v $PWD:/data -w /data \
-u $(id -u) \
-p 8080:8080 \
-ti \
recetox/callc \
bash -c ". /opt/conda/etc/profile.d/conda.sh && conda activate callc && $cmd"

