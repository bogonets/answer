# 프로젝트

프로젝트는 작업 공간의 최소 단위 입니다.

```{warning}
하단의 기능들은 현재 구현중 입니다.
```

## 프로젝트 목록

프로젝트 목록은 소속된 전체 프로젝트 목록을 볼 수 있으며,
필요하다면 `새로운 프로젝트` 버튼을 클릭하여 새로운 프로젝트를 생성할 수 있습니다.

![projects.png](./images/projects.png)

하나의 프로젝트를 선택하면 프로젝트의 대시보드 페이지로 이동합니다.

## 대시보드

프로젝트를 선택하면 가장 처음 확인 가능한 페이지 입니다. 프로젝트가 사용중인 리소스를 정량적으로 확인할 수 있습니다.

![projects-dashboard](./images/projects-dashboard.png)

## 간반보드

스케줄링을 위한 간반보드 페이지 입니다. 작업(Task)을 카드(Card)로 나타내고,
드래그-앤-드롭을 사용하여 진행 상태를 갱신할 수 있습니다.

![projects-kanban](./images/projects-kanban.png)

이 기능은 `테이블`로 정의한 내용을 기반으로 작동합니다.

## 레이아웃

`시각 프로그래밍`에 배치한 여러 람다를 시각화 하여, 하나의 어플리케이션으로 구성할 수 있습니다.

![projects-layout](./images/projects-layout.png)

### 입력 위젯

- 버튼 이벤트 : 버튼을 클릭하면 연결된 람다가 실행됩니다.
- 스위치 : 연결된 람다의 플래그를 수정할 수 있습니다.
- 웹캠 녹화 : [WebRTC](https://webrtc.org/)를 사용한 실시간 영상 또는 음성을 람다로 주입할 수 있습니다.

### 출력 위젯

- 비디오 재생 : 연결된 람다의 결과가 영상일 경우 그것을 재생합니다.
- 음악 재생 : 연결된 람다의 결과가 음성일 경우 그것을 재생합니다.
- 라이브 테이블 : 연결된 람다의 결과가 매트릭스(Matrix)일 경우 그것을 출력합니다.

### 기타 위젯

- 주피터 : [Jupyter Notebook](https://jupyter.org/)을 사용한 Python 람다를 편집할 수 있습니다.
- 외부 사이트 : 외부 사이트를 IFrame 으로 임베딩할 수 있습니다.

## 파일

프로젝트에서 사용 가능한 클라우드 저장소 입니다.

![projects-files](./images/projects-files.png)

필요하다면 `시각 프로그래밍`의 원시 데이터로 사용하거나 `시각 프로그래밍`의 결과로 저장할 수 있습니다.

## 테이블

시각화된 데이터베이스를 이용여 통계정보 및 구조화된 정보를 생성/읽기/업데이트/제거 할 수 있습니다.

![projects-tables](./images/projects-tables.png)

필요하다면 `시각 프로그래밍`의 원시 데이터로 사용하거나 `시각 프로그래밍`의 결과로 저장할 수 있습니다.

## 태스크

`시각 프로그래밍` 또는 백그라운드에서 작동중인 작업(Task)을 관리할 수 있습니다.

![projects-tasks](./images/projects-tasks.png)

## 시각 프로그래밍

시각적 구성요소인 람다(Lambda)를 활용하여 로직을 구성하고 실행할 수 있습니다.

![projects-vp](./images/projects-vp.png)

## 회원 관리

현재 프로젝트에 가입된 멤버와 각 멤버의 권한을 확인할 수 있습니다.

![projects-members](./images/projects-members.png)

## 프로젝트 설정

프로젝트의 기본 속성을 확인하거나 수정할 수 있습니다.

![projects-settings](./images/projects-settings.png)
