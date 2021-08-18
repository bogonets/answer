# -*- coding: utf-8 -*-

from recc.http import http_path_keys as p

# Depth root.
root = "/"

# Depth 1st.
app = "/app"
api = "/api"

# Static files.
index = "/index.html"
favicon = "/favicon.ico"
app_index = app + index
app_favicon = app + favicon

# Depth 2nd.
v1 = "/v1"
v2 = "/v2"

# Depth 3rd.
admin = "/admin"
already = "/already"
configs = "/configs"
extra = "/extra"
groups = "/groups"
heartbeat = "/heartbeat"
infos = "/infos"
init = "/init"
overview = "/overview"
password = "/password"
permissions = "/permissions"
projects = "/projects"
public = "/public"
self = "/self"
signin = "/signin"
signup = "/signup"
state = "/state"
system = "/system"
templates = "/templates"
test = "/test"
users = "/users"
version = "/version"


def _param_path(key: str) -> str:
    return "/{" + key + "}"


# Params (Use the prefix 'p')
pgroup = _param_path(p.group)
pkey = _param_path(p.key)
pname = _param_path(p.name)
pperm = _param_path(p.perm)
pproject = _param_path(p.project)
puser = _param_path(p.user)

# Mixin for ROOT
api_v1 = api + v1
api_v2 = api + v2
api_v2_public = api + v2 + public

# Mixin (api prefix)
api_version = api + version
api_heartbeat = api + heartbeat

# Mixin (api/v2 sub)
configs_pkey = configs + pkey
groups_pgroup = groups + pgroup
infos_pkey = infos + pkey
permissions_pperm = permissions + pperm
projects_pgroup_pproject = projects + pgroup + pproject
signup_admin = signup + admin
state_already = state + already
system_overview = system + overview
users_puser = users + puser

# Mixin (api/v2/self sub)
self_extra = self + extra
self_groups = self + groups
self_groups_pgroup = self + groups + pgroup
self_password = self + password
self_projects = self + projects
self_projects_pgroup_pproject = self + projects + pgroup + pproject
