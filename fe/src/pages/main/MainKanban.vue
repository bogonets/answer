<i18n lang="yaml">
en:
  tools:
    tables: "Tables"
    kanbans: "Kanban"
    filter: "Filter"
    sort: "Sort"
    hide: "Hide Fields"
  msg:
    empty: "Empty Tables"

ko:
  tools:
    tables: "테이블"
    kanbans: "간반"
    filter: "필터"
    sort: "정렬"
    hide: "숨김"
  msg:
    empty: "테이블이 존재하지 않습니다."
</i18n>

<template>
  <div class="kanban-main">
    <v-toolbar dense flat>
      <v-btn plain small @click="onClickTables">
        <v-icon left>
          mdi-table
        </v-icon>
        {{ $t('tools.tables') }}
      </v-btn>

      <v-btn plain small @click="onClickKanbans">
        <v-icon left>
          mdi-view-week-outline
        </v-icon>
        {{ $t('tools.kanbans') }}
      </v-btn>

      <v-btn plain small @click="onClickFilter">
        <v-icon left>
          mdi-filter
        </v-icon>
        {{ $t('tools.filter') }}
      </v-btn>

      <v-btn plain small @click="onClickSort">
        <v-icon left>
          mdi-sort
        </v-icon>
        {{ $t('tools.sort') }}
      </v-btn>

      <v-btn plain small @click="onClickHide">
        <v-icon left>
          mdi-eye-off
        </v-icon>
        {{ $t('tools.hide') }}
      </v-btn>

      <v-btn icon plain small @click="onClickMore">
        <v-icon>
          mdi-dots-horizontal
        </v-icon>
      </v-btn>
    </v-toolbar>
    <v-divider></v-divider>

    <view-port>
      <div ref="kanban-board" class="kanban-board">
        <v-responsive
            class="kanban-board--responsive"
            content-class="kanban-board--responsive-content"
        >
          <div
              v-for="task in tasks"
              :key="`task-${task.id}`"
              class="kanban-task"
          >
            <div class="kanban-task--header">
              <v-icon small class="mx-1">mdi-chevron-right</v-icon>
              <span class="text-subtitle-1 text--secondary font-weight-bold">
                {{ task.name }}
              </span>
              <v-spacer></v-spacer>
              <v-btn small icon>
                <v-icon small>mdi-plus</v-icon>
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
                >
                  <v-card-text>{{ card.name }}</v-card-text>
                  <v-card-subtitle>Subtitle</v-card-subtitle>

                  <v-card-text>
                    Author:
                    <v-chip small color="primary">
                      <v-icon size="24" left>mdi-account-circle</v-icon>
                      John Leider
                    </v-chip>
                  </v-card-text>
                  <v-card-actions>

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
  }
})
export default class MainKanban extends VueBase {
  @Ref('kanban-board')
  kanbanBoard!: HTMLDivElement;

  @Ref('kanban-task--responsive')
  kanbanTaskResponsive!: Array<VResponsive>;

  loading = false;

  dragula!: Drake;
  tasks = [
    {
      id: 0,
      name: "first",
      cards: [
        {
          id: 0,
          name: "card0",
          loading: false,
        },
        {
          id: 1,
          name: "card1",
          loading: true,
        },
        {
          id: 4,
          name: "card4",
          loading: true,
        },
        {
          id: 5,
          name: "card5",
          loading: false,
        },
        {
          id: 6,
          name: "card6",
          loading: false,
        },
        {
          id: 7,
          name: "card7",
          loading: false,
        },
      ],
    },
    {
      id: 1,
      name: "second",
      cards: [
        {
          id: 2,
          name: "card2",
          loading: false,
        },
        {
          id: 3,
          name: "card3",
          loading: false,
        },
      ],
    },
    {
      id: 2,
      name: "third",
      cards: [
        {
          id: 8,
          name: "card8",
          loading: false,
        },
      ],
    },
  ];

  mounted() {
    console.dir(this.kanbanTaskResponsive);
    const el = this.kanbanTaskResponsive[0].$el;
    const c = el.getElementsByClassName('kanban-task--responsive-content');
    console.dir(c[0]);
    // this.dragula = createDragula([this.bar1, this.bar2], {
    //   mirrorContainer: this.kanbanBoard,
    // });

    this.dragula = createDragula({
      mirrorContainer: this.kanbanBoard,
    });
    this.kanbanTaskResponsive.map(t => {
      const c = t.$el.getElementsByClassName('kanban-task--responsive-content')[0];
      this.dragula.containers.push(c);
    })
  }

  onClickTables() {
  }

  onClickKanbans() {
  }

  onClickFilter() {
  }

  onClickSort() {
  }

  onClickHide() {
  }

  onClickMore() {
  }
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
