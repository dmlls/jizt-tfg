#!/bin/bash

STRIMZI_RELEASE_NAME="strimzi"
STRIMZI_NAMESPACE="kafka"  # strimzi-operator namespace
STRIMZI_VERSION="0.20.1"

JIZT_RELEASE_NAME="jizt"
JIZT_NAMESPACE="default"
JIZT_VERSION="0.0.1"

# If user interrupts installation, make sure we leave
# everything consistent.
trap tidy_up SIGINT  
tidy_up() {
    unhide_deployments
    echo -e "\nInstallation cancelled."
    exit 1
}

# Function definitions
hide_deployments() {
    cd ./jizt/templates
    for file in *-deployment.yaml; do
        if [[ -f $file  ]]; then
            mv $file .$file  # hide files
        fi
    done
    cd - > /dev/null  # don't print directory
}

unhide_deployments() {
    cd ./jizt/templates
    for file in .*-deployment.yaml; do
        if [[ -f $file  ]]; then
            mv $file "${file:1}"  # unhide files
        fi;
    done
    cd - > /dev/null  # don't print directory
}

echo "THANK YOU for installing JIZT v$JIZT_VERSION."
echo "The installation process will take some time... But hey! Rome wasn't built"
echo "in a day. We recommend that you go get a coffee and come visit later :)"

echo -e "\n> Installing Strimzi operator..."
echo -e "\n>>> Adding Strimzi chart repo..."
helm repo add strimzi https://strimzi.io/charts/

echo -e "\n>>> Configuring namespaces..."
kubectl create namespace $STRIMZI_NAMESPACE
kubectl create namespace $JIZT_NAMESPACE

echo -e "\n>>> Installing strimzi-operator-$STRIMZI_VERSION helm chart in namespace '$STRIMZI_NAMESPACE'..."
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
EOF

echo -e "\n> Installing jizt..."

echo -e "\n>>> Installing Strimzi/Kafka related components in namespace '$JIZT_NAMESPACE'..."

# Helm "--wait" flag does not seem to give much of a sh*t for Strimzi stuff so
# we hide microservices deployments so Helm doesn't install them yet.
hide_deployments
sleep 8
cat << EOF | helm install $JIZT_RELEASE_NAME ./jizt \
--wait \
--namespace $JIZT_NAMESPACE \
"$@" \
-f -
    namespace: "$JIZT_NAMESPACE"
EOF

echo -e "\n>>> Waiting for everything to be ready..." 

# As the deployment has not been yet created, kubectl will return the error:
# "Error from server (NotFound): deployments.apps "jizt-cluster-entity-operator" not found".
# We wait until this deployment is ready.
error=$(kubectl rollout status deployment.apps/jizt-cluster-entity-operator 2>&1 >/dev/null)
while [[ $error == *"Error"*  ]]; do
    sleep 10
    error=$(kubectl rollout status deployment.apps/jizt-cluster-entity-operator 2>&1 >/dev/null)
done

echo -e "\n>>> Installing jizt microservices in namespace '$JIZT_NAMESPACE'..."

# Unhide microservices deployments to install them now
# that everything is ready.
unhide_deployments
cat << EOF | helm upgrade $JIZT_RELEASE_NAME ./jizt \
--wait \
--namespace $JIZT_NAMESPACE \
"$@" \
-f -
    namespace: "$JIZT_NAMESPACE"
EOF

echo -e "\n> Everything ready, done installing!"

