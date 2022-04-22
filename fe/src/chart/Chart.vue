<template>
  <div>
    <canvas ref="canvas" :width="width" :height="height"></canvas>
  </div>
</template>

<script lang="ts">
import {Vue, Component, Prop, Ref, Watch, Emit} from 'vue-property-decorator';
import type {
  ChartType,
  ChartData,
  ChartOptions,
  ChartConfiguration,
  Plugin,
} from 'chart.js';
import {Chart as ChartJS} from 'chart.js';

const DEFAULT_TYPE = 'line';
const DEFAULT_WIDTH = 480;
const DEFAULT_HEIGHT = 480;

@Component
export default class Chart extends Vue {
  @Prop({type: String, default: DEFAULT_TYPE})
  readonly type!: ChartType;

  @Prop({type: Number, default: DEFAULT_WIDTH})
  readonly width!: number;

  @Prop({type: Number, default: DEFAULT_HEIGHT})
  readonly height!: number;

  @Prop({type: Array, default: () => []})
  readonly plugins!: Array<Plugin>;

  @Prop({
    type: Object,
    default: () => {
      return {};
    },
  })
  readonly chartData!: ChartData;

  @Prop({
    type: Object,
    default: () => {
      return {};
    },
  })
  readonly options!: ChartOptions;

  @Ref()
  readonly canvas!: HTMLCanvasElement;

  chart?: ChartJS;

  beforeDestroy() {
    if (this.chart) {
      this.chart.destroy();
    }
  }

  renderChart() {
    if (this.chart) {
      this.chart.destroy();
    }

    const context = this.canvas.getContext('2d');
    if (context === null) {
      throw Error('Canvas context is null');
    }

    const config = {
      type: this.type,
      data: this.chartData,
      options: this.options,
      plugins: this.plugins,
    } as ChartConfiguration;
    this.chart = new ChartJS(context, config);
  }

  @Watch('options.plugins.streaming.pause')
  onChangeOptionsPluginsStreamingPause() {
    if (this.chart) {
      this.chart.update();
    }
  }

  @Watch('chartData')
  onChangeChartData(newData, oldData) {
    if (oldData && typeof this.chart !== 'undefined') {
      const chart = this.chart;

      const newDatasetLabels = newData.datasets.map(d => d.label);
      const oldDatasetLabels = oldData.datasets.map(d => d.label);

      const oldLabels = JSON.stringify(oldDatasetLabels);
      const newLabels = JSON.stringify(newDatasetLabels);

      // Check if Labels are equal and if dataset length is equal
      if (
        newLabels === oldLabels &&
        oldData.datasets.length === newData.datasets.length
      ) {
        newData.datasets.forEach((dataset, i) => {
          // Get new and old dataset keys
          const oldDatasetKeys = Object.keys(oldData.datasets[i]);
          const newDatasetKeys = Object.keys(dataset);

          // Get keys that aren't present in the new data
          const deletionKeys = oldDatasetKeys.filter(key => {
            return key !== '_meta' && newDatasetKeys.indexOf(key) === -1;
          });

          // Remove outdated key-value pairs
          deletionKeys.forEach(deletionKey => {
            delete chart.data.datasets[i][deletionKey];
          });

          // Update attributes individually to avoid re-rendering the entire chart
          for (const attribute in dataset) {
            if (typeof dataset[attribute] !== 'undefined') {
              chart.data.datasets[i][attribute] = dataset[attribute];
            }
          }
        });

        if (typeof newData['labels'] !== 'undefined') {
          chart.data.labels = newData.labels;
          this.labelsUpdate();
        }
        if (typeof newData['xLabels'] !== 'undefined') {
          chart.data['xLabels'] = newData.xLabels;
          this.xlabelsUpdate();
        }
        if (typeof newData['yLabels'] !== 'undefined') {
          chart.data['yLabels'] = newData.yLabels;
          this.ylabelsUpdate();
        }
        chart.update();
        this.chartUpdate();
      } else {
        if (chart) {
          chart.destroy();
          this.chartDestroy();
        }
        this.renderChart();
        this.chartRender();
      }
    } else {
      if (this.chart) {
        this.chart.destroy();
        this.chartDestroy();
      }

      this.renderChart();
      this.chartRender();
    }
  }

  @Emit('labels:update')
  labelsUpdate() {}

  @Emit('xlabels:update')
  xlabelsUpdate() {}

  @Emit('ylabels:update')
  ylabelsUpdate() {}

  @Emit('chart:update')
  chartUpdate() {}

  @Emit('chart:destroy')
  chartDestroy() {}

  @Emit('chart:render')
  chartRender() {}
}
</script>
