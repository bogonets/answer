<i18n lang="yaml">
en:
  tools:
    tree: "Tree"
    add: "Add Lambda"
    properties: "Properties"
    console: "Console"

ko:
  tools:
    tree: "계층 구조"
    add: "람다 추가"
    properties: "속성"
    console: "콘솔"
</i18n>

<template>
  <div class="vp-main">
    <v-toolbar dense flat>
      <v-btn plain small @click="onClickTree">
        <v-icon left>
          mdi-file-tree
        </v-icon>
        {{ $t('tools.tree') }}
      </v-btn>

      <v-btn plain small @click="onClickAddLambda">
        <v-icon left>
          mdi-lambda
        </v-icon>
        {{ $t('tools.add') }}
      </v-btn>

      <v-btn plain small @click="onClickProperties">
        <v-icon left>
          mdi-ballot-outline
        </v-icon>
        {{ $t('tools.properties') }}
      </v-btn>

      <v-btn plain small @click="onClickConsole">
        <v-icon left>
          mdi-console
        </v-icon>
        {{ $t('tools.console') }}
      </v-btn>

      <v-btn icon plain small @click="onClickMore">
        <v-icon>
          mdi-dots-horizontal
        </v-icon>
      </v-btn>
    </v-toolbar>
    <v-divider></v-divider>

    <view-port>
      <canvas
          ref="vp-canvas"
          class="vp-canvas"
          @contextmenu="onContextMenu"
      ></canvas>
    </view-port>
  </div>
</template>

<script lang="ts">
import {Component, Ref} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ViewPort from '@/components/ViewPort.vue';
import {Context, GraphOptions, Graph} from '@/vp/context';

@Component({
  components: {
    ViewPort,
  }
})
export default class MainVisualProgramming extends VueBase {
  @Ref('vp-canvas')
  vpCanvas!: HTMLCanvasElement;

  context!: Context;

  graph = {
    lambdas: {
      button0: {
        type: 'signal',
        template: 'button',
        x1: 50,
        y1: 40,
        x2: 180,
        y2: 115,
        props: [
          {
            type: 'flow_output',
            name: 'out',
            value: '',
            mime: '',
          },
          {
            type: 'button',
            name: 'btn',
            value: 'Start Training!',
            mime: 'vp/button',
          },
        ],
      },
      ml0: {
        type: 'function',
        template: 'ml',
        x1: 250,
        y1: 150,
        x2: 420,
        y2: 280,
        props: [
          {
            type: 'flow_input',
            name: 'in',
            value: '',
            mime: '',
          },
          {
            type: 'flow_output',
            name: 'out',
            value: '',
            mime: '',
          },
          {
            type: 'data_input',
            name: 'training_set',
            value: '',
            mime: '',
          },
          {
            type: 'data_input',
            name: 'validation_set',
            value: '',
            mime: '',
          },
          {
            type: 'data_output',
            name: 'model',
            value: '',
            mime: '',
          },
          {
            type: 'button',
            name: 'stop',
            value: 'Interrupt',
            mime: '',
          },
        ],
      },
      files0: {
        type: 'data',
        template: 'files',
        x1: 80,
        y1: 160,
        x2: 180,
        y2: 235,
        props: [
          {
            type: 'text_input',
            name: 'path',
            value: '',
            mime: '',
          },
          {
            type: 'data_output',
            name: 'files',
            value: '',
            mime: '',
          },
        ],
      },
      files1: {
        type: 'data',
        template: 'files',
        x1: 80,
        y1: 260,
        x2: 180,
        y2: 335,
        props: [
          {
            type: 'text_input',
            name: 'path',
            value: '',
            mime: '',
          },
          {
            type: 'data_output',
            name: 'files',
            value: '',
            mime: '',
          },
        ],
      },
      sendmail2: {
        type: 'export',
        template: 'sendmail',
        x1: 550,
        y1: 260,
        x2: 660,
        y2: 410,
        props: [
          {
            type: 'flow_input',
            name: 'in',
            value: '',
            mime: '',
          },
          {
            type: 'data_input',
            name: 'title',
            value: '',
            mime: '',
          },
          {
            type: 'data_input',
            name: 'mail',
            value: '',
            mime: '',
          },
          {
            type: 'data_input',
            name: 'content',
            value: '',
            mime: '',
          },
          {
            type: 'data_input',
            name: 'attach',
            value: '',
            mime: '',
          },
        ],
      },
    },
    templates: {},
    arcs: [
      {
        from: {
          lambda: 'button0',
          prop: 'out',
        },
        to: {
          lambda: 'ml0',
          prop: 'in',
        },
      },
      {
        from: {
          lambda: 'ml0',
          prop: 'out',
        },
        to: {
          lambda: 'sendmail2',
          prop: 'in',
        },
      },
      {
        from: {
          lambda: 'files0',
          prop: 'files',
        },
        to: {
          lambda: 'ml0',
          prop: 'training_set',
        },
      },
      {
        from: {
          lambda: 'files1',
          prop: 'files',
        },
        to: {
          lambda: 'ml0',
          prop: 'validation_set',
        },
      },
    ],
  } as Graph;

  mounted() {
    const options = {
      view: this.vpCanvas,
    } as GraphOptions;
    this.context = new Context(this.graph, options);
  }

  beforeDestroy() {
    this.context.close();
  }

  onContextMenu(event: PointerEvent) {
    event.preventDefault();
    this.context.openContextMenu();
  }

  onClickTree() {
  }

  onClickAddLambda() {
  }

  onClickProperties() {
  }

  onClickMore() {
  }

  onClickConsole() {
  }
}
</script>

<style lang="scss" scoped>
.vp-canvas {
  //width: 100%;
  //height: 100%;
}
</style>
