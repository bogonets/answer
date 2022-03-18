#!/usr/bin/env bash

if [[ $(id -u) -ne 0 ]]; then
    echo 'Please run as root.'
    exit 1
fi

USAGE="
Usage: $0 [options]

Available options are:
  -h, --help       Print this message.
  -u, --uninstall  Remove all installed files.
  -c, --cleanup    Remove all cache files after installation is complete.
  -v, --verbose    Be more verbose/talkative during the operation.
  --               Stop handling options.
"

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" || exit; pwd)
SOURCE_ROOT_DIR=$(cd "$SCRIPT_DIR/.." || exit; pwd)
SOURCE_CORE_DIR=$(cd "$SOURCE_ROOT_DIR/core" || exit; pwd)
SOURCE_FE_DIR=$(cd "$SOURCE_ROOT_DIR/fe" || exit; pwd)

UNINSTALL_FLAG=0
CLEANUP_FLAG=0
VERBOSE_FLAG=0

PYTHON_VERSION=3.9.11
PYTHON_FILE=Python-${PYTHON_VERSION}.tgz
PYTHON_DOWNLOAD_URL="https://www.python.org/ftp/python/${PYTHON_VERSION}/${PYTHON_FILE}"
PYTHON_DOWNLOAD_MD5=f7890dd43302daa5fcb7b0254b4d0f33

RECC_ROOT_DIR=/usr/local/recc
RECC_DEPENDENCIES=$RECC_ROOT_DIR/dependencies
RECC_PYTHON_DIR=$RECC_ROOT_DIR/python
RECC_PYTHON_BIN=$RECC_PYTHON_DIR/bin
RECC_PYTHON_LIB=$RECC_PYTHON_DIR/lib
RECC_PYTHON_INC=$RECC_PYTHON_DIR/include
RECC_PYTHON_SRC=$RECC_ROOT_DIR/Python-${PYTHON_VERSION}
RECC_PYTHON_FILE=$RECC_ROOT_DIR/$PYTHON_FILE
RECC_PYTHON_EXE=$RECC_PYTHON_BIN/python3
RECC_PYTHON_PIP=$RECC_PYTHON_BIN/pip3
RECC_HOME_DIR=$RECC_ROOT_DIR/home

RECC_STORAGE_DIR=$RECC_HOME_DIR/storage
RECC_CONFIG_PATH=$RECC_HOME_DIR/config.yml
RECC_LOGGING_PATH=$RECC_HOME_DIR/logging.yml

RECC_SERVICE_SRC="$SCRIPT_DIR/recc.service"
RECC_SERVICE_DEST="/etc/systemd/system/recc.service"
RECC_JOURNAL_SRC="$SCRIPT_DIR/journald@recc.conf"
RECC_JOURNAL_DEST="/etc/systemd/journald@recc.conf"
RECC_CTL_SRC="$SCRIPT_DIR/recctl"
RECC_CTL_DEST="/usr/local/bin/recctl"

RECC_USER=recc
RECC_GROUP=recc

trap 'cancel_installation' INT

function cancel_installation
{
    local msg="An interrupt signal was detected."
    echo -e "\033[31m$msg\033[0m" 1>&2
    exit 1
}

function print_verbose
{
    if [[ $VERBOSE_FLAG -eq 1 ]]; then
        echo "$@"
    fi
}

function print_message
{
    echo -e "\033[32m$@\033[0m"
}

function print_error
{
    echo -e "\033[31m$@\033[0m" 1>&2
}

function check_dir_or_create
{
    local dir=$1
    if [[ -d "$dir" ]]; then
        print_verbose "Exists directory: $dir"
    else
        print_verbose "Create directory: $dir"
        mkdir -p "$dir"
    fi
}

function check_dir_or_create_chown
{
    local dir=$1
    local user=$2
    local group=$3
    if [[ -d "$dir" ]]; then
        print_verbose "Exists directory: $dir"
    else
        print_verbose "Create directory: $dir"
        mkdir -p "$dir"
        chown $user:$group "$dir"
    fi
}

function exists_program_or_exit
{
    local name=$1
    local var_name=$2
    local which_path=$(which $name 2> /dev/null)

    if [[ ! -x "$which_path" ]]; then
        print_error "Not found $name"
        exit 1
    fi
    if [[ ! -z $var_name ]]; then
        eval "$var_name=$which_path"
    fi
}

function get_core_count
{
    local platform=$(uname -s)
    case "$platform" in
    Darwin)
        exists_program_or_exit sysctl
        sysctl -n hw.ncpu
        ;;
    *)
        exists_program_or_exit grep
        grep -c '^processor' /proc/cpuinfo
        ;;
    esac
}

function get_build_thread_count
{
    local core_count=$(get_core_count)
    local thread_count=1
    if [[ $core_count -ge 1 ]]; then
        let "thread_count = $core_count * 2"
    fi
    echo $thread_count
}

function get_datetime
{
    local prefix=$1
    local suffix=$2
    local datetime=$(date '+%Y%m%d_%H%M%S')
    echo "$prefix$datetime$suffix"
}

function get_file_checksum
{
    local file=$1
    case "$(uname -s)" in
    Darwin)
        exists_program_or_exit md5
        exists_program_or_exit awk
        md5 -r "$file" | awk '{print $1}'
        ;;
    *)
        exists_program_or_exit md5sum
        exists_program_or_exit awk
        md5sum "$file" | awk '{print $1}'
        ;;
    esac
}

function get_variable_checksum
{
    local var=$1
    case "$(uname -s)" in
    Darwin)
        exists_program_or_exit md5
        exists_program_or_exit awk
        echo "$var" | md5 -r | awk '{print $1}'
        ;;
    *)
        exists_program_or_exit md5sum
        exists_program_or_exit awk
        echo "$var" | md5sum | awk '{print $1}'
        ;;
    esac
}

function checksum_or_exit
{
    local file_path=$1
    local checksum=$2
    local result=$(get_file_checksum "$file_path")
    if [[ "$result" != "$checksum" ]]; then
        print_error "Checksum error: actual(${result}) vs expected(${checksum})"
        exit 1
    fi
}

function get_file_extension
{
    local file=$1
    echo "${file#*.}"
}

function get_file_name
{
    local file=$1
    echo "${file%%.*}"
}

function to_lower
{
    local var=$1
    exists_program_or_exit awk
    echo "$var" | awk '{print tolower($0)}'
}

function extract
{
    local file=$1
    local output=$2
    ## $3 ... More arguments of the command.
    shift 2

    if [[ ! -f "$file" ]]; then
        print_error "File not found: $file"
        exit 1
    fi
    if [[ -z $output ]]; then
        output=$PWD
    fi
    if [[ ! -d "$output" ]]; then
        mkdir -p "$output"
    fi

    local ext=$(get_file_extension "$file")
    local ext_lower=$(to_lower "$ext")

    case $ext_lower in
    .zip)
        exists_program_or_exit unzip
        unzip "$@" -qo "$file" -d "$output"
        ;;
    *)
        exists_program_or_exit tar
        tar "$@" -xf "$file" -C "$output"
        ;;
    esac
}

function download
{
    local file=$1
    local url=$2
    ## $3 ... More arguments of the command.
    shift 2

    if [[ ! -f "$file" ]]; then
        print_verbose "Download $url -> $file"
        exists_program_or_exit curl
        curl "$@" -L -k -o "$file" "$url"
    else
        print_verbose "Exists file: $file"
    fi
}

function git_sync
{
    local url=$1
    local dest=$2
    exists_program_or_exit git
    if [[ -d "$dest" ]]; then
        pushd "$PWD" > /dev/null
        cd "$dest"
        git pull
        popd > /dev/null
    else
        git clone --depth 1 "$url" "$dest"
    fi
}

function checked_download
{
    local file=$1
    local url=$2
    local md5_checksum=$3
    shift 3

    if [[ -z $file ]]; then
        print_error "File argument is empty."
        exit 1
    fi
    if [[ -z $url ]]; then
        print_error "URL argument is empty."
        exit 1
    fi

    download "$file" "$url" "$@"

    if [[ ! -z "$md5_checksum" ]]; then
        checksum_or_exit "$file" "$md5_checksum"
    fi
}

function check_code_or_exit
{
    local code=$?
    local msg=$1
    if [[ $code -ne 0 ]]; then
        print_error "An error has been detected (exit=$code,file=${BASH_SOURCE[0]})"
        if [[ -n $msg ]]; then
            print_error "$msg"
        fi
        exit $code
    fi
}

function test_installed_dpkg
{
    exists_program_or_exit sed
    local result=`dpkg --get-selections $1 | sed -E 's/^([^\t ]+)[[:space:]]+([^\t ]+)$/\2/g'`
    if [[ "$result" == "install" ]]; then
        echo 1
    else
        echo 0
    fi
}

function install_python
{
    if [[ -x "$RECC_PYTHON_EXE" ]]; then
        print_verbose "Already python executable: $RECC_PYTHON_EXE"
        return
    fi

    checked_download "$RECC_PYTHON_FILE" "$PYTHON_DOWNLOAD_URL" "$PYTHON_DOWNLOAD_MD5"
    extract "$RECC_PYTHON_FILE" "$RECC_ROOT_DIR"

    if [[ ! -d "$RECC_PYTHON_SRC" ]]; then
        print_eror "Not found python source directory: $RECC_PYTHON_SRC"
        exit 1
    fi

    pushd "$PWD" > /dev/null
    cd "$RECC_PYTHON_SRC"

    LDFLAGS="-L/opt/X11/lib -L$RECC_PYTHON_LIB -Wl,-rpath=$RECC_PYTHON_LIB" \
    CPPFLAGS="-I/opt/X11/include -I$RECC_PYTHON_INC" \
    ./configure \
        --prefix=$RECC_PYTHON_DIR \
        --libdir=$RECC_PYTHON_LIB \
        --enable-shared \
        --enable-optimizations \
        --with-lto
    check_code_or_exit

    make -s -j$(get_build_thread_count) install
    check_code_or_exit

    popd > /dev/null
}

function install_debian_dependencies
{
    apt-get update
    apt-get install -y "$@"
}

function test_and_install_debian_dependencies
{
    local packages="$@"

    if [[ -f "$RECC_DEPENDENCIES" ]]; then
        local prev_checksum=$(get_file_checksum "$RECC_DEPENDENCIES")
        local next_checksum=$(get_variable_checksum "$packages")

        print_verbose "Dependencies checksum prev: "$prev_checksum
        print_verbose "Dependencies checksum next: "$next_checksum

        if [[ "$prev_checksum" == "$next_checksum" ]]; then
            print_verbose "Dependencies checksum is equals"
            return
        fi
    fi

    install_debian_dependencies $packages
    check_code_or_exit

    echo "$packages" > "$RECC_DEPENDENCIES"
}

function install_user_and_group
{
    exists_program_or_exit awk
    exists_program_or_exit grep

    local exists_user=$(cat /etc/passwd | awk -F: '{print $1}' | grep recc)
    if [[ -n $exists_user ]]; then
        print_verbose "Exists '$RECC_USER' user"
    else
        exists_program_or_exit useradd
        print_verbose "Create '$RECC_USER' user"
        useradd -l -M -N -d "$RECC_HOME_DIR" -s /bin/bash "$RECC_USER"
    fi

    local exists_group=$(cat /etc/group | awk -F: '{print $1}' | grep recc)
    if [[ -n $exists_group ]]; then
        print_verbose "Exists '$RECC_GROUP' group"
    else
        exists_program_or_exit groupadd
        exists_program_or_exit gpasswd
        exists_program_or_exit usermod
        print_verbose "Create '$RECC_GROUP' group"
        groupadd "$RECC_GROUP"
        gpasswd -a "$RECC_USER" "$RECC_GROUP"
        usermod -aG docker "$RECC_USER"
    fi

    check_dir_or_create_chown "$RECC_HOME_DIR" "$RECC_USER" "$RECC_GROUP"
    check_dir_or_create_chown "$RECC_STORAGE_DIR" "$RECC_USER" "$RECC_GROUP"
}

function cleanup_cache
{
    if [[ -d "$RECC_PYTHON_SRC" ]]; then
        print_verbose "Remove python source directory: $RECC_PYTHON_SRC"
        rm -rf "$RECC_PYTHON_SRC"
    fi
    if [[ -f "$RECC_PYTHON_FILE" ]]; then
        print_verbose "Remove the downloaded python compressed file: $RECC_PYTHON_SRC"
        rm "$RECC_PYTHON_FILE"
    fi
}

function test_and_copy
{
    local src=$1
    local dest=$2
    if [[ -f "$dest" ]]; then
        print_verbose "Exists '$dest' file."
    else
        print_verbose "Copy '$src' -> '$dest'"
        cp "$src" "$dest"
    fi
}

function test_and_copy_recc_file
{
    local src=$1
    local dest=$2
    if [[ -f "$dest" ]]; then
        print_verbose "Exists '$dest' file."
    else
        print_verbose "Copy '$src' -> '$dest'"
        cp "$src" "$dest"
        chown $RECC_USER:$RECC_GROUP "$dest"
    fi
}

function install_recc
{
    exists_program_or_exit grep
    local exists_recc=$("$RECC_PYTHON_PIP" list | grep recc | sed 's/  */-/g')
    if [[ -n "$exists_recc" ]]; then
        print_verbose "Exists $exists_recc"
        exit 0
    fi

    if [[ ! -d "$RECC_HOME_DIR" ]]; then
        print_error "Not exists home directory: $RECC_HOME_DIR"
        exit 1
    fi

    print_message "Build front-end ..."
    exists_program_or_exit yarn
    yarn --cwd "$SOURCE_FE_DIR" build

    print_message "Update PIP ..."
    "$RECC_PYTHON_PIP" install --upgrade pip

    print_message "Update Cython ..."
    "$RECC_PYTHON_PIP" install cython

    print_message "Install main requirements ..."
    "$RECC_PYTHON_PIP" install -r "$SOURCE_CORE_DIR/requirements.main.txt"

    print_message "Build core ..."
    "$RECC_PYTHON_EXE" "$SOURCE_CORE_DIR/setup.py" install

    print_message "Copy other files ..."
    test_and_copy_recc_file "$SOURCE_CORE_DIR/logging.yml" "$RECC_HOME_DIR/logging.yml"
    test_and_copy_recc_file "$SOURCE_CORE_DIR/config.yml" "$RECC_HOME_DIR/config.yml"
    test_and_copy "$RECC_CTL_SRC" "$RECC_CTL_DEST"
    test_and_copy "$RECC_SERVICE_SRC" "$RECC_SERVICE_DEST"
    test_and_copy "$RECC_JOURNAL_SRC" "$RECC_JOURNAL_DEST"
}

function print_usage
{
    echo "$USAGE"
}

while [[ -n $1 ]]; do
    case $1 in
    -h|--help)
        print_usage
        exit 0
        ;;
    -u|--uninstall)
        UNINSTALL_FLAG=1
        shift
        ;;
    -c|--cleanup)
        CLEANUP_FLAG=1
        shift
        ;;
    -v|--verbose)
        VERBOSE_FLAG=1
        shift
        ;;
    --)
        shift
        break
        ;;
    *)
        print_error "Unknown option: $1"
        exit 1
        ;;
    esac
done

if [[ $UNINSTALL_FLAG -eq 1 ]]; then
    read -p "Remove all installed files? (y/n)" USER_ANSWER
    case "$USER_ANSWER" in
    y|Y)
      rm -rf "$RECC_ROOT_DIR"
      rm "$RECC_SERVICE_DEST"
      rm "$RECC_JOURNAL_DEST"
      exit 0
      ;;
    *)
      exit 1
      ;;
    esac
fi

check_dir_or_create "$RECC_ROOT_DIR"
check_dir_or_create "$RECC_PYTHON_DIR"

print_message "Install debian dependencies ..."
test_and_install_debian_dependencies \
    git make pkg-config build-essential llvm gdb \
    lcov wget curl lzma lzma-dev uuid-dev xz-utils tk-dev \
    zlib1g-dev libbz2-dev liblzma-dev \
    libssl-dev libreadline-dev libncursesw5-dev \
    libxml2-dev libxmlsec1-dev libffi-dev \
    libsqlite3-dev libgdbm-dev libgdbm-compat-dev

print_message "Install python ..."
install_python

print_message "Install user and group ..."
install_user_and_group

print_message "Install recc ..."
install_recc

if [[ $CLEANUP_FLAG -eq 1 ]]; then
    print_message "Cleanup cache ..."
    cleanup_cache
fi
