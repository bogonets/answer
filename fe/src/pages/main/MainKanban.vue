<i18n lang="yaml">
en:
  tools:
    tables: 'Tables'
    kanbans: 'Kanban'
    filter: 'Filter'
    sort: 'Sort'
    hide: 'Hide Fields'
  msg:
    empty: 'Empty Tables'

ko:
  tools:
    tables: '테이블'
    kanbans: '간반'
    filter: '필터'
    sort: '정렬'
    hide: '숨김'
  msg:
    empty: '테이블이 존재하지 않습니다.'
</i18n>

<template>
  <div class="kanban-main">
    <v-toolbar dense flat>
      <v-btn plain small @click="onClickTables">
        <v-icon left>mdi-table</v-icon>
        {{ $t('tools.tables') }}
      </v-btn>

      <v-btn plain small @click="onClickKanbans">
        <v-icon left>mdi-view-week-outline</v-icon>
        {{ $t('tools.kanbans') }}
      </v-btn>

      <v-btn plain small @click="onClickFilter">
        <v-icon left>mdi-filter</v-icon>
        {{ $t('tools.filter') }}
      </v-btn>

      <v-btn plain small @click="onClickSort">
        <v-icon left>mdi-sort</v-icon>
        {{ $t('tools.sort') }}
      </v-btn>

      <v-btn plain small @click="onClickHide">
        <v-icon left>mdi-eye-off</v-icon>
        {{ $t('tools.hide') }}
      </v-btn>

      <v-btn icon plain small @click="onClickMore">
        <v-icon>mdi-dots-horizontal</v-icon>
      </v-btn>
    </v-toolbar>
    <v-divider></v-divider>

    <view-port>
      <div ref="kanban-board" class="kanban-board">
        <v-responsive
          class="kanban-board--responsive"
          content-class="kanban-board--responsive-content"
        >
          <div v-for="task in tasks" :key="`task-${task.id}`" class="kanban-task">
            <div class="kanban-task--header">
              <v-icon small class="mx-1">mdi-chevron-right</v-icon>
              <span class="text-subtitle-1 text--secondary font-weight-bold">
                {{ task.name }}
              </span>
              <v-spacer></v-spacer>
              <v-btn small icon>
                <v-icon small>mdi-plus</v-icon>
              </v-btn>
              <v-btn small icon>
                <v-icon small>mdi-cog</v-icon>
              </v-btn>
            </div>
            <v-divider></v-divider>

            <div class="kanban-task--body">
              <v-responsive
                ref="kanban-task--responsive"
                class="kanban-task--responsive"
                content-class="kanban-task--responsive-content"
              >
                <v-card
                  v-for="card in task.cards"
                  :key="`task-${task.id}-card-${card.id}`"
                  class="kanban-card"
                  outlined
                  :loading="card.loading"
                  :disabled="card.disabled"
                >
                  <v-card-title v-if="card.title">
                    {{ card.title }}
                  </v-card-title>
                  <v-card-subtitle v-if="card.subtitle">
                    {{ card.subtitle }}
                  </v-card-subtitle>

                  <v-card-text>
                    <div
                      v-for="(propType, propTypeIndex) in cardPropTypes"
                      :key="`task-${task.id}-card-${card.id}-prop-${propTypeIndex}`"
                    >
                      <div v-if="propType.key in card.props" class="flex flex-row">
                        <v-icon small>{{ getPropertyTypeIcon(propType.type) }}</v-icon>
                        <span class="ml-1 text-overline">{{ propType.key }}</span>
                      </div>

                      <div v-if="propType.type === 'array:account'">
                        <v-chip
                          v-for="account in card.props[propType.key]"
                          :key="`task-${task.id}-card-${card.id}-prop-${propTypeIndex}-${account}`"
                          small
                          class="mr-1"
                        >
                          <v-icon size="24" left>mdi-account-circle</v-icon>
                          {{ account }}
                        </v-chip>
                      </div>
                      <div v-else-if="propType.type === 'array:category'">
                        <v-chip
                          v-for="category in card.props[propType.key]"
                          :key="`task-${task.id}-card-${card.id}-prop-${propTypeIndex}-${category}`"
                          small
                          class="mr-1"
                          :color="propType.format[category].color"
                        >
                          {{ propType.format[category].name }}
                        </v-chip>
                      </div>
                      <div v-else-if="propType.type === 'text'">
                        <span class="ml-1 text-body-2 text--secondary font-weight-bold">
                          {{ card.props[propType.key] }}
                        </span>
                      </div>
                      <div v-else-if="['link', 'directory'].includes(propType.type)">
                        <a class="ml-1 text-decoration-underline font-weight-medium">
                          {{ card.props[propType.key] }}
                        </a>
                      </div>
                    </div>
                  </v-card-text>

                  <v-card-actions>
                    <v-chip small>
                      <v-icon size="24" left>mdi-account-circle</v-icon>
                      {{ card.author }}
                    </v-chip>
                    <v-spacer></v-spacer>

                    <v-btn text small rounded color="secondary">
                      <v-icon small class="mr-1">mdi-comment-text-outline</v-icon>
                      {{ card.comments }}
                    </v-btn>
                    <v-btn icon small color="secondary">
                      <v-icon size="18">mdi-open-in-app</v-icon>
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-responsive>
            </div>

            <div class="kanban-task--footer">
              <!-- EMPTY -->
            </div>
          </div>
        </v-responsive>
      </div>
    </view-port>
  </div>
</template>

<script lang="ts">
import {Component, Ref} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ViewPort from '@/components/ViewPort.vue';
import {VResponsive} from 'vuetify/lib/components/VResponsive';
import createDragula, {Drake} from 'dragula';

@Component({
  components: {
    ViewPort,
  },
})
export default class MainKanban extends VueBase {
  @Ref('kanban-board')
  kanbanBoard!: HTMLDivElement;

  @Ref('kanban-task--responsive')
  kanbanTaskResponsive!: Array<VResponsive>;

  loading = false;

  dragula!: Drake;
  cardPropTypes = [
    {
      key: 'title',
      type: 'title',
    },
    {
      key: 'content',
      type: 'subtitle',
    },
    {
      key: 'workers',
      type: 'array:account',
    },
    {
      key: 'tags',
      type: 'array:category',
      format: [
        {
          name: 'A부품 라인',
          color: 'green',
        },
        {
          name: '최우선',
          color: 'deep-orange',
        },
        {
          name: 'B부품 라인',
          color: 'purple',
        },
        {
          name: '신규',
          color: 'yellow',
        },
      ],
    },
    {
      key: 'directory',
      type: 'directory',
    },
  ];

  tasks = [
    {
      id: 0,
      name: '데이터 취득',
      cards: [
        {
          id: 0,
          loading: false,
          comments: 10,
          author: '존시나',
          title: '2022/1분기 모델 훈련',
          subtitle: '1,2월 데이터 총 100건',
          disabled: false,
          props: {
            workers: ['피카츄', '라이츄'],
            tags: [0, 1],
            directory: '/work/2022-03-31',
          },
        },
      ],
    },
    {
      id: 1,
      name: '라벨링',
      cards: [
        {
          id: 2,
          loading: false,
          comments: 999,
          author: '헐크 호건',
          title: '2021/4분기 모델 훈련',
          subtitle: 'Fake 데이터 10건 포함',
          disabled: false,
          props: {
            workers: ['파이리'],
            tags: [2],
            directory: '/work/2021-12-30',
          },
        },
        {
          id: 3,
          loading: true,
          comments: 0,
          author: 'The Rock',
          title: '긴급 데이터 훈련',
          subtitle: '새로운 부품 추가로 인한 새로운 클래스 추가',
          disabled: false,
          props: {
            workers: ['꼬북이', '또도가스', '잉어킹', '이상해씨'],
            tags: [2, 3, 1],
            directory: '/work/2021-06-12-hotfix',
          },
        },
      ],
    },
    {
      id: 2,
      name: '모델 학습',
      cards: [
        {
          id: 8,
          loading: true,
          comments: 0,
          author: '핫산',
          title: '2021/3분기 모델 훈련',
          subtitle: '오늘의 포켓몬은 뭘까요',
          disabled: false,
          props: {
            workers: ['피죤투'],
            tags: [0],
            directory: '/work/2021-08-02',
          },
        },
      ],
    },
    {
      id: 3,
      name: '완료',
      cards: [
        {
          id: 8,
          loading: false,
          comments: 1,
          author: '볼드모트',
          title: '2021/신규 모델 추가',
          subtitle: '런어웨이가즈아',
          disabled: true,
          props: {
            workers: ['장작의왕', '빛바랜자', '야수'],
            tags: [3],
            directory: '/new/model2',
          },
        },
      ],
    },
  ];

  mounted() {
    this.dragula = createDragula({
      mirrorContainer: this.kanbanBoard,
    });
    this.kanbanTaskResponsive.map(t => {
      const c = t.$el.getElementsByClassName('kanban-task--responsive-content')[0];
      this.dragula.containers.push(c);
    });
  }

  getPropertyTypeIcon(typeName: string) {
    switch (typeName) {
      case 'title':
        return 'mdi-format-title';
      case 'subtitle':
        return 'mdi-format-text';
      case 'text':
        return 'mdi-format-text';
      case 'link':
        return 'mdi-link-variant';
      case 'directory':
        return 'mdi-folder';
      case 'array:text':
        return 'mdi-format-text';
      case 'array:account':
        return 'mdi-account';
      case 'array:category':
        return 'mdi-tag';
      default:
        return '';
    }
  }

  onClickTables() {}

  onClickKanbans() {}

  onClickFilter() {}

  onClickSort() {}

  onClickHide() {}

  onClickMore() {}
}
</script>

<style lang="scss" scoped>
@import '~vuetify/src/styles/styles.sass';
@import '~dragula/dist/dragula.css';

$color-grey: map-get($colors, 'grey');
$color-grey-base: map-get($color-grey, 'base');
$color-grey-lighten-5: map-get($color-grey, 'lighten-5');
$color-grey-lighten-4: map-get($color-grey, 'lighten-4');
$color-grey-lighten-3: map-get($color-grey, 'lighten-3');
$color-grey-lighten-2: map-get($color-grey, 'lighten-2');
$color-grey-lighten-1: map-get($color-grey, 'lighten-1');
$color-grey-darken-1: map-get($color-grey, 'darken-1');
$color-grey-darken-2: map-get($color-grey, 'darken-2');
$color-grey-darken-3: map-get($color-grey, 'darken-3');
$color-grey-darken-4: map-get($color-grey, 'darken-4');

$color-black: map-get($shades, 'black');
$color-white: map-get($shades, 'white');

$gap-size: 8px;

.theme--light.v-application {
  .kanban-board {
    background: $color-grey-lighten-2;
    color: map-deep-get($material-light, 'text', 'secondary');

    .kanban-task {
      background: $color-grey-lighten-3;
    }

    .kanban-card {
      background: $color-grey-lighten-5;
    }
  }
}

.theme--dark.v-application {
  .kanban-board {
    background: $color-grey-darken-4;
    color: map-deep-get($material-dark, 'text', 'secondary');

    .kanban-task {
      background: $color-grey-darken-3;
    }

    .kanban-card {
      background: $color-grey-darken-3;
    }
  }
}

@mixin fill-size {
  width: 100%;
  height: 100%;
}

@mixin fill-height {
  height: 100%;
}

.kanban-main {
  .kanban-board {
    @include fill-size;

    .kanban-board--responsive {
      @include fill-size;

      overflow-x: auto;
      overflow-y: hidden;

      ::v-deep.kanban-board--responsive-content {
        @include fill-size;

        padding: $gap-size 0 $gap-size $gap-size;

        display: flex;
        flex-direction: row;
        flex-wrap: nowrap;
      }
    }

    // When dragging and dropping, the position of the DOM may be moved.
    .kanban-task {
      @include fill-height;

      margin-right: $gap-size;

      min-width: 320px;
      max-width: 320px;
      min-height: 100px;

      display: flex;
      flex-direction: column;
      flex-wrap: nowrap;

      .kanban-task--header {
        padding: 4px;

        display: flex;
        flex-direction: row;
        flex-wrap: nowrap;

        align-items: center;
      }

      .kanban-task--body {
        flex-grow: 1;

        overflow-x: hidden;
        overflow-y: auto;

        display: flex;
        flex-direction: column;
        flex-wrap: nowrap;

        .kanban-task--responsive {
          // [Important]
          // Do not add the `height: 100%;` style.
          // Affects the size calculation of <v-responsive>

          // An empty space is required to drag and drop onto an empty space.
          // Use `flex-grow: 1` instead of `height: 100%;` style.
          flex-grow: 1;

          ::v-deep.kanban-task--responsive-content {
            @include fill-height;

            display: flex;
            flex-direction: column;
            flex-wrap: nowrap;

            padding: $gap-size;
          }
        }
      }

      .kanban-task--footer {
        bottom: 0;
      }
    }

    // When dragging and dropping, the position of the DOM may be moved.
    .kanban-card {
      margin-bottom: $gap-size;

      //border: 1px solid green;
    }
  }
}
</style>
