FROM continuumio/miniconda3:4.9.2

RUN mkdir /opt/callc
RUN mkdir /opt/callc/install
WORKDIR /opt/callc

COPY install/environment_callc.yml /opt/callc/install/

RUN conda env create -f install/environment_callc.yml

RUN apt install -y libxt6 sassc
RUN bash -c '. /opt/conda/etc/profile.d/conda.sh && conda activate callc && Rscript -e "install.packages(\"doMC\")"'

RUN bash -c '. /opt/conda/etc/profile.d/conda.sh && conda activate callc && conda install xlrd'
RUN bash -c '. /opt/conda/etc/profile.d/conda.sh && conda activate callc && conda install notebook\<6.1.6 rise matplotlib'

# debug only
RUN bash -c '. /opt/conda/etc/profile.d/conda.sh && conda activate callc && pip install trepan3k'

COPY install /opt/callc/install/
COPY rt /opt/callc/rt/
RUN mkdir /opt/callc/rt/test_preds
RUN chmod -R a+w /opt/callc/rt


COPY ljocha.scss patch-reveal-themes.sh /work/
# COPY *.ipynb pbc3.xtc 1L2Y.pdb /work/

WORKDIR /work
ARG prefix=/opt/conda/envs/callc
RUN sassc -I ${prefix}/share/jupyter/nbextensions/rise/reveal.js/css/theme/source ljocha.scss ljocha.css && ./patch-reveal-themes.sh ljocha.css && cp ljocha.css ${prefix}/share/jupyter/nbextensions/rise/reveal.js/css/theme

COPY sitola_9-21/* /work/
ENV PATH="${prefix}/bin:${PATH}"
