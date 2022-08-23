#!/usr/bin/env bash

USAGE="
Usage: $0 [options]

Available options are:
  -h, --help       Print this message.
  --skip-apt       Skip installing dependency packages.
  -c, --cleanup    Remove all cache files after installation is complete.
  -v, --verbose    Be more verbose/talkative during the operation.
  --               Stop handling options.
"

CLEANUP_FLAG=0
VERBOSE_FLAG=0
SKIP_APT_FLAG=0

PYTHON_VERSION=3.9.13
PYTHON_ARCHIVE=Python-${PYTHON_VERSION}.tgz
PYTHON_DOWNLOAD_URL="https://www.python.org/ftp/python/${PYTHON_VERSION}/${PYTHON_ARCHIVE}"
PYTHON_DOWNLOAD_MD5=eafda83543bad127cadef4d288fdab87

PREFIX_DIR=/usr/local/recc

RECC_PYTHON_DIR=$PREFIX_DIR/python
RECC_PYTHON_BIN=$RECC_PYTHON_DIR/bin
RECC_PYTHON_LIB=$RECC_PYTHON_DIR/lib
RECC_PYTHON_INC=$RECC_PYTHON_DIR/include
RECC_PYTHON_SRC=$PREFIX_DIR/Python-${PYTHON_VERSION}
RECC_PYTHON_ARCHIVE=$PREFIX_DIR/$PYTHON_ARCHIVE
RECC_PYTHON_EXE=$RECC_PYTHON_BIN/python3

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
    # shellcheck disable=SC2145
    echo -e "\033[32m$@\033[0m"
}

function print_error
{
    # shellcheck disable=SC2145
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
        chown "$user:$group" "$dir"
    fi
}

function exists_program_or_exit
{
    local name=$1

    if [[ ! -x $(which "$name" 2> /dev/null) ]]; then
        print_error "Not found $name"
        exit 1
    fi
}

function get_core_count
{
    local platform
    platform=$(uname -s)

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
    local thread_count=1
    local core_count
    core_count=$(get_core_count)

    if [[ $core_count -ge 1 ]]; then
        thread_count=$(( core_count * 2 ))
    else
        thread_count=1
    fi
    echo "$thread_count"
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

function checksum_or_exit
{
    local file_path=$1
    local checksum=$2
    local result
    result=$(get_file_checksum "$file_path")

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

    local ext
    local ext_lower
    ext=$(get_file_extension "$file")
    ext_lower=$(to_lower "$ext")

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

    if [[ -n "$md5_checksum" ]]; then
        checksum_or_exit "$file" "$md5_checksum"
    fi
}

# shellcheck disable=SC2120
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

function cleanup_cache
{
    if [[ -d "$RECC_PYTHON_SRC" ]]; then
        print_verbose "Remove python source directory: $RECC_PYTHON_SRC"
        rm -rf "$RECC_PYTHON_SRC"
    fi
    if [[ -f "$RECC_PYTHON_ARCHIVE" ]]; then
        print_verbose "Remove the downloaded python compressed file: $RECC_PYTHON_SRC"
        rm "$RECC_PYTHON_ARCHIVE"
    fi
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
    --skip-apt)
        SKIP_APT_FLAG=1
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

if [[ $(id -u) -ne 0 ]]; then
    print_error "Please run as root."
    exit 1
fi

if [[ -x "$RECC_PYTHON_EXE" ]]; then
    print_message "Already python executable: $RECC_PYTHON_EXE"
    exit 0
fi

check_dir_or_create "$PREFIX_DIR"
check_dir_or_create "$RECC_PYTHON_DIR"

if [[ $SKIP_APT_FLAG -eq 1 ]]; then
    print_verbose "Skip installing dependency packages."
else
    print_message "Install debian dependencies ..."
    apt-get update
    apt-get install -y \
        git make pkg-config build-essential llvm gdb \
        lcov wget curl lzma lzma-dev uuid-dev xz-utils tk-dev \
        zlib1g-dev libbz2-dev liblzma-dev \
        libssl-dev libreadline-dev libncursesw5-dev \
        libxml2-dev libxmlsec1-dev libffi-dev \
        libsqlite3-dev libgdbm-dev libgdbm-compat-dev
    check_code_or_exit
fi

print_message "Download python source file ..."
checked_download "$RECC_PYTHON_ARCHIVE" "$PYTHON_DOWNLOAD_URL" "$PYTHON_DOWNLOAD_MD5"

print_message "Extract python source file ..."
extract "$RECC_PYTHON_ARCHIVE" "$PREFIX_DIR"

if [[ ! -d "$RECC_PYTHON_SRC" ]]; then
    print_eror "Not found python source directory: $RECC_PYTHON_SRC"
    exit 1
fi

pushd "$PWD" > /dev/null || exit 1
cd "$RECC_PYTHON_SRC" || exit 1

LDFLAGS="-L/opt/X11/lib -L$RECC_PYTHON_LIB -Wl,-rpath=$RECC_PYTHON_LIB"
CPPFLAGS="-I/opt/X11/include -I$RECC_PYTHON_INC"
export LDFLAGS
export CPPFLAGS

print_message "Configuring ..."
./configure \
    --prefix=$RECC_PYTHON_DIR \
    --libdir=$RECC_PYTHON_LIB \
    --enable-shared \
    --enable-optimizations \
    --with-lto
check_code_or_exit

print_message "Making ..."
make -s "-j$(get_build_thread_count)" install
check_code_or_exit

popd > /dev/null || exit 1

if [[ $CLEANUP_FLAG -eq 1 ]]; then
    print_message "Cleaning ..."
    cleanup_cache
fi
