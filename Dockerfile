FROM continuumio/miniconda3:4.9.2

RUN mkdir /opt/callc
COPY rt /opt/callc/rt/
COPY install /opt/callc/install/
RUN chmod -R a+w /opt/callc/rt

WORKDIR /opt/callc

RUN conda env create -f install/environment_callc.yml

# RUN conda init
RUN bash -c '. /opt/conda/etc/profile.d/conda.sh && conda activate callc && conda install notebook\<6.1.6'
RUN bash -c '. /opt/conda/etc/profile.d/conda.sh && conda activate callc && conda install xlrd'

RUN apt install -y libxt6
RUN bash -c '. /opt/conda/etc/profile.d/conda.sh && conda activate callc && Rscript -e "install.packages(\"doMC\")"'

