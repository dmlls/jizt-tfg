#!/bin/bash
RELEASE_NAME="strimzi"
NAMESPACE="strimzi"
VERSION="0.20.1"

helm repo add strimzi https://strimzi.io/charts/

# try to delete namespace first in case it already exists
kubectl delete namespace $NAMESPACE 2> /dev/null
kubectl create namespace $NAMESPACE

helm install $RELEASE_NAME strimzi/strimzi-kafka-operator \
--namespace $NAMESPACE \
--version $VERSION  \
"$@"  # additional Helm arguments, e.g., "--dry-run" or "--debug"
