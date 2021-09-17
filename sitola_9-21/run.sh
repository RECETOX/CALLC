port=8081
cmd="${1:-jupyter notebook --port $port --ip 0.0.0.0}"

docker run \
-e HOME=/data \
-e PYTHONPATH=/opt/callc/rt \
-v $PWD:/data -w /data \
-u $(id -u) \
-p $port:$port \
-ti \
recetox/callc \
bash -c ". /opt/conda/etc/profile.d/conda.sh && conda activate callc && $cmd"

