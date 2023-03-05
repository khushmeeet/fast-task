# check if jq is installed
if ! [ -x "$(command -v jq)" ]; then
    echo 'Error: jq is not installed.' >&2
    echo "Install jq: brew install jq"
    exit 1
fi

helm_status=$(helm status user-service --output json | jq -r '.status')
if [[ $helm_status == *"not found"* ]]; then
    echo ">> user-service is not installed"
    echo ">> installing user-service"
    helm install user-service ./user-service/helm
elif [[ $helm_status == *"installed"* ]]; then
    echo ">> user-service is already installed"
    echo ">> updating user-service"
    helm upgrade user-service ./user-service/helm
fi

helm_status=$(helm status todo-service --output json | jq -r '.status')
if [[ $helm_status == *"not found"* ]]; then
    echo ">> todo-service is not installed"
    echo ">> installing todo-service"
    helm install todo-service ./todo-service/helm
elif [[ $helm_status == *"installed"* ]]; then
    echo ">> todo-service is already installed"
    echo ">> updating todo-service"
    helm upgrade todo-service ./todo-service/helm
fi