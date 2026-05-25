import json
import os

#####
# Auto Permission Sync
#####
# should generally only be used for sources that support polling of permissions
# e.g. can pull in only permission changes rather than having to go through all
# documents every time
DEFAULT_PERMISSION_DOC_SYNC_FREQUENCY = int(
    os.environ.get("DEFAULT_PERMISSION_DOC_SYNC_FREQUENCY") or 5 * 60
)


#####
# Confluence
#####

# In seconds, default is 30 minutes
CONFLUENCE_PERMISSION_GROUP_SYNC_FREQUENCY = int(
    os.environ.get("CONFLUENCE_PERMISSION_GROUP_SYNC_FREQUENCY") or 30 * 60
)
# In seconds, default is 30 minutes
CONFLUENCE_PERMISSION_DOC_SYNC_FREQUENCY = int(
    os.environ.get("CONFLUENCE_PERMISSION_DOC_SYNC_FREQUENCY") or 30 * 60
)
# This is a boolean that determines if anonymous access is public
# Default behavior is to not make the page public and instead add a group
# that contains all the users that we found in Confluence
CONFLUENCE_ANONYMOUS_ACCESS_IS_PUBLIC = (
    os.environ.get("CONFLUENCE_ANONYMOUS_ACCESS_IS_PUBLIC", "").lower() == "true"
)


#####
# JIRA
#####

# In seconds, default is 30 minutes
JIRA_PERMISSION_DOC_SYNC_FREQUENCY = int(
    os.environ.get("JIRA_PERMISSION_DOC_SYNC_FREQUENCY") or 30 * 60
)
# In seconds, default is 30 minutes
JIRA_PERMISSION_GROUP_SYNC_FREQUENCY = int(
    os.environ.get("JIRA_PERMISSION_GROUP_SYNC_FREQUENCY") or 30 * 60
)


#####
# Google Drive
#####
GOOGLE_DRIVE_PERMISSION_GROUP_SYNC_FREQUENCY = int(
    os.environ.get("GOOGLE_DRIVE_PERMISSION_GROUP_SYNC_FREQUENCY") or 5 * 60
)


#####
# GitHub
#####
# In seconds, default is 5 minutes
GITHUB_PERMISSION_DOC_SYNC_FREQUENCY = int(
    os.environ.get("GITHUB_PERMISSION_DOC_SYNC_FREQUENCY") or 5 * 60
)
# In seconds, default is 5 minutes
GITHUB_PERMISSION_GROUP_SYNC_FREQUENCY = int(
    os.environ.get("GITHUB_PERMISSION_GROUP_SYNC_FREQUENCY") or 5 * 60
)


#####
# Slack
#####
SLACK_PERMISSION_DOC_SYNC_FREQUENCY = int(
    os.environ.get("SLACK_PERMISSION_DOC_SYNC_FREQUENCY") or 5 * 60
)

NUM_PERMISSION_WORKERS = int(os.environ.get("NUM_PERMISSION_WORKERS") or 2)


#####
# Teams
#####
# In seconds, default is 5 minutes
TEAMS_PERMISSION_DOC_SYNC_FREQUENCY = int(
    os.environ.get("TEAMS_PERMISSION_DOC_SYNC_FREQUENCY") or 5 * 60
)

#####
# SharePoint
#####
# In seconds, default is 30 minutes
SHAREPOINT_PERMISSION_DOC_SYNC_FREQUENCY = int(
    os.environ.get("SHAREPOINT_PERMISSION_DOC_SYNC_FREQUENCY") or 30 * 60
)

# In seconds, default is 5 minutes
SHAREPOINT_PERMISSION_GROUP_SYNC_FREQUENCY = int(
    os.environ.get("SHAREPOINT_PERMISSION_GROUP_SYNC_FREQUENCY") or 5 * 60
)


####
# Celery Job Frequency
####
CHECK_TTL_MANAGEMENT_TASK_FREQUENCY_IN_HOURS = float(
    os.environ.get("CHECK_TTL_MANAGEMENT_TASK_FREQUENCY_IN_HOURS") or 1
)  # float for easier testing


STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")

# JWT Public Key URL
JWT_PUBLIC_KEY_URL: str | None = os.getenv("JWT_PUBLIC_KEY_URL", None)


# Super Users
SUPER_USERS = json.loads(os.environ.get("SUPER_USERS", "[]"))
SUPER_CLOUD_API_KEY = os.environ.get("SUPER_CLOUD_API_KEY", "api_key")

POSTHOG_API_KEY = os.environ.get("POSTHOG_API_KEY")
POSTHOG_HOST = os.environ.get("POSTHOG_HOST") or "https://us.i.posthog.com"
POSTHOG_DEBUG_LOGS_ENABLED = (
    os.environ.get("POSTHOG_DEBUG_LOGS_ENABLED", "").lower() == "true"
)

MARKETING_POSTHOG_API_KEY = os.environ.get("MARKETING_POSTHOG_API_KEY")

HUBSPOT_TRACKING_URL = os.environ.get("HUBSPOT_TRACKING_URL")

GATED_TENANTS_KEY = "gated_tenants"

# License enforcement - when True, blocks API access for gated/expired licenses
LICENSE_ENFORCEMENT_ENABLED = (
    os.environ.get("LICENSE_ENFORCEMENT_ENABLED", "true").lower() == "true"
)

# Internal enterprise build: single control point that disables license
# expiration / seat-limit enforcement and tier gating, and forces tier
# resolution to ENTERPRISE for self-hosted deployments. Auth, RBAC, tenant
# isolation, and admin permission checks are unaffected. Defaults to false
# so upstream behavior is unchanged unless explicitly opted in.
INTERNAL_BUILD = os.environ.get("INTERNAL_BUILD", "").lower() == "true"

# White-label branding: when WHITE_LABEL_ENABLED is true, the env values
# below override any stored EnterpriseSettings values at API response time.
# Admins can still set fields via the existing admin UI for any env var
# that is left unset. When WHITE_LABEL_ENABLED is false the overlay is a
# no-op and existing branding behavior is preserved.
WHITE_LABEL_ENABLED = os.environ.get("WHITE_LABEL_ENABLED", "").lower() == "true"
WHITE_LABEL_APP_NAME = os.environ.get("APP_NAME") or None
WHITE_LABEL_COMPANY_NAME = os.environ.get("COMPANY_NAME") or None
WHITE_LABEL_SUPPORT_EMAIL = os.environ.get("SUPPORT_EMAIL") or None
WHITE_LABEL_SUPPORT_URL = os.environ.get("SUPPORT_URL") or None
WHITE_LABEL_PRIMARY_BRAND_COLOR = os.environ.get("PRIMARY_BRAND_COLOR") or None
WHITE_LABEL_LOGO_URL = os.environ.get("LOGO_URL") or None
WHITE_LABEL_FAVICON_URL = os.environ.get("FAVICON_URL") or None
WHITE_LABEL_FOOTER_BRANDING = os.environ.get("FOOTER_BRANDING") or None

# Cloud data plane URL - self-hosted instances call this to reach cloud proxy endpoints
# Used when MULTI_TENANT=false (self-hosted mode)
CLOUD_DATA_PLANE_URL = os.environ.get(
    "CLOUD_DATA_PLANE_URL", "https://cloud.onyx.app/api"
)
