FROM centos:7 as builder

# =================================================================
# STAGE 1 -- Configure a build host and install the license manager
# This list of packages is from the ESRI requirements description.
# It includes the entire X-Window server that we will never need.
# Hence the multistage build, first download many files so that
# the Esri installer can run in silent mode, and then 
# ignore them in stage2.

RUN yum install -y \
 compat-libstdc++-33.i686 \
 compat-libf2c-34.i686 \
 compat-openldap.i686 \
 cairo.i686 \
 freeglut.i686 \
 fuse-libs.i686 \
 gmp.i686 \
 gtk2.i686 \
 PackageKit-glib.i686 \
 PackageKit-gtk3-module.i686 \
 polkit.i686 \
 polkit.x86_64 \
 redhat-lsb.i686

RUN yum install -y \
 libcanberra.i686 \
 libgcc.i686 \
 libgfortran.i686 \
 libidn.i686 \
 libstdc++.i686 \
 libSM.i686 \
 libX11.i686 \
 libXau.i686 \
 libxcb.i686 \
 libXdamage.i686 \
 libXext.i686 \
 libXfixes.i686 \
 libXrender.i686 \
 libXp.i686 \
 libXScrnSaver.i686 \
 libXtst.i686

RUN yum install -y \
 mesa-libGL.i686 \
 mesa-libGLU.i686

# Since the final stage will be running Debian it might be better to add another stage
# and build the conda portion in Debian instead of CentOS.
ADD https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh .
RUN sh Miniconda3-latest-Linux-x86_64.sh -b -p /opt/conda
ENV PATH=/opt/conda/bin:${PATH}
ADD conda_requirements.txt ./

# From MapProxy, I left git and pi in here but probably don't need them.
RUN conda update -n base -c defaults conda && \
    conda config --add channels conda-forge && \
    conda install -y --name base pip git --file conda_requirements.txt

# I can use any username here, I suppose
RUN adduser flexlm && \
    mkdir -p /usr/local/share/macrovision/storage && \
    chmod 777 /usr/local/share/macrovision/storage

USER flexlm
WORKDIR /home/flexlm

# Tested with each of these, 2023-03-09
#COPY ArcGIS_License_Manager_Linux_2021.0_177950.tar.gz LicenseManager.tar.gz
COPY ArcGIS_License_Manager_Linux_2022_1_184756.tar.gz LicenseManager.tar.gz

RUN tar xzvf LicenseManager.tar.gz && \
    cd LicenseManager_Linux && \
    ./Setup -l Yes -m silent

# Dump messages out so that errors will be visible on the console when building 
RUN cat arcgis/licensemanager/.Setup/LicenseManager_InstallLog.log

USER root

# ===========================================
# DEPLOYMENT STAGE -- install and run the microservice
# Note that python-bjoern is running in Debian Bullseye
FROM tecktron/python-bjoern
COPY --from=builder /opt/conda /opt/conda
ENV PATH=/opt/conda/bin:${PATH}
    
COPY --from=builder /home/flexlm/arcgis/licensemanager/bin/lmutil /usr/local/bin/
ADD lmstat /usr/local/bin/
ADD service.txt /usr/local/share/

ENV PYTHONPATH /app
WORKDIR /app
COPY prestart.sh .
COPY app app

# No idea if I need this. It might still matter to someone since it's in builder stage
RUN mkdir -p /usr/local/share/macrovision/storage && \
    chmod 777 /usr/local/share/macrovision/storage

RUN useradd --uid 1000 --create-home --home-dir /srv/arctic arctic && \
    chfn --full-name "Arctic" arctic
USER arctic
WORKDIR /srv/arctic
