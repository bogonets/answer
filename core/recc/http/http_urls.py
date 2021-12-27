# -*- coding: utf-8 -*-

from typing import Optional
from recc.http import http_path_keys as p

# Depth root.
empty = ""
root = "/"

# Depth 1st.
app = "/app"
app_root = app + root
api = "/api"

# Static files.
index = "/index.html"
favicon = "/favicon.ico"
app_index = app + index
app_favicon = app + favicon

# Depth 2nd.
v1 = "/v1"
v2 = "/v2"

# Depth 3rd ~.
admin = "/admin"
already = "/already"
configs = "/configs"
containers = "/containers"
daemon = "/daemon"
daemons = "/daemons"
dev = "/dev"
environments = "/environments"
extra = "/extra"
groups = "/groups"
heartbeat = "/heartbeat"
infos = "/infos"
init = "/init"
main = "/main"
members = "/members"
names = "/names"
oem = "/oem"
overview = "/overview"
password = "/password"
permissions = "/permissions"
plugin = "/plugin"
plugins = "/plugins"
projects = "/projects"
public = "/public"
raw = "/raw"
refresh = "/refresh"
role = "/role"
roles = "/roles"
self = "/self"
signin = "/signin"
signup = "/signup"
start = "/start"
state = "/state"
stop = "/stop"
system = "/system"
tasks = "/tasks"
templates = "/templates"
test = "/test"
token = "/token"
usernames = "/usernames"
users = "/users"
version = "/version"
versions = "/versions"


def _param_path(key: str, pattern: Optional[str] = None) -> str:
    if pattern:
        return "/{" + key + ":" + pattern + "}"
    else:
        return "/{" + key + "}"


# Params (Use the prefix 'p')
pcontainer = _param_path(p.container)
pdaemon = _param_path(p.daemon)
pgroup = _param_path(p.group)
pkey = _param_path(p.key)
pname = _param_path(p.name)
pmember = _param_path(p.member)
prole = _param_path(p.role)
pplugin = _param_path(p.plugin)
pproject = _param_path(p.project)
ptail = _param_path(p.tail, r".*")
ptask = _param_path(p.task)
puser = _param_path(p.user)

# Mixin for ROOT
api_v1 = api + v1
api_v2 = api + v2
api_v2_admin = api + v2 + admin
api_v2_dev = api + v2 + dev
api_v2_main = api + v2 + main
api_v2_public = api + v2 + public
api_v2_self = api + v2 + self
api_v2_plugins = api + v2 + plugins

# Mixin (/api)
api_version = api + version
api_heartbeat = api + heartbeat

# Mixin (/api/v2)
configs_pkey = configs + pkey
containers_pcontainer = containers + pcontainer
daemon_plugins = daemon + plugins
daemons_pdaemon = daemons + pdaemon
daemons_pdaemon_start = daemons_pdaemon + start
daemons_pdaemon_stop = daemons_pdaemon + stop
groups_pgroup = groups + pgroup
groups_pgroup_members = groups_pgroup + members
groups_pgroup_members_pmember = groups_pgroup_members + pmember
groups_pgroup_projects = groups_pgroup + projects
infos_oem = infos + oem
infos_pkey = infos + pkey
permissions_pgroup = permissions + pgroup
permissions_pgroup_pproject = permissions_pgroup + pproject
plugin_names = plugin + names
pplugin_ptail = pplugin + ptail
projects_pgroup_pproject = projects + pgroup + pproject
projects_pgroup_pproject_overview = projects_pgroup_pproject + overview
projects_pgroup_pproject_members = projects_pgroup_pproject + members
projects_pgroup_pproject_members_pmember = projects_pgroup_pproject_members + pmember
roles_prole = roles + prole
roles_pgroup = roles + pgroup
roles_pgroup_pproject = roles + pgroup + pproject
signup_admin = signup + admin
state_already = state + already
system_overview = system + overview
system_versions = system + versions
tasks_ptask = tasks + ptask
tasks_pgroup_pproject = tasks + pgroup + pproject
token_refresh = token + refresh
users_puser = users + puser
