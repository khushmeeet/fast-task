# check if jq is installed
if ! [ -x "$(command -v jq)" ]; then
    echo 'Error: jq is not installed.' >&2
    echo "Install jq: brew install jq"
    exit 1
fi

user_status=$(helm status user-service --output json | jq -r '.info.status')
if [[ $user_status == *"uninstalled"* ]]; then
    echo ">> user-service is not installed"
    echo ">> installing user-service"
    helm install user-service ./user_service/helm
elif [[ $user_status == *"deployed"* ]]; then
    echo ">> user-service is already installed"
    echo ">> updating user-service"
    helm uninstall user-service
    helm install user-service ./user_service/helm
fi

echo ""
echo ""

todo_status=$(helm status todo-service --output json | jq -r '.info.status')
if [[ $todo_status == *"uninstalled"* ]]; then
    echo ">> todo-service is not installed"
    echo ">> installing todo-service"
    helm install todo-service ./todo_service/helm
elif [[ $todo_status == *"deployed"* ]]; then
    echo ">> todo-service is already installed"
    echo ">> updating todo-service"
    helm uninstall todo-service
    helm install todo-service ./todo_service/helm
fi