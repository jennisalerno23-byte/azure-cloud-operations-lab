# Day 3 - Identity, RBAC and Storage

## Implemented
- System Assigned Managed Identity on Linux VM
- Azure Storage Account
- Private Blob Container: health-reports
- RBAC: Storage Blob Data Contributor
- Python health check upload to Blob Storage

## Validations
- Managed Identity obtained Azure token successfully
- Manual Blob upload succeeded
- health_check.py uploaded CRITICAL and HEALTHY reports
- Blob upload returned HTTP 201

## Troubleshooting
- Microsoft.Storage provider was not registered
- Removing RBAC caused HTTP 403 AuthorizationPermissionMismatch
- Restoring RBAC restored Blob upload successfully

## Key concept
Authentication = Who are you?
Authorization = What are you allowed to do?
