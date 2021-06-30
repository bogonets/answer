# RECC

Restructured Engine for the Cyclops Cloud

## Packages

- **core**: Backend REST API/Core Node.
- **fe**: Frontend Web.

## Release

### Upgrade Version

버전은 패키지별로 관리한다.

## Development

### PyCharm CE setup

- 자동완성을 위해 `core` 디렉토리는 `Sources Root` 로 지정한다
  1. 해당 디렉토리에 마우스 커서 올려놓고 마우스 우클릭.
  2. `Mark Directory as > Sources Root` 메뉴 선택.
- 자동완성을 위해 `core/recc` 디렉토리는 `Namespace package` 로 지정한다
  1. 해당 디렉토리에 마우스 커서 올려놓고 마우스 우클릭.
  2. `Mark Directory as > Namespace package` 메뉴 선택.
- 공백 문자를 출력한다.
  1. `Editor > General > Appearance` 이동.
  2. `Show whitespaces` 의 모든 체크박스 선택.
  3. `Show line numbers` 체크박스 선택.
  4. `Shoiw indent guides` 체크박스 선택.
- 맞춤법 검사(Spell Checker)를 위한 사전 단어를 등록한다.
  1. `Dictionary` 플러그인을 설치한다.
  2. `Editor > Proofreading > Spelling` 에서 `Custom dictionaries` 항목에 `project.dic` 파일을 추가한다.
- Python code formatter, black 을 사용한다. 이를 위한 `Code Style` 변경
  1. `Settings > Editor > Code Style > Python` 에서 `Tabs and Indents` 탭의 `Continuation indent` 를 `4` 로 변경.
- 한 줄은 88 문자로 고정한다.
  1. `Editor > General > Appearance` 에서 `Show hard wrap and visual guides (configured in Code Style options)` 를 선택.
  2. `Editor > Code Style > Python` 에서 `Wrapping and Braces` 탭의 `Hard wrap at` 항목을 `88`로 수정.
- Python Interpreter 선택.
  1. `Project: recc > Python Interpreter` 이동.
  2. 자신의 파이썬 환경 선택. (Virtual environment 추천)

### PyCharm Pro setup

- Code 의 중복성 체크 제거.
  1. `Settings > Editor > Duplicates` 이동.
  2. `Python` 항목의 체크박스 해제.
- SQL 외래키(Foreign key) 사용시 참조 에러 Disable.
  1. `Settings > Editor > Inspections` 이동.
  2. `SQL > Unresolved reference` 항목의 체크박스 해제.

### core project

```sh
cd core
bash requirements.sh
python core_main.py
```

### fe project

```sh
cd fe
curl -L "https://raw.githubusercontent.com/tj/n/master/bin/n" -o n
n lts
npm install -g yarn
yarn
yarn serve
```

### Docker Compose

```
cd core
docker-compose -f docker-compose-mini.yml up -d
```

### Exclude analyzer

분석 조건에서 인라인 코드로 제외 처리 하는 방법은 다음과 같다:

#### Black

- `# fmt: off` 와 `# fmt: on` 사이의 코드. (동일한 수준의 들여 쓰기)
- 또는 [YAPF](https://github.com/google/yapf) 스타일의 코드.
- [The Black code style](https://black.readthedocs.io/en/stable/the_black_code_style.html) 페이지 참조.

#### PyCharm

- `# noinspection PyPep8` 주석 다음줄에 해당하는 구문.
- `# noqa` 주석이 포함된 한 줄. (`flake8` 와 `pycodestyle.py` 에 대응한다)
- [Disabling and enabling inspections](https://www.jetbrains.com/help/pycharm/disabling-and-enabling-inspections.html) 페이지 참조.

#### Coverage.py

- `# pragma: no cover` 주석이 포함된 한 줄.
- 또는 `# nocov` 또는 `# noqa` 주석이 포함된 한 줄.
- `tox.ini` 파일의 `[report]` 항목, `exclude_lines` 참조.
- [Excluding code from coverage.py](https://coverage.readthedocs.io/en/coverage-5.4/excluding.html) 페이지 참조.

#### Flake8

- `# noqa` 주석이 포함된 한 줄.
- 또는 `# noqa: E731,E123` 와 같이 지정할 수 있다.
- 또는 파일 상단에 `# flake8: noqa` 주석 추가.
- [Selecting and Ignoring Violations](https://flake8.pycqa.org/en/latest/user/violations.html) 페이지 참조.

#### mypy

- `mypy.ini` 파일에 모듈명 추가.
- 또는 파일 상단에 `# mypy: ignore-errors` 주석 추가.
- [Inline configuration](https://mypy.readthedocs.io/en/stable/inline_config.html) 페이지 참조.

#### PEP 484

- `# type: ignore` comment
- `@no_type_check` decorator on a class or function
- Custom class or Function decorator marked with `@no_type_check_decorator`
- [PEP 484 -- Type Hints](https://www.python.org/dev/peps/pep-0484/) 페이지 참조.

## GitLab CI Configuration

- Pipeline 에서 사용될 변수를 추가한다.
  1. 프로젝트 선택.
  2. `Project > Settings > CI/CD > Variables` 메뉴 션택.
  3. 변수 추가.

### CI Variables

- `DEVPI_URL` Devpi repository URL (e.g. `https://devpi.site.com/user/index`)
- `DEVPI_ID` Devpi repository user id.
- `DEVPI_PW` Devpi repository user password.
- `REGISTRY_HOST` Docker registry (e.g. `docker.site.com`)
- `REGISTRY_ID` Docker registry user id.
- `REGISTRY_PW` Docker registry user password.

## Terms

### Modules

- `bp` Blueprint
- `bs` Blueprint Store
- `cm` Container Manager
- `cs` Cache Store
- `db` DataBase
- `es` ElasticSearch
- `tm` Task Manager
- `ts` Template Store
- `vs` Visual Scripting

### Architecture

- `group`
- `project`
- `task`
- `fullpath` - group + project + task
- `layout`
- `widget`
- `volume`
- `network`
- `container`
- `storage`
- `session`

### Visual Scripting

- `graph`
- `task`
- `node`
- `arc`
- `slot`
- `box`
- `signal`
- `blueprint`
- `template`
- `lambda`

## License

See `LICENSE` file.
