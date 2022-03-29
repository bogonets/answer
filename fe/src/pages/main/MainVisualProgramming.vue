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
        x2: 150,
        y2: 140,
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
            value: 'Click Me!',
            mime: 'vp/button',
          },
        ],
      },
      ml0: {
        type: 'function',
        template: 'ml',
        x1: 200,
        y1: 240,
        x2: 300,
        y2: 340,
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
            name: 'dataset',
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
      2: {
        type: 'export',
        template: 'send_mail',
        x1: 250,
        y1: 360,
        x2: 350,
        y2: 460,
        props: [],
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
      }
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
