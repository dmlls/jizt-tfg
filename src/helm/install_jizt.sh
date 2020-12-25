#!/bin/bash

STRIMZI_RELEASE_NAME="strimzi"
STRIMZI_NAMESPACE="kafka"  # strimzi-operator namespace
STRIMZI_VERSION="0.20.1"

JIZT_RELEASE_NAME="jizt"
JIZT_NAMESPACE="default"

echo "> Installing Strimzi operator..."
echo -e "\n>>> Adding Strimzi chart repo..."
helm repo add strimzi https://strimzi.io/charts/

echo -e "\n>>> Configuring namespaces..."
kubectl create namespace $STRIMZI_NAMESPACE
kubectl create namespace $JIZT_NAMESPACE

echo -e "\n>>> Installing Helm charts..."
# Additional Helm arguments can be passed when executing the script,
# e.g., "./install-strimzi.sh --dry-run --debug"
cat << EOF | helm install $STRIMZI_RELEASE_NAME strimzi/strimzi-kafka-operator \
--namespace $STRIMZI_NAMESPACE \
--version $STRIMZI_VERSION \
"$@" \
-f -
    watchNamespaces: ["$JIZT_NAMESPACE"]
EOF

echo -e "\n> Installing jizt..."
cat << EOF | helm install $JIZT_RELEASE_NAME ./jizt \
--namespace $JIZT_NAMESPACE \
"$@" \
-f -
    namespace: "$JIZT_NAMESPACE"
EOF

echo -e "\n> Done installing!"
