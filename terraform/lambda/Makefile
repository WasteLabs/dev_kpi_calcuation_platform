init:
	terraform init --reconfigure --upgrade

plan:
	terraform plan -var-file="../global.tfvars"

apply:
	terraform apply -auto-approve -var-file="../global.tfvars"

destroy:
	terraform destroy -var-file="../global.tfvars"

fmt:
	terraform fmt

lint:
	tflint .

doc:
	terraform-docs markdown . --output-file README.md

git_stage: fmt lint doc
	git add .
