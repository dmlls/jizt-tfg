#!/bin/bash

JIZT_RELEASE_NAME="jizt"
JIZT_NAMESPACE="default"  # must match JIZT_NAMESPACE in _instal_strimzi_operator,sh
JIZT_VERSION="0.0.1"
JIZT_CHART_PATH="../jizt"  # don't add trailing slash

# If user interrupts installation, make sure we leave
# everything consistent.
trap tidy_up SIGINT  
tidy_up() {
    unhide_deployments
    exit 1
}

# Function definitions
hide_deployments() {
    cd "$JIZT_CHART_PATH/templates"
    for file in *-deployment.yaml; do
        if [[ -f $file  ]]; then
            mv $file .$file  # hide files
        fi
    done
    cd - > /dev/null  # don't print directory
}

unhide_deployments() {
    cd "$JIZT_CHART_PATH/templates"
    for file in .*-deployment.yaml; do
        if [[ -f $file  ]]; then
            mv $file "${file:1}"  # unhide files
        fi;
    done
    cd - > /dev/null  # don't print directory
}

echo -e "\n> Installing JIZT v$JIZT_VERSION..."

echo -e "\n>>> Configuring namespaces..."
kubectl create namespace $JIZT_NAMESPACE 2> /dev/null

echo -e "\n>>> Installing Strimzi/Kafka related components in namespace '$JIZT_NAMESPACE'..."

# Helm "--wait" flag does not seem to give much of a sh*t for Strimzi stuff so
# we hide microservices deployments so Helm doesn't install them yet.
hide_deployments
sleep 8
cat << EOF | helm install $JIZT_RELEASE_NAME $JIZT_CHART_PATH \
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

echo -e "\n>>> Installing JIZT microservices in namespace '$JIZT_NAMESPACE'..."

# Unhide microservices deployments to install them now
# that everything is ready.
unhide_deployments
cat << EOF | helm upgrade $JIZT_RELEASE_NAME $JIZT_CHART_PATH \
--wait \
--namespace $JIZT_NAMESPACE \
"$@" \
-f -
    namespace: "$JIZT_NAMESPACE"
EOF
