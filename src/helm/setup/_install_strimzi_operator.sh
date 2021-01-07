#!/bin/bash

STRIMZI_RELEASE_NAME="strimzi"
STRIMZI_NAMESPACE="kafka"
STRIMZI_VERSION="0.20.1"
JIZT_NAMESPACE="default"  # must match JIZT_NAMESPACE in _instal_jizt,sh

echo -e "\n> Installing Strimzi operator..."
echo -e "\n>>> Adding Strimzi chart repo..."
helm repo add strimzi https://strimzi.io/charts/
helm repo update

echo -e "\n>>> Configuring namespaces..."
kubectl create namespace $STRIMZI_NAMESPACE 2> /dev/null  # ignore AlreadyExists error

echo -e "\n>>> Installing strimzi-kafka-operator-$STRIMZI_VERSION Helm chart in namespace '$STRIMZI_NAMESPACE'..."
echo "This will take some time... You can check what's going on with kubectl from another terminal"
# Additional Helm arguments can be passed when executing the script,
# e.g., "./install-strimzi.sh --dry-run --debug"
cat << EOF | helm install $STRIMZI_RELEASE_NAME strimzi/strimzi-kafka-operator \
--wait \
--namespace $STRIMZI_NAMESPACE \
--version $STRIMZI_VERSION \
"$@" \
-f -
    watchNamespaces: ["$JIZT_NAMESPACE"]
    imageRepositoryOverride: "eu.gcr.io/jizt-299516"
EOF
