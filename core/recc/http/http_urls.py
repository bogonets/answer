# -*- coding: utf-8 -*-

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
config = "/config"
extra = "/extra"
heartbeat = "/heartbeat"
init = "/init"
login = "/login"
public = "/public"
self = "/self"
signup = "/signup"
test = "/test"
user = "/user"
version = "/version"

# Params (Use the prefix 'p')
pkey = "/{key}"

# Mixin for ROOT
api_v1 = api + v1
api_v2 = api + v2
api_v2_public = api + v2 + public

# Mixin
api_version = api + version
api_heartbeat = api + heartbeat
config_pkey = config + pkey
self_extra = self + extra
signup_admin = signup + admin
test_init = test + init
