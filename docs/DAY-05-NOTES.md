# Day 5 - Terraform Drift and Docker

## Terraform Drift

### Validation
- Changed NSG HTTP destination port manually from 80 to 8080 in Azure Portal.
- `terraform plan` detected drift.
- Terraform proposed an in-place update from 8080 back to 80.
- `terraform apply` restored the declared configuration.
- Final `terraform plan` returned no changes.

## Key concept
Terraform configuration defines the desired state.
Manual changes can create drift.
`terraform plan` detects differences between real infrastructure and configuration.

## Docker

### Implemented
- Installed Docker Engine on the Linux VM.
- Started the Docker service.
- Pulled the `nginx:latest` image.
- Created an Nginx container mapped as `8080:80`.

### Validations
- `docker ps` confirmed the container was running.
- `curl http://localhost:8080` returned the Nginx welcome page.
- Stopped and restarted the same container successfully.
- Removed the container while keeping the image.
- Removed the Nginx image afterward.

### Key concepts
- Image = reusable template.
- Container = running instance created from an image.
- `docker stop` does not delete a container.
- `docker rm` deletes the container.
- `docker rmi` deletes the image.

## GitHub Actions - Terraform CI

### Implemented
- Created `.github/workflows/terraform-check.yml`.
- Workflow runs automatically when Terraform files or the workflow itself change.
- Added manual execution with `workflow_dispatch`.

### Validation
- GitHub runner checked out the repository.
- Terraform was installed and initialized.
- `terraform fmt -check` completed successfully.
- `terraform validate` completed successfully.

### Troubleshooting
- First workflow run failed because the GitHub runner did not have `~/.ssh/id_rsa.pub`.
- Added a temporary SSH key generation step to the workflow.
- Second workflow run completed successfully.

## Key concept
CI validates the Terraform configuration in a clean environment without deploying infrastructure.

A configuration that works locally may still depend on files or settings that do not exist in another environment.
