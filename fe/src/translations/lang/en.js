export default {
    title: 'Answer',

    rules: {
        required: 'Required field.',
        at_least_4char: 'At least 4 characters.',
        email: 'Email format is incorrect.',
        integer: 'Only integer characters are allowed.',
        phone: 'Phone format is incorrect.',
        slug: 'Slug format is incorrect.',
        no_recc_prefix: "'recc.' prefix cannot be used.",
    },

    toast: {
        request_success: 'The request was successful',
        request_failure: 'The request failed',
        no_layout_read: 'Layout read permission is required',
        no_layout_write: 'Layout write permission is required',
        no_storage_read: 'Storage read permission is required',
        no_storage_write: 'Storage write permission is required',
        no_manager_read: 'Manager read permission is required',
        no_manager_write: 'Manager write permission is required',
        no_graph_read: 'Graph read permission is required',
        no_graph_write: 'Graph write permission is required',
        no_member_read: 'Member read permission is required',
        no_member_write: 'Member write permission is required',
        no_setting_read: 'Setting read permission is required',
        no_setting_write: 'Setting write permission is required',
    },

    permissions: {
        recc_domain_layout_view: 'Layout View',
        recc_domain_layout_edit: 'Layout Edit',
        recc_domain_storage_view: 'Storage View',
        recc_domain_storage_edit: 'Storage Edit',
        recc_domain_manager_view: 'Manager View',
        recc_domain_manager_edit: 'Manager Edit',
        recc_domain_graph_view: 'Graph View',
        recc_domain_graph_edit: 'Graph Edit',
        recc_domain_member_view: 'Member View',
        recc_domain_member_edit: 'Member Edit',
        recc_domain_setting_view: 'Setting View',
        recc_domain_setting_edit: 'Setting Edit',
        recc_domain_delete: 'Domain Delete',
    },

    basic: {
        admin: "AdminOverview.vue",
        apply: "Apply",
        back: "Back",
        cancel: "Cancel",
        change: "Change",
        clear: "Clear",
        close: "Close",
        continue: "Continue",
        create: "Create",
        delete: "Delete",
        download: "Download",
        edit: "Edit",
        email: "Email",
        guest: "Guest",
        left: "Left",
        load: "Load",
        next: "Next",
        no: "No",
        ok: "Ok",
        open: "Open",
        right: "Right",
        save: "Save",
        submit: "Submit",
        telephone: "Telephone",
        version: "Version",
        yes: "Yes",
    },

    main: {
        projects: "Projects",
        groups: "Groups",
    },

    config: {
        translations: {
            title: "Translations",
        },
        account: {
            unknown_user: "Unknown"
        },
        admin: {
        },
    },

    version: "Version",
    submit: "Submit",
    back: "Back",
    next: "Next",
    close: "Close",
    save: "Save",
    load: "Load",
    download: "Download",
    change: "Change",
    edit: "Edit",
    open: "Open",
    clear: "Clear",
    apply: "Apply",
    cancel: "Cancel",
    create: "Create",
    delete: "Delete",
    ok: "Ok",
    yes: "Yes",
    no: "No",
    continue: "Continue",
    email: "Email",
    telephone: "Telephone",
    left: "Left",
    right: "Right",

    checking_init_api: "Checking API initialization...",
    warn_alldata_clear: "All data will be deleted.",
    warn_olddata_clear: "All old data will be deleted.",
    ques_want_delete: "Are you sure you want to delete it?",
    ques_want_continue: "Are you sure you want to continue?",
    translations: "Translations",
    en: "English",
    ko: "Korean",
    connecting_api: "Connecting to API server...",
    unreachable_api: "Unreachable API server.",
    uninitialized_api: "A reachable but uninitialized API.",
    connected_api: "API connection successful.",
    required_field: "Required field",
    more_than_4char: "It must be at least 4 characters long.",
    api_settings: "API Settings",
    api_change_origin: "You can change the API origin address.",
    api_origin: "Origin address",
    page_setting: "Page Setting",
    auto_saved: "Auto saved",
    file_upload: "File upload",
    phone_number: "Phone Number",
    goto_login: "Go to login page",
    goto_project: "Go to Project",
    graph_status: "Graph Status Board",
    graph_setting: "Graph Setting",
    null: "[Null]",
    theme: "Theme",
    its_me: "It's me",
    permission: "Permission",
    last_login: "Last login",
    active: "Active",
    demand: "Demand",
    selection: "Selection",
    duplicate_check: "duplicate check",
    available: "Available",
    unavailable: "Unavailable",
    unknown: "Unknown",
    duplicated_username: {
        default: "Please duplication check.",
        success: "The user name is available.",
        error: "Duplicate account name.",
    },
    min_greater_3: "At least three characters.",
    min_greater_4: "At least four characters.",
    same_password: "Fill in the same password.",

    how_to: "How to",
    storage: "Storage",
    storage_logger: "Storage_logger",
    select_project_storage: "Select Storage of Project",

    create_project: {
        descriptions: "This page creates a new project of Answer.",
        how_to:
        'Please enter a project name that does not overlap and click the "Create" button.',
        new_project: "New Project",
        network_error: "Network Error. Please try again.",
        empty_project_name: "Empty project name.",
        duplicated_error: "Duplicated project name.",
        duplicated_success: "This project name is available.",
    },
    discription: "Discription",

    public_and_private: "Public/Private",
    public: "Public",
    private: "Private",

    project_list: "Project list",
    project_name: "Project name",
    project_edit: "Project Edit",
    projects: {
        add_success: "Project create: Success.",
        add_failed: "Project create: Failed.",
        edit_success: "Project edit: Success.",
        edit_failed: "Project edit: Failed.",
        delete_success: "Project delete: Success.",
        delete_failed: "Project delete: Failed.",
        get_list_success: "Project list load: Success.",
        get_list_failed: "Project list load: Failed.",
    },
    bucket: "Bucket",
    buckets: {
        bucket_list: "Bucket list",
        new_bucket: "New bucket",
        bucket_name: "Bucket name",
        add_success: "Create Bucket: Success",
        add_failed: "Create Bucket: Failed",
        add_failed_duplicated: "Create Bucket: Failed (Duplicated Name.)",
        edit_success: "Edit Bucket: Success",
        edit_failed: "Edit Bucket: Failed",
        delete_success: "Delete Bucket: Success",
        delete_failed: "Delete Bucket: Failed",
        delete_failed_is_not_empty: "Delete Bucket: Failed (Is not empty.)",
        get_list_success: "Load bucket list: Success",
        get_list_failed: "Load bucket list: Failed",
        check_delete_bucket: "Are you sure you want to delete the bucket?",
    },

    objects: {
        object_list: "Objcet list",
        object_name: "Objcet name",
        size: "File Size",
        add_success: "Upload Object: Success",
        add_failed: "Upload Object: Failed",
        delete_success: "Delete Object: Success",
        delete_failed: "Delete Object: Failed",
        get_list_success: "Load object list: Success",
        get_list_failed: "Load object list: Success",
        check_delete_object: "Are you sure you want to delete the object?",
        folder_name: "Folder Name",
        duplicated_folder_name: "Duplicated folder name.",
        empty_folder_name: "Empty folder name.",
        error_file: "Error file",
        unknown_file: "Unknown file",
    },
    auto_change_dir: "Automatic conversion dir",

    manual: "Manual",
    start: "Start",
    stop: "Stop",
    loading: "Loading",
    failed: "Failed",
    success: "Success",
    information: "Information",
    copy: "Copy",
    install: "Install",
    installed: "Installed",
    list: "List",
    add_libs: "Add Library",
    ex: "Ex",
    fullscreen: "FullScreen",
    defaultscreen: "Restore size",
    show_chips: "Show chips",

    execute: "Execute",
    execute_success: "Execute: Success",
    execute_failed: "Execute: Failed",
    save_failed: "Save: Failed",
    load_failed: "Load: Failed",
    load_template_failed: "Load Lambda Template: Failed",
    open_local: "Open local file.",
    download_local: "Save to local.",
    show_graph_state: "Show graph state",

    layout_errors: {
        empty_name: "Layout name is empty.",
        existed_name: "Existed layout name.",
        check_console_log: "Check console log.",
    },
    loading_data: "Loading Data...",
    empty_data: "Empty data.",
    jupyter: {
        jupyter: "Jupyter",
        project_manage: "Jupyter Project Manage",
        new_project_name: "New Jupyter Name",
        pip_manage: "Jupyter Pip Manage",
        pip_installer: "Install Jupyter Pip",
        pip_remove: "Remove Jupyter Pip",
        open_project: "Open Jupyter",
    },
    empty_page: "Empty Page",
    project: "Project",
    manage: "Manage",
    new: "New",
    created_time: "Created Time",
    modified_time: "Modified Time",
    url: "Url",

    hours: "Hour",
    minutes: "Min",
    seconds: "Seconds",

    collapsed_style: "Folding mode",
    horizontal_style: "Length mode",
    pinned_style: "Pinned mode",
    input: "Input",
    output: "Output",
    slot: "Slot",
    tag: "Tag",
    group: "Group",
    signal: "Signal",
    signals: "Signals",
    detailsetting: {
        save_success: "Save Success.",
        save_failed: "Save Failed.",
        setname: "Set slot name",
        setsignals: "Set signal name",
        wrong_input_slot_setting: "Wrong Input Slot Setting.",
        wrong_output_slot_setting: "Wrong Output Slot Setting.",
    },

    language: "Language",
    user_name: "User Name",
    id: "id",
    password: "Password",
    password_confirm: "Confirm Password",
    change_password: "Change Password",
    current_password: "Current Password",
    current_password_hint:
    "You must provide your current password in order to change it.",
    server: "Server",
    server_is_not_opend: "Server is not opend.",
    dashboard: "Dashboard",
    event: "Event",
    user: "User",
    user_edit: "Modify member information",
    members: "Members",
    members_manage: "Members manage",
    member_add_success: "Successfully add member.",
    member_add_failed: "Failed to add member.",
    member_edit_success: "Successfully changed member information",
    member_edit_failed: "Failed to change member information",
    member_delete_success: "Successfully deleted member information",
    member_delete_failed: "Failed to delete member information",
    get_member_list_success: "Successfully loaded member list.",
    get_member_list_failed: "Failed to load member list.",
    auth_management: "Authentication Management",
    general_setting: "General setting",
    information_view: "Information view",
    add_user: "Add User",
    user_list: "User List",
    datalist: "Data List",
    search: "Search",
    add_group: "Add Group",
    select_group: "Select Group",
    select_data: "Select Data",
    no_group: "No Group",
    group_list: "Group List",
    select_authority: "Select Authority",
    sign_in: "Sign in",
    sign_up: "Sign up",
    signup: {
        descriptions: "This page is a sign-up page.",
        how_to:
        'Please enter a project name that does not overlap and click the "Sign up" button.',
    },
    is_not_existed_admin: "Administrator account does not exist.",
    go_to_signup_admin: "Go to Administrator Sign up page.",
    is_not_existed_admin_go_to_signup_admin:
    "Administrator account does not exist and will be taken to the Admin sign-up page.",
    admin: "AdminOverview.vue",
    guest: "Guest",
    expired_time: "The period has expired.",
    setting: "Setting",
    please_wait: "Please wait.",
    login_error_message: {
        empty_id: "Please Input UserName.",
        empty_password: "Please Input Password.",
        invalid_id_password: "Invalid ID or password.",
        network_error: "Network Error. Please try again.",
    },
    join_error_message: {
        empty_id: "Please Input UserName.",
        empty_password: "Please Input Password.",
        short_id: "ID is too short. (at least 3 character needed.)",
        short_password: "Password is too short. (at least 4 character needed.)",
        not_match_password: "Does not Match Password.",
        email_format_error: "Email format is incorrect.",
        network_error: "Network Error. Please try again.",
    },
    dialog_message: {
        delete: "Are you sure you want to delete?",
        user_delete: "Are you sure you want to delete the members?",
        project_delete: "Are you sure you want to delete the project?",
    },
    default: "Default",
    profile: "Profile",
    logout: "Log out",
    widgets: "Widgets",
    preference: "Preference",
    admin_setting: "Admin Settings",
    user_setting: "User Setting",
    group_setting: "Group Setting",
    video_setting: "Video Setting",
    select_type: "Select Type",
    select_type_sub_title: "Select the type to use.",
    realtime_cctv: "Realtime CCTV",
    video_player: "Video Player",
    audio_player: "Audio Player",
    device_setting_title: "Device Setting",
    device_list: "Device List",
    manual_setting: "Manual Setting",
    device_name: "Device Name",
    detail_setting: "Detail Setting",
    required_setting: "Detailed settings are required.",
    add: "ADD",
    finish_text: "Setup Finish",
    setup_finish: {
        finish_message: "Setup is successfully completed.",
        button_admin: "To Admin Page",
        button_main: "To Main Page",
    },

    have_no_layout: "You have no Layout.",
    click_icon_addlayout: "Please click the icon to add a layout.",

    video_load_success: "Video load: Success.",
    video_load_failed: "Video load: Failed.",
    camera_select: "Camera List",
    please_select_camera: "Please Select Camera.",

    data_select: "Data List",

    no_data_table: "No Data.",
    no_search_data: "No data has been searched.",
    unit: "unit",

    layout_name: "Layout Name",
    panels_number: "Panels Number",

    line_width: "Line Width",
    color: "Color",

    second: "s",
    limit_setting: "Limit Setting",
    timer_setting: "Timer Setting",
    timer_start: "Timer Start",
    timer_stop: "Timer Stop",
    timer_time_setting: "Timer Time Setting",

    camera_player: "Camera Player",
    data_table: "Data Table",
    add_panel: "Add Panel",

    layout: "Layout",
    event_setting: "Event Setting",
    event_area_setting: "Event Area Setting",
    add_layout: "Add Layout",

    ip: "IP",
    port: "PORT",

    data_setting: "Data Setting",
    data_choice: "Data Select",
    empty_url: "Empty Camera url",

    task: "Task",
    lambda: "Lambda",
    lambda_duplicated: "Duplicated lambda",
    lambda_viewer: "Lambda Viewer",
    lambda_template: "Lambda Template",
    task_duplicated: "Duplicated task",
    output_slot: "Output Slot",
    add_task: "Add Task",
    add_lambda: "Add Lambda",
    add_lambda_in_task: "Add Lambda in Task",
    add_lambda_in: "Add Lambda in",
    clone_task: "Clone Task",
    clone_lambda: "Clone Lambda",
    remove_lambda: "Remove Lambda",
    remove_task: "Remove Task",
    optimization_size: "Optimization size",

    connection_will_disconnected:
    "If slot is connected, the connection will be disconnected.",

    properties: "Properties",
    shape: "Shape",
    visual_setting: "Visual Setting",
    lambda_must_belong_to_task: "Lambda must belong to Task.",
    lambda_is_not_exist: "Lambda is not exist.",
    task_is_not_exist: "Task is not exist.",
    make_lambda_please: "Please make Lambda.",
    make_task_please: "Please make Task.",
    already_task_in: "Already part of the task.",
    wrong_edge_setting: "Wrong edge setting",
    empty_begin_end: "Empty Begin lambda and End lambda.",
    empty_begin: "Empty Begin lambda.",
    empty_end: "Empty End lambda.",
    task_id: "Task ID",
    lambda_id: "Lambda ID",
    please_check: "Please Check.",
    preset: "Preset",
    name: "Name",
    please_write_preset_name: "Please fill out Preset Name.",
    info: "Info",
    warning: "Warning",
    error: "Error",
    task_manager: "Task Manager",
    persons: "Persons",

    lambdaInfo: {
        original_name: "Original name",
        author: "Author",
        mime_type: "MIME type",
        engines: "Engines",
        use_system_packages: "Use system packages",
        use: "Used",
        unuse: "Unused",
        bug_report: "Bug report",
        homepage: "Homepage",
        descriptions: "Descriptions",
    },

    info_delete_save_value: "The saved settings will be deleted.",
    info_delete_lambda_save_value:
    "Saved Lambda and Saved Data will be deleted.",
    q_want_delete_task: "Are you sure you want to delete the Task?",
    q_want_delete_lambdas: "Are you sure you want to delete the Lambda?",
    q_want_delete_layout: "Are you sure you want to delete the layout?",
    q_want_move: "Want to move?",

    detail: "Detail",
    to: "to",
    mode: "Mode",
    line: "Line",
    rect: "Rectangle",
    poly: "Polygon",
    arc: "Arc",

    drawcanvas: {
        line: "Line",
        rectangle: "Rectangle",
        circle: "Circle",
        polygon: "Polygon",
        delete: "All clear",
        guideline: "Guide line",
    },

    auto_reconnector: "Auto Reconnect",
    server_is_dead: "Server is dead.",
    check_rtcserver_try_again: "Please check the server and try again.",
    please_retry: "Please retry.",
    connect_success: "Connection Successful",

    reconnect_setting: "Reconnection Setting",
    reconnect_interval: "Reconnection Time Iterval",
    reconnect_number: "Number of reconnection",
    unlimited: "Unlimited",
    start_playing_video: "Start playing video(camera).",
    try_reconnect: "Try reconnection",

    object_draw_type: "Object drawing type",
    only_bbox: "Rectangle",
    only_points: "Polygon",
    both_all_see: "Both",
    none_see: "None",

    label_setting: "Label setting",
    label_number: "Number of label",
    label: "Label",

    widget_list: "Widget list",
    plz_add_widget: "Please add widgets.",
    component_list: "Component list",
    open_component_list: "Open Component list.",
    delete_layout: "Delete Layout",
    delete_panel: "Delete window",

    header: "Header",
    category: "Category",
    current_img_save: "Save Current Image",
    zoom_in: "Zoom IN",
    zoom_out: "Zoom OUT",
    no_img: "No Image",
    no_text: "No Text",
    image_load_failed: "Image load failed.",
    image_viewer: "ImageViewer",
    image_viewer2: "ImageViewer2",
    latest: "Latest",
    index: "Index",
    popupwindow: "Popup",
    refresh: "Refresh",
    plugin: "Plugin",

    network: {
        status_code: "Status code",
    },

    renewal: "Renewal",
    show_rois: "Show Rois",
    greater_than: "Greater Than",
    less_than: "Less Than",
    within_range: "Within Range",
    out_of_range: "Out of Rnage",
    threshold: "Threshold",
    rgb_color: "RGB Color",
    line_style: "Line Style",
    airjoy: "AIRJOY",
    airjoy_manage: "Airjoy Manage",
    airjoy_graph: "Airjoy Graph",
    airjoy_monitor: "Airjoy Monitor",
    project_member: "Project Member",
    add_member: "Add Member",
    authentication: "Authentication",
    member_list: "Member List",
    all_select: "[All Select]",
    auths: {
        administrator: "Administrator",
        operator: "Operator",
        guest: "Guest",
    },
    start_date: "Start Date",
    end_date: "End Date",
    one_day: "1Day",
    one_week: "1Week",
    one_month: "1Month",
    six_month: "6Month",
    term: "TERM",
    live: "LIVE",
    agency_name: "Agency Name",
    initialize: "Initialize",
    change_property: "Change Prop",
    wind_control: "Wind Control",
}
