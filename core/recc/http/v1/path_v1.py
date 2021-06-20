# -*- coding: utf-8 -*-

# [No authentication]
initialization = "/initialization"
signup_admin = "/users/admin"
login = "/login"
refresh_token = "/login"
get_core_version = "/version/core"
get_api_version = "/version/api"

# [Authentication]
test_login = "/login/test"

# user
get_users = "/users"
add_user = "/users"
delete_user = "/users"
set_user = "/users"
exist_user = "/users/{usr}"
get_user = "/users/{usr}/get"

# graph
get_templates = "/graph/templates"

# project
get_projects = "/project"
set_project = "/project"
exist_project = "/project/projectName"
get_project = "/project/{proj}"
create_project = "/project/{proj}"
delete_project = "/project/{proj}"

# project/layout
create_layout = "/project/{proj}/layout"
get_layouts = "/project/{proj}/layouts"
get_layout = "/project/{proj}/layout/{layout}"
set_layout_extra = "/project/{proj}/layout/{layout}"
delete_layout_extra = "/project/{proj}/layout/{layout}"
exist_layout = "/project/{proj}/layouts/check"

# project/graph
get_proj_graph = "/project/{proj}/graph"
set_proj_graph = "/project/{proj}/graph"
get_proj_graph_status = "/project/{proj}/graph/infos"
stop_proj_task = "/project/{proj}/graph/stop/{task}"
get_proj_task_prop = "/project/{proj}/graph/main/tasks/{task}/lambda-props"
set_proj_task_prop = "/project/{proj}/graph/main/tasks/{task}/lambda-props"
send_proj_task_signal = "/project/{proj}/graph/main/tasks/{task}/lambda-signal"
get_property_hint = "/nodeTypes/{type}/properties/{prop}/hint"

# project/bucket
get_buckets = "/projects/{proj}/buckets"
create_bucket = "/projects/{proj}/buckets"
delete_bucket = "/projects/{proj}/buckets/{bucket}"
get_bucket_objs = "/projects/{proj}/buckets/{bucket}/objects"
get_bucket_obj = "/projects/{proj}/buckets/{bucket}/objects/{obj}"
set_bucket_obj = "/projects/{proj}/buckets/{bucket}/objects"
delete_bucket_obj = "/projects/{proj}/buckets/{bucket}/objects/{obj}"

# widget/jupyter
get_jupyters = "/project/{proj}/jupyters"
new_jupyter = "/project/{proj}/jupyters"
delete_jupyter = "/project/{proj}/jupyters/{jupyter}"
get_pips = "/pips"
get_pip = "/pips/{pip}"
add_pips = "/pips"
remove_pips = "/pips"
remove_pip = "/pips/{pip}"

# widget/image_viewer
get_image_by_viewer = (
    "/signal/projects/{proj}/tasks/{task}/nodes/{lambda}/slots/{out}/image"
)

# Unused
_save_event_roi = "/graphs/{node}/properties/{prop}"
_get_table_data_list = "/datalist"
_get_table_category_list = "/datalist/{data}"
_get_table_data = "/datalist/{data}/{category}"
_get_image_latest = "/datalist/{plugin}/{category}/image"
_get_image_from_index = "/datalistImage/{index}"
_get_rtc_host = "/graph/webrtcurls"
_set_event_list = "/project/{proj}/eventlist"
