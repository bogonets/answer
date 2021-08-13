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
infos = "/infos"
extra = "/extra"
heartbeat = "/heartbeat"
init = "/init"
overview = "/overview"
password = "/password"
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
pkey = _param_path(p.key)
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
infos_pkey = infos + pkey
projects_pproject = projects + pproject
self_extra = self + extra
self_password = self + password
signup_admin = signup + admin
state_already = state + already
system_overview = system + overview
users_puser = users + puser
test_init = test + init
