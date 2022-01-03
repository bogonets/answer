export default {
    title: 'Answer',

    rules: {
        required: '공백을 허용하지 않습니다.',
        at_least_4char: '최소 네 글자 이상 허용됩니다.',
        email: '이메일 형식이 올바르지 않습니다.',
        integer: '정수형 문자만 허용됩니다.',
        phone: '전화번호 형식이 올바르지 않습니다.',
        slug: '슬러그 형식이 올바르지 않습니다.',
        no_recc_prefix: "'recc.' 접두사 는 사용할 수 없습니다.",
    },

    toast: {
        request_success: '요청에 성공하였습니다.',
        request_failure: '요청에 실패하였습니다.',
        no_layout_read: '레이아웃 읽기 권한이 필요합니다.',
        no_layout_write: '레이아웃 쓰기 권한이 필요합니다.',
        no_storage_read: '저장소 읽기 권한이 필요합니다.',
        no_storage_write: '저장소 쓰기 권한이 필요합니다.',
        no_manager_read: '관리자 읽기 권한이 필요합니다.',
        no_manager_write: '관리자 쓰기 권한이 필요합니다.',
        no_graph_read: '그래프  읽기 권한이 필요합니다.',
        no_graph_write: '그래프 쓰기 권한이 필요합니다.',
        no_member_read: '멤버  읽기 권한이 필요합니다.',
        no_member_write: '멤버 쓰기 권한이 필요합니다.',
        no_setting_read: '설정 읽기 권한이 필요합니다.',
        no_setting_write: '설정 쓰기 권한이 필요합니다.',
    },

    permissions: {
        recc_domain_layout_view: '레이아웃 보기',
        recc_domain_layout_edit: '레이아웃 편집',
        recc_domain_file_view: '파일 보기',
        recc_domain_file_edit: '파일 편집',
        recc_domain_table_view: '테이블 보기',
        recc_domain_table_edit: '테이블 편집',
        recc_domain_task_view: '태스크 보기',
        recc_domain_task_edit: '태스크 편집',
        recc_domain_vp_view: '비주얼 프로그래밍 보기',
        recc_domain_vp_edit: '비주얼 프로그래밍 편집',
        recc_domain_member_view: '회원 보기',
        recc_domain_member_edit: '회원 편집',
        recc_domain_setting_view: '설정 보기',
        recc_domain_setting_edit: '설정 편집',
        recc_domain_delete: '도메인 제거',
        recc_domain_vms_live_view: 'VMS 실시간 보기',
        recc_domain_vms_live_edit: 'VMS 실시간 편집',
        recc_domain_vms_device_view: 'VMS 장치 보기',
        recc_domain_vms_device_edit: 'VMS 장치 편집',
        recc_domain_vms_event_view: 'VMS 이벤트 보기',
        recc_domain_vms_event_edit: 'VMS 이벤트 편집',
        recc_domain_airjoy_device_view: 'AIRJOY 장치 보기',
        recc_domain_airjoy_device_edit: 'AIRJOY 장치 편집',
        recc_domain_airjoy_live_view: 'AIRJOY 실시간 보기',
        recc_domain_airjoy_live_edit: 'AIRJOY 실시간 편집',
        recc_domain_airjoy_chart_view: 'AIRJOY 차트 보기',
        recc_domain_airjoy_chart_edit: 'AIRJOY 차트 편집',
        recc_domain_airjoy_service_view: 'AIRJOY 서비스 보기',
        recc_domain_airjoy_service_edit: 'AIRJOY 서비스 편집',
    },

    basic: {
        admin: "관리자",
        apply: "적용",
        back: "뒤로",
        cancel: "취소",
        change: "변경",
        clear: "지우기",
        close: "닫기",
        continue: "계속",
        create: "생성",
        delete: "삭제",
        download: "다운로드",
        edit: "수정",
        email: "이메일",
        guest: "게스트",
        left: "왼쪽",
        load: "불러오기",
        next: "다음",
        no: "아니오",
        ok: "확인",
        open: "열기",
        right: "오른쪽",
        save: "저장",
        submit: "제출",
        telephone: "전화번호",
        version: "버전",
        yes: "예",
    },

    main: {
        projects: "Projects",
        groups: "Groups",
    },

    config: {
        translations: {
            title: "언어선택",
        },
        account: {
            unknown_user: "알수없음"
        },
        admin: {
        },
    },

    version: "버전",
    submit: "제출",
    back: "뒤로",
    next: "다음",
    close: "닫기",
    save: "저장",
    load: "불러오기",
    download: "다운로드",
    change: "변경",
    edit: "수정",
    open: "열기",
    clear: "지우기",
    apply: "적용",
    cancel: "취소",
    create: "생성",
    delete: "삭제",
    ok: "확인",
    yes: "예",
    no: "아니오",
    continue: "계속",
    email: "이메일",
    telephone: "전화번호",
    left: "왼쪽",
    right: "오른쪽",

    checking_init_api: "API 초기화 체크중...",
    warn_alldata_clear: "모든 데이터가 삭제됩니다.",
    warn_olddata_clear: "이전 데이터가 삭제됩니다.",
    ques_want_delete: "삭제하시겠습니까?",
    ques_want_continue: "계속하시겠습니까?",
    translations: "언어선택",
    en: "영어",
    ko: "한국어",
    connecting_api: "API 서버 연결중 ...",
    unreachable_api: "API 서버 연결에 실패하였습니다.",
    uninitialized_api: "API 서버가 연결되었지만, 초기화되지 않았습니다.",
    connected_api: "API 연결 설공.",
    required_field: "공백을 허용하지 않습니다.",
    more_than_4char: "4자 이상이여야 합니다.",
    api_settings: "API 설정",
    api_change_origin: "서버 주소를 변경할 수 있습니다.",
    api_origin: "서버 주소",
    page_setting: "페이지 설정",
    auto_saved: "자동 저장됨",
    file_upload: "파일 올리기",
    phone_number: "휴대전화",
    goto_login: "로그인 페이지로",
    goto_project: "프로젝트로",
    graph_status: "그래프 상태 보기",
    graph_setting: "그래프 설정",
    null: "[없음]",
    theme: "테마",
    its_me: "나",
    permission: "권한",
    last_login: "마지막 로그인",
    active: "활동",
    demand: "필수",
    selection: "선택",
    duplicate_check: "중복 체크",
    available: "사용가능",
    unavailable: "사용불가",
    unknown: "알 수 없음",
    duplicated_username: {
        default: "중복 체크 해주세요.",
        success: "사용 가능한 계정명입니다.",
        error: "중복된 계정명입니다.",
    },
    min_greater_3: "최소 3자 이상",
    min_greater_4: "최소 4자 이상",
    same_password: "패스워드와 동일하게 작성하세요.",

    how_to: "방법",
    storage: "저장소",
    storage_logger: "이벤트 저장소",
    select_project_storage: "프로젝트 저장소를 선택하세요.",

    create_project: {
        descriptions:
        "이 페이지는 ANSWER의 새로운 프로젝트를 생성할 수 있습니다.",
        how_to:
        '중복되지 않는 프로젝트 명을 입력한 후 "생성" 버튼을 클릭해주세요.',
        new_project: "새로운 프로젝트",
        network_error: "네트워크가 원활하지 않습니다. 다시 시도해주세요.",
        empty_project_name: "빈 프로젝트 명입니다.",
        duplicated_error: "중복되는 프로젝트 명입니다.",
        duplicated_success: "사용 가능한 프로젝트 명입니다.",
    },
    discription: "설명",

    public_and_private: "공개/비공개",
    public: "공개",
    private: "비공개",

    project_list: "프로젝트 목록",
    project_name: "프로젝트 명",
    project_edit: "프로젝트 수정",
    projects: {
        add_success: "프로젝트 생성: 성공",
        add_failed: "프로젝트 생성: 실패",
        edit_success: "프로젝트 수정: 성공",
        edit_failed: "프로젝트 수정: 실패",
        delete_success: "프로젝트 삭제: 성공",
        delete_failed: "프로젝트 삭제: 실패",
        get_list_success: "프로젝트 목록 불러오기: 성공",
        get_list_failed: "프로젝트 목록 불러오기: 실패",
    },

    bucket: "버켓",
    buckets: {
        bucket_list: "버켓 목록",
        new_bucket: "새로운 버켓",
        bucket_name: "버켓 이름",
        add_success: "버켓 생성: 성공",
        add_failed: "버켓 생성: 실패",
        add_failed_duplicated: "버켓 생성: 실패 (중복 이름)",
        edit_success: "버켓 수정: 성공",
        edit_failed: "버켓 수정: 실패",
        delete_success: "버켓 삭제: 성공",
        delete_failed: "버켓 삭제: 실패",
        delete_failed_is_not_empty: "버켓 삭제: 실패 (빈 버켓이 아닙니다.)",
        get_list_success: "버켓 목록 불러오기: 성공",
        get_list_failed: "버켓 목록 불러오기: 실패",
        check_delete_bucket: "버켓을 정말로 삭제하시겠습니까?",
    },

    objects: {
        object_list: "오브젝트 목록",
        object_name: "오브젝트 이름",
        size: "파일 크기",
        add_success: "오브젝트 업로드: 성공",
        add_failed: "오브젝트 업로드: 실패",
        delete_success: "오브젝트 삭제: 성공",
        delete_failed: "오브젝트 삭제: 실패",
        get_list_success: "오브젝트 목록 불러오기: 성공",
        get_list_failed: "오브젝트 목록 불러오기: 실패",
        check_delete_object: "오브젝트를 정말로 삭제하시겠습니까?",
        folder_name: "폴더 명",
        duplicated_folder_name: "중복된 폴더 명",
        empty_folder_name: "빈 폴더 명",
        error_file: "잘못된 파일",
        unknown_file: "알수 없는 파일",
    },
    auto_change_dir: "자동 변환 폴더",

    manual: "수동",
    start: "시작",
    stop: "중지",
    loading: "로딩중",
    failed: "실패",
    success: "성공",
    information: "정보",
    copy: "복사",
    install: "설치",
    installed: "설치된",
    list: "목록",
    add_libs: "추가할 라이브러리",
    ex: "예시",
    fullscreen: "전체 창",
    defaultscreen: "이전 크기로 복원",
    show_chips: "칩 보기",

    execute: "실행",
    execute_success: "실행: 성공",
    execute_failed: "실행: 실패",
    save_failed: "그래프 저장: 실패",
    load_failed: "저장된 그래프 불러오기: 실패",
    load_template_failed: "람다 템플릿 불러오기: 실패",
    open_local: "로컬 파일 열기",
    download_local: "로컬 파일로 저장",
    show_graph_state: "그래프 상태 보기",

    layout_errors: {
        empty_name: "레이아웃 이름이 없습니다.",
        existed_name: "레이아웃 명이 이미 존재합니다.",
        check_console_log: "콘솔 창 로그 확인하십시오.",
    },
    loading_data: "데이터 로딩중...",
    empty_data: "데이터가 비어있습니다.",
    jupyter: {
        jupyter: "Jupyter",
        project_manage: "Jupyter 프로젝트 관리",
        new_project_name: "새로운 Jupyter 이름",
        pip_manage: "Jupyter Pip 관리",
        pip_installer: "Jupyter Pip 설치",
        pip_remove: "Jupyter Pip 제거",
        open_project: "Jupyter를 열어주세요",
    },
    empty_page: "빈 페이지",
    project: "프로젝트",
    manage: "관리",
    new: "새로운",
    created_time: "생성일",
    modified_time: "수정일",
    url: "주소",

    hours: "시간",
    minutes: "분",
    seconds: "초",

    collapsed_style: "접기 모드",
    horizontal_style: "세로 모드",
    pinned_style: "고정 모드",
    input: "입력",
    output: "출력",
    slot: "슬롯",
    tag: "태그",
    group: "그룹",
    signal: "신호",
    signals: "신호",
    detailsetting: {
        save_success: "저장 완료.",
        save_failed: "저장 실패",
        setname: "슬롯 이름을 설정하세요.",
        setsignals: "신호 이름을 설정하세요.",
        wrong_input_slot_setting: "잘못된 입력 슬롯 설정.",
        wrong_output_slot_setting: "잘못된 출려 슬롯 설정.",
    },

    language: "언어",
    user_name: "계정명",
    id: "아이디",
    password: "비밀번호",
    password_confirm: "비밀번호 확인",
    change_password: "비밀번호 변경",
    current_password: "현재 비밀번호",
    current_password_hint: "현재 암호를 변경하려면 암호를 제공해야 합니다.",
    server: "서버",
    server_is_not_opend: "서버가 열려 있지 않습니다.",
    dashboard: "대쉬보드",
    event: "이벤트",
    user: "회원",
    user_edit: "회원정보 수정",
    members: "회원",
    members_manage: "회원 관리",
    member_add_success: "회원 추가 성공",
    member_add_failed: "회원 추가 실패",
    member_edit_success: "회원 정보 변경 성공",
    member_edit_failed: "회원 정보 변경 실패",
    member_delete_success: "회원 삭제 성공",
    member_delete_failed: "회원 삭제 실패",
    get_member_list_success: "회원 목록 불러오기 성공",
    get_member_list_failed: "회원 목록 불러오기 실패",
    auth_management: "권한 관리",
    general_setting: "기본 설정",
    information_view: "정보 보기",
    add_user: "회원 추가",
    user_list: "회원 목록",
    datalist: "데이터 목록",
    search: "검색",
    add_group: "그룹 추가",
    select_group: "그룹 선택",
    select_data: "데이터 선택",
    no_group: "그룹 없음",
    group_list: "그룹 목록",
    select_authority: "권한 선택",
    sign_in: "로그인",
    sign_up: "회원 가입",
    signup: {
        descriptions: "이 페이지는 회원가입 페이지입니다.",
        how_to:
        '중복되지 않는 회원 명을 입력한 후 "회원가입" 버튼을 클릭해주세요.',
    },
    is_not_existed_admin: "관리자 계정이 존재하지 않습니다.",
    go_to_signup_admin: "관리자 가입 페이지로 이동합니다.",
    is_not_existed_admin_go_to_signup_admin:
    "관리자 계정이 존재하지 않아 관리자 가입 페이지로 이동합니다.",
    admin: "관리자",
    guest: "게스트",
    expired_time: "로그인 기간이 만료되었습니다.",
    setting: "설정",
    please_wait: "잠시만 기다려주세요.",
    login_error_message: {
        empty_id: "계정명을 입력해주세요.",
        empty_password: "비밀번호를 입력해주세요.",
        invalid_id_password: "계정 또는 비밀번호가 잘못되었습니다.",
        networkerror: "네트워크가 원활하지 않습니다. 다시 시도해주세요.",
    },
    join_error_message: {
        empty_id: "계정명을 입력해주세요.",
        empty_password: "비밀번호를 입력해주세요.",
        short_id: "아이디가 너무 짧습니다. (3자이상)",
        short_password: "비밀번호가 너무 짧습니다. (4자이상)",
        not_match_password: "비밀번호와 일치하지 않습니다.",
        email_format_error: "이메일 형식이 아닙니다.",
        networkerror: "네트워크가 원활하지 않습니다. 다시 시도해주세요.",
    },
    dialog_message: {
        delete: "정말로 삭제하시겠습니까?",
        user_delete: "회원을 정말로 삭제하시겠습니까?",
        project_delete: "프로젝트를 정말로 삭제하시겠습니까?",
    },
    default: "기본",
    profile: "프로필",
    logout: "로그 아웃",
    widgets: "위젯",
    preference: "설정",
    admin_setting: "관리자 설정",
    user_setting: "회원 관리",
    group_setting: "그룹 관리",
    video_setting: "비디오 설정",
    select_type: "유형 선택",
    select_type_sub_title: "사용할 유형을 선택하십시오.",
    realtime_cctv: "실시간 CCTV",
    video_player: "비디오 플레이어",
    audio_player: "오디오 플레이어",
    device_setting_title: "장치설정",
    device_list: "장치 목록",
    manual_setting: "수동 설정",
    device_name: "장치 이름",
    detail_setting: "상세 설정",
    required_setting: "상세 설정 내용이 필요합니다.",
    add: "추가",
    finish_text: "설정 완료",
    setup_finish: {
        finish_message: "설정이 완료되었습니다.",
        button_admin: "관리자 페이지로",
        button_main: "메인 페이지로",
    },

    have_no_layout: "저장된 레이아웃이 없습니다.",
    click_icon_addlayout: "아이콘을 클릭하여 레이아웃을 추가하여 주십시오.",

    video_load_success: "비디오 불러오기: 성공.",
    video_load_failed: "비디오 불러오기: 실패.",
    camera_select: "카메라 리스트",
    please_select_camera: "카메라를 선택해주세요.",

    data_select: "데이터 리스트",

    no_data_table: "데이터가 없습니다.",
    no_search_data: "검색한 데이터가 없습니다.",
    unit: "단위",

    layout_name: "레이아웃 명",
    panels_number: "사용할 창 개수",

    line_width: "선 두께",
    color: "색상",

    second: "초",
    limit_setting: "제한 설정",
    timer_setting: "타이머 설정",
    timer_start: "타이머 시작",
    timer_stop: "타이머 중지",
    timer_time_setting: "타이머 시간 설정",

    camera_player: "카메라 뷰어",
    data_table: "데이터 표",
    add_panel: "창 추가",

    layout: "레이아웃",
    event_area_setting: "이벤트 영역 설정",
    event_setting: "이벤트 설정",
    add_layout: "레이아웃 추가",

    ip: "아이피",
    port: "포트번호",

    data_setting: "데이터 설정",
    data_choice: "데이터 선택",
    empty_url: "카메라 URL이 없습니다.",

    task: "태스크",
    lambda: "람다",
    lambda_duplicated: "람다 중복",
    lambda_viewer: "람다 뷰어",
    lambda_template: "람다 템플릿",
    task_duplicated: "태스크 중복",
    output_slot: "출력 슬롯",
    add_task: "태스크 추가",
    add_lambda: "람다 추가",
    add_lambda_in_task: "태스크안에 람다 추가",
    add_lambda_in: "에 람다 추가",
    clone_task: "태스크 복사",
    clone_lambda: "람다 복사",
    remove_lambda: "람다 삭제",
    remove_task: "태스크 삭제",
    optimization_size: "크기 최적화",

    connection_will_disconnected:
    "슬롯이 연결되어 있다면, 연결이 끊어집니다.",

    properties: "속성",
    shape: "모양",
    visual_setting: "설정",
    lambda_must_belong_to_task: "람다는 태스크에 속해야 합니다.",
    lambda_is_not_exist: "람다가 존재하지 않습니다.",
    task_is_not_exist: "태스크가 존재하지 않습니다.",
    make_lambda_please: "람다를 만들어주십시오.",
    make_task_please: "태스크를 만들어주십시오.",
    already_task_in: "이미 태스크에 속해 있습니다.",
    wrong_edge_setting: "잘못된 Edge 설정.",
    empty_begin_end: "Begin람다와 End람다 모두 없습니다.",
    empty_begin: "Begin람다가 없습니다.",
    empty_end: "End람다가 없습니다.",
    task_id: "태스크 아이디",
    lambda_id: "람다 아이디",
    please_check: "확인해 주시기 바랍니다.",
    preset: "프리셋",
    name: "이름",
    please_write_preset_name: "프리셋 이름을 작성하세요.",
    info: "알림",
    warning: "경고",
    error: "에러",
    task_manager: "태스크 매니저",
    persons: "명",

    lambdaInfo: {
        original_name: "본래 이름",
        author: "작성자",
        mime_type: "MIME 타입",
        engines: "엔진",
        use_system_packages: "시스템 패키지 사용 여부",
        use: "사용",
        unuse: "사용하지 않음",
        bug_report: "버그 리포트",
        homepage: "홈페이지",
        descriptions: "설명",
    },

    info_delete_save_value: "저장된 설정값이 삭제됩니다.",
    info_delete_lambda_save_value:
    "태스크에 속한 람다와 저장된 설정값이 삭제됩니다.",
    q_want_delete_task: "태스크를 삭제하시겠습니까?",
    q_want_delete_lambdas: "람다를 삭제하시겠습니까?",
    q_want_delete_layout: "레이아웃을 삭제하시겠습니까?",
    q_want_move: "이동하시겠습니까?",

    detail: "상세",
    to: "에서",
    mode: "방식",
    line: "선",
    rect: "사각형",
    poly: "다각형",
    arc: "원",

    drawcanvas: {
        line: "선",
        rectangle: "사각형",
        circle: "원",
        polygon: "다각형",
        delete: "전체 삭제",
        guideline: "가이드라인",
    },

    auto_reconnector: "자동 재연결",
    server_is_dead: "서버가 죽었습니다.",
    check_rtcserver_try_again: "RTC서버를 확인하신 후 다시 시도해 주십시오.",
    please_retry: "재시도 해주십시오.",
    connect_success: "연결 성공",

    reconnect_setting: "재연결 설정",
    reconnect_interval: "재연결 간격 설정",
    reconnect_number: "재연결 횟수 제한",
    unlimited: "제한 해제",
    start_playing_video: "비디오(카메라) 영상을 재생합니다.",
    try_reconnect: "재연결 시도",

    object_draw_type: "객체 보기 유형",
    only_bbox: "사각형",
    only_points: "다각형",
    both_all_see: "모두 보기",
    none_see: "모두 보지않기",

    label_setting: "라벨 설정",
    label_number: "설정된 라벨 수",
    label: "라벨",

    widget_list: "위젯 목록",
    plz_add_widget: "위젯을 추가해 주세요.",
    component_list: "컴포넌트 목록",
    open_component_list: "컴포넌트 목록 열기",
    delete_layout: "레이아웃 삭제",
    delete_panel: "창 삭제",
    header: "헤더",
    category: "카테고리",
    current_img_save: "현재 이미지 저장",
    zoom_in: "확대하기",
    zoom_out: "축소하기",
    no_img: "이미지가 없습니다.",
    no_text: "텍스트가 없습니다.",
    image_load_failed: "이미지 불러오기 실패.",
    image_viewer: "이미지뷰어",
    image_viewer2: "이미지뷰어2",
    latest: "최신",
    index: "인덱스",
    popupwindow: "팝업창",
    refresh: "새로고침",
    plugin: "플러그인",

    network: {
        status_code: "상태 코드",
    },

    renewal: "갱신",
    show_rois: "ROI 모두 보기",
    greater_than: "기준보다 클때",
    less_than: "기준보다 작을때",
    within_range: "두 기준 사이일때",
    out_of_range: "두 기준 밖일때",
    threshold: "임계치",
    rgb_color: "RGB 색상",
    line_style: "선 색상",
    airjoy: "에어조이",
    airjoy_manage: "에어조이 모니터링",
    airjoy_graph: "에어조이 그래프",
    airjoy_monitor: "에어조이 모니터",
    project_member: "프로젝트 멤버",
    add_member: "멤버 추가",
    authentication: "권한",
    member_list: "멤버 목록",
    all_select: "[전부 선택]",
    auths: {
        administrator: "관리자",
        operator: "부관리자",
        guest: "게스트",
    },
    start_date: "시작 날짜",
    end_date: "종료 날짜",
    one_day: "1일",
    one_week: "1주일",
    one_month: "1개월",
    six_month: "6개월",
    term: "기간",
    live: "실시간",
    agency_name: "기관명",
    initialize: "초기화",
    change_property: "속성변경",
    wind_control: "풍량조절",
}
