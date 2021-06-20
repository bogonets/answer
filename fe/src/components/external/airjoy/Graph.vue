<script lang="ts">
import { Component, Prop, Mixins } from "vue-property-decorator";
import Chart from "chart.js";
import VueChart from "vue-chartjs";
import "chartjs-plugin-colorschemes";

/**
 * Time serese chart
 */
@Component
export default class Graph extends Mixins(
  VueChart.Line,
  VueChart.mixins.reactiveProp
) {
  /**
   * Chart data
   */
  @Prop({ required: true, default: {} })
  public chartData!: Chart.ChartData;

  /**
   * Chart options(If override default options)
   */
  @Prop()
  public chartOptions!: Chart.ChartOptions;

  /**
   * Chart options
   */
  // private options: Chart.ChartOptions = {};
  @Prop()
  public options!: Chart.ChartOptions;

  /**
   * Chart instance
   */
  private chart!: Chart;

  /**
   * initialize
   */
  mounted() {
    // Draw chart
    this.renderChart(this.chartData, this.options);
    this.chart = this.$data._chart;
  }

  update() {
    this.renderChart(this.chartData, this.options);
  }
}
</script>

<style scoped lang="scss"></style>
