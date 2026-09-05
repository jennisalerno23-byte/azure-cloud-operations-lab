import urllib.request
import urllib.error
import json
import shutil
import datetime
import os


# =========================
# CONFIGURATION
# =========================

url = "http://localhost"

storage_account = os.getenv("STORAGE_ACCOUNT_NAME")
container_name = os.getenv("STORAGE_CONTAINER_NAME", "health-reports")

if not storage_account:
    raise RuntimeError(
        "STORAGE_ACCOUNT_NAME environment variable is required"
    )


# =========================
# FUNCTIONS
# =========================

def get_status(percent):
    if percent >= 90:
        return "CRITICAL"
    elif percent >= 70:
        return "WARNING"
    else:
        return "HEALTHY"


def get_managed_identity_token():
    token_url = (
        "http://169.254.169.254/metadata/identity/oauth2/token"
        "?api-version=2018-02-01"
        "&resource=https://storage.azure.com/"
    )

    request = urllib.request.Request(
        token_url,
        headers={"Metadata": "true"}
    )

    with urllib.request.urlopen(request, timeout=5) as response:
        data = json.loads(response.read().decode())

    return data["access_token"]


def upload_report(report, blob_name, token):
    blob_url = (
        f"https://{storage_account}.blob.core.windows.net/"
        f"{container_name}/{blob_name}"
    )

    report_bytes = report.encode("utf-8")

    request = urllib.request.Request(
        blob_url,
        data=report_bytes,
        method="PUT",
        headers={
            "Authorization": f"Bearer {token}",
            "x-ms-version": "2023-11-03",
            "x-ms-blob-type": "BlockBlob",
            "Content-Type": "text/plain"
        }
    )

    with urllib.request.urlopen(request, timeout=10) as response:
        return response.status


# =========================
# HEALTH CHECK
# =========================

statuses = []
report_lines = []

timestamp = datetime.datetime.now()

report_lines.append("=== CLOUD OPERATIONS HEALTH CHECK ===")
report_lines.append(f"Timestamp: {timestamp}")


# HTTP / NGINX

try:
    response = urllib.request.urlopen(url, timeout=5)
    status_code = response.getcode()

    if status_code == 200:
        nginx_status = "HEALTHY"
    else:
        nginx_status = "WARNING"

    statuses.append(nginx_status)

    report_lines.append(f"Nginx status: {nginx_status}")
    report_lines.append(f"HTTP status: {status_code}")

except Exception as error:
    statuses.append("CRITICAL")

    report_lines.append("Nginx status: DOWN")
    report_lines.append(f"HTTP error: {error}")


# DISK

disk = shutil.disk_usage("/")
disk_percent = (disk.used / disk.total) * 100
disk_status = get_status(disk_percent)

statuses.append(disk_status)

report_lines.append(
    f"Disk usage: {disk_percent:.1f}% [{disk_status}]"
)


# MEMORY

with open("/proc/meminfo", "r") as file:
    memory_info = file.readlines()

mem_total = int(memory_info[0].split()[1])
mem_available = int(memory_info[2].split()[1])

mem_used_percent = (
    (mem_total - mem_available) / mem_total
) * 100

memory_status = get_status(mem_used_percent)

statuses.append(memory_status)

report_lines.append(
    f"Memory usage: {mem_used_percent:.1f}% [{memory_status}]"
)


# OVERALL STATUS

if "CRITICAL" in statuses:
    overall_status = "CRITICAL"
elif "WARNING" in statuses:
    overall_status = "WARNING"
else:
    overall_status = "HEALTHY"

report_lines.append(f"OVERALL STATUS: {overall_status}")


# =========================
# DISPLAY REPORT
# =========================

report = "\n".join(report_lines)

print(report)


# =========================
# UPLOAD TO AZURE BLOB
# =========================

blob_timestamp = timestamp.strftime("%Y%m%d-%H%M%S")
blob_name = f"health-check-{blob_timestamp}.txt"

try:
    token = get_managed_identity_token()

    upload_status = upload_report(
        report,
        blob_name,
        token
    )

    print(f"Blob upload: SUCCESS [{upload_status}]")
    print(f"Blob name: {blob_name}")

except urllib.error.HTTPError as error:
    print(f"Blob upload: FAILED [HTTP {error.code}]")
    print(error.read().decode())

except Exception as error:
    print("Blob upload: FAILED")
    print(f"Error: {error}")
