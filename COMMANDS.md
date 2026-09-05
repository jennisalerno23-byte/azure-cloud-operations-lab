# Cloud Operations Lab - Command Reference

Quick reference for the commands practiced during the lab.

## Terraform

| Command                   | Purpose                                                                                      |
| ------------------------- | -------------------------------------------------------------------------------------------- |
| `terraform init`          | Initializes the working directory and downloads the required providers.                      |
| `terraform fmt`           | Formats Terraform configuration files.                                                       |
| `terraform validate`      | Checks whether the configuration is syntactically and structurally valid.                    |
| `terraform plan`          | Compares the declared configuration with the real infrastructure and shows proposed changes. |
| `terraform apply`         | Applies the changes required to match the declared configuration.                            |
| `terraform plan -destroy` | Shows which Terraform-managed resources would be removed.                                    |
| `terraform destroy`       | Removes the infrastructure managed by the current Terraform state.                           |

### Typical workflow

`edit` → `terraform fmt` → `terraform validate` → `terraform plan` → `terraform apply`

> **Drift:** `terraform plan` can detect differences between the real infrastructure and the desired state declared in the `.tf` files.

## Linux

| Command                                        | Purpose                                        |
| ---------------------------------------------- | ---------------------------------------------- |
| `whoami`                                       | Shows the current user.                        |
| `hostname`                                     | Shows the machine hostname.                    |
| `pwd`                                          | Shows the current working directory.           |
| `ip addr`                                      | Shows network interfaces and IP addresses.     |
| `ip route`                                     | Shows the local routing table.                 |
| `ss -tulpn`                                    | Shows listening ports and network sockets.     |
| `ps aux --sort=-%cpu \| head`                  | Shows the processes using the most CPU.        |
| `systemctl status nginx --no-pager`            | Checks the current state of the Nginx service. |
| `sudo systemctl stop nginx`                    | Stops Nginx.                                   |
| `sudo systemctl start nginx`                   | Starts Nginx.                                  |
| `journalctl -u nginx --since "10 minutes ago"` | Shows recent Nginx service logs.               |
| `curl http://localhost`                        | Tests an HTTP service locally.                 |
| `df -h`                                        | Shows disk usage.                              |
| `free -h`                                      | Shows memory usage.                            |
| `logger -p daemon.info "Test message"`         | Generates a Syslog event for testing.          |

## Azure CLI

| Command                                                                                                                                                | Purpose                                                       |
| ------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------- |
| `az provider register --namespace Microsoft.X`                                                                                                         | Registers an Azure resource provider for the subscription.    |
| `az provider show --namespace Microsoft.X --query registrationState`                                                                                   | Checks whether a resource provider is registered.             |
| `az vm show --resource-group rg-cloud-operations-lab --name vm-cloud-operations-lab -d --query publicIps -o tsv`                                       | Retrieves the VM public IP address.                           |
| `az monitor metrics list --resource "$VM_ID" --metric "Percentage CPU" --interval PT1M --aggregation Average -o table`                                 | Retrieves Azure Monitor CPU metrics from the VM.              |
| `az monitor log-analytics workspace show --resource-group rg-cloud-operations-lab --workspace-name law-cloud-operations-lab --query provisioningState` | Checks the provisioning state of the Log Analytics workspace. |

### Useful pattern

`--query` filters the output and `-o tsv` returns a clean text value when only one field is needed.

## Git / GitHub

| Command                                                          | Purpose                                               |
| ---------------------------------------------------------------- | ----------------------------------------------------- |
| `git clone <repository-url>`                                     | Downloads a repository and its history.               |
| `git status`                                                     | Shows the current branch and pending changes.         |
| `git diff`                                                       | Shows unstaged changes.                               |
| `git diff --cached`                                              | Shows changes already staged for commit.              |
| `git add <file>`                                                 | Stages a file for the next commit.                    |
| `git commit -m "message"`                                        | Creates a commit with the staged changes.             |
| `git push`                                                       | Sends local commits to the remote repository.         |
| `git branch -M main`                                             | Renames the current branch to `main`.                 |
| `git remote add origin <repository-url>`                         | Connects the local repository to a remote repository. |
| `gh auth login --hostname github.com --git-protocol https --web` | Authenticates GitHub CLI using the browser.           |
| `gh auth status`                                                 | Checks the current GitHub CLI authentication status.  |
| `gh auth setup-git`                                              | Configures Git to use GitHub CLI authentication.      |

### Practical workflow

`git status` → `git diff` → `git add` → `git commit` → `git push`

## Docker

| Command | Purpose |
|---|---|
| `docker --version` | Shows the installed Docker version. |
| `systemctl status docker --no-pager` | Checks whether the Docker service is running. |
| `sudo docker run -d --name nginx-container -p 8080:80 nginx` | Creates and starts an Nginx container in the background, mapping VM port 8080 to container port 80. |
| `sudo docker ps` | Shows running containers. |
| `sudo docker ps -a` | Shows all containers, including stopped ones. |
| `sudo docker images` | Shows locally available container images. |
| `sudo docker stop nginx-container` | Stops the container without deleting it. |
| `sudo docker start nginx-container` | Starts an existing stopped container. |
| `sudo docker rm nginx-container` | Deletes a stopped container. |
| `sudo docker rmi nginx` | Deletes the local Nginx image. |

### Key concept

**Image** = reusable template used to create containers.  
**Container** = running or stopped instance created from an image.

> `docker stop` does not delete a container. `docker rm` deletes the container, while `docker rmi` deletes the image.

## KQL

| Query | Purpose |
|---|---|
| `Syslog` | Displays Syslog data collected in Log Analytics. |
| `Syslog \| take 20` | Returns a small sample of Syslog events. |
| `Syslog \| where Computer == "vm-cloud-operations-lab" \| take 20` | Filters events for the lab VM. |
| `Syslog \| where Facility == "daemon" \| order by TimeGenerated desc \| take 20` | Filters daemon events and shows the most recent entries first. |
| `Syslog \| where SyslogMessage contains "Cloud Operations Lab" \| order by TimeGenerated desc` | Searches for a specific test message. |
| `Syslog \| where SyslogMessage contains "nginx" \| order by TimeGenerated desc` | Finds Nginx-related service events. |
| `Syslog \| where SeverityLevel in ("warning", "err", "crit") \| order by TimeGenerated desc` | Searches for higher-severity Syslog events. |

### Basic pattern

`Table` → `where` → `order by` → `take`

> KQL was used in this lab to investigate centralized Linux logs in Azure Log Analytics.
