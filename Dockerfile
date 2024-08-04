FROM openjdk:11

ENV SPARK_VERSION=3.2.0
ENV HADOOP_VERSION=3.3.1

RUN mkdir -p /opt && \
    cd /opt && \
    curl https://archive.apache.org/dist/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz | \
        tar -zx hadoop-${HADOOP_VERSION}/lib/native && \
    ln -s hadoop-${HADOOP_VERSION} hadoop && \
    echo Hadoop ${HADOOP_VERSION} native libraries installed in /opt/hadoop/lib/native

RUN mkdir -p /opt && \
    cd /opt && \
    curl https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop2.7.tgz | \
        tar -zx && \
    ln -s spark-${SPARK_VERSION}-bin-hadoop2.7 spark && \
    echo Spark ${SPARK_VERSION} installed in /opt

# add scripts and update spark default config
# ADD common.sh spark-master spark-worker /
COPY docker/common.sh docker/spark-master docker/spark-worker  /
COPY spark_jobs spark_jobs

RUN chmod +x common.sh spark-master spark-worker
ADD docker/spark-defaults.conf /opt/spark/conf/spark-defaults.conf
ENV PATH=$PATH:/opt/spark/bin