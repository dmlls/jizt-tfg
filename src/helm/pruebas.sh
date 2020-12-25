RELEASE_NAME="strimzi"
STRIMZI_NAMESPACE="strimzi"  # strimzi-operator namespace
PROJECT_NAMESPACE="default"  # project namespace (must exist beforehand)
VERSION="0.20.1"
echo "$RELEASE_NAME strimzi/strimzi-kafka-operator \
--namespace $STRIMZI_NAMESPACE \
--version $VERSION \
$@ "
