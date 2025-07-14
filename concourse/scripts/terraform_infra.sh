set -euo pipefail

aws_account_id=$(echo "$secrets" | jq -r .aws_account_id)
aws_access_key_id=$(echo "$secrets" | jq -r .aws_access_key_id)

aws_secret_access_key=$(echo "$secrets" | jq -r .aws_secret_access_key)
domain=$(echo "$secrets" | jq -r .domain)

service_subdomain=$(echo "$secrets" | jq -r .service_subdomain)
ecr_repository=$(echo "$secrets" | jq -r .ecr_repository)

export AWS_ACCESS_KEY_ID=$aws_access_key_id
export AWS_SECRET_ACCESS_KEY=$aws_secret_access_key

git config --global url."https://x-access-token:$github_access_token@github.com/".insteadOf "https://github.com/"

if [[ ${env} != "prod" ]]; then
    env="dev"
fi

cd resource-repo/terraform/lambda

terraform init -backend-config=env/${env}/backend-${env}.tfbackend -reconfigure
terraform apply \
-var "aws_account_id=$aws_account_id" \
-var "aws_access_key_id=$aws_access_key_id" \
-var "aws_secret_access_key=$aws_secret_access_key" \
-var "domain=$domain" \
-var "service_subdomain=$service_subdomain" \
-var "container_ver=${tag}" \
-var "ecr_repository=$ecr_repository" \
-auto-approve

cd ../api_gateway

terraform init -backend-config=env/${env}/backend-${env}.tfbackend -reconfigure
terraform apply \
-var "aws_account_id=$aws_account_id" \
-var "aws_access_key_id=$aws_access_key_id" \
-var "aws_secret_access_key=$aws_secret_access_key" \
-var "domain=$domain" \
-auto-approve

