# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# syntax=docker/dockerfile:1
FROM python:3.9-bullseye

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      sudo \
      curl \
      vim \
      unzip \
      openjdk-11-jdk \
      build-essential \
      software-properties-common \
      ssh && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Jupyter and other python deps
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Add scala kernel via spylon-kernel
RUN python3 -m spylon_kernel install

# Download and install IJava jupyter kernel
RUN curl https://github.com/SpencerPark/IJava/releases/download/v1.3.0/ijava-1.3.0.zip -Lo ijava-1.3.0.zip \
  && unzip ijava-1.3.0.zip \
  && python3 install.py --sys-prefix \
  && rm ijava-1.3.0.zip

# Optional env variables
ENV SPARK_HOME=${SPARK_HOME:-"/opt/spark"}
ENV PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.9.7-src.zip:$PYTHONPATH

WORKDIR ${SPARK_HOME}

ENV SPARK_VERSION=3.3.4
ENV SPARK_MAJOR_VERSION=3.3
ENV ICEBERG_VERSION=1.4.2

# Download spark
RUN mkdir -p ${SPARK_HOME} \
 && curl https://dlcdn.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop2.tgz -o spark-${SPARK_VERSION}-bin-hadoop2.tgz \
 && tar xvzf spark-${SPARK_VERSION}-bin-hadoop2.tgz --directory /opt/spark --strip-components 1 \
 && rm -rf spark-${SPARK_VERSION}-bin-hadoop2.tgz


# Add iceberg spark runtime jar to IJava classpath
ENV IJAVA_CLASSPATH=/opt/spark/jars/*

RUN mkdir -p /home/iceberg/localwarehouse /home/iceberg/notebooks /home/iceberg/warehouse /home/iceberg/spark-events /home/iceberg
#COPY notebooks/ /home/iceberg/notebooks

# Add a notebook command
RUN echo '#! /bin/sh' >> /bin/notebook \
 && echo 'export PYSPARK_DRIVER_PYTHON=jupyter-notebook' >> /bin/notebook \
 && echo "export PYSPARK_DRIVER_PYTHON_OPTS=\"--notebook-dir=/home/iceberg/notebooks --ip='*' --NotebookApp.token='' --NotebookApp.password='' --port=8888 --no-browser --allow-root\"" >> /bin/notebook \
 && echo "pyspark" >> /bin/notebook \
 && chmod u+x /bin/notebook

# Add a pyspark-notebook command (alias for notebook command for backwards-compatibility)
RUN echo '#! /bin/sh' >> /bin/pyspark-notebook \
 && echo 'export PYSPARK_DRIVER_PYTHON=jupyter-notebook' >> /bin/pyspark-notebook \
 && echo "export PYSPARK_DRIVER_PYTHON_OPTS=\"--notebook-dir=/home/iceberg/notebooks --ip='*' --NotebookApp.token='' --NotebookApp.password='' --port=8888 --no-browser --allow-root\"" >> /bin/pyspark-notebook \
 && echo "pyspark" >> /bin/pyspark-notebook \
 && chmod u+x /bin/pyspark-notebook

RUN mkdir -p /root/.ipython/profile_default/startup
COPY ipython/startup/00-prettytables.py /root/.ipython/profile_default/startup
COPY ipython/startup/README /root/.ipython/profile_default/startup

#COPY spark-defaults.conf /opt/spark/conf
ENV PATH="/opt/spark/sbin:/opt/spark/bin:${PATH}"

RUN chmod u+x /opt/spark/sbin/* && \
    chmod u+x /opt/spark/bin/*

#COPY .pyiceberg.yaml /root/.pyiceberg.yaml

COPY entrypoint.sh .

ENTRYPOINT ["./entrypoint.sh"]
CMD ["notebook"]
