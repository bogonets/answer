<template>
  <div>
    <canvas ref="defaultCanvas" resize></canvas>
  </div>
</template>

<script>
import { Vue, Component, Prop } from "vue-property-decorator";
import Paper from "paper";

/**
 * It helps to draw on the canvas.
 *
 * @author zer0 <osom8979@gmail.com>
 */
@Component
export default class WhiteBoard extends Vue {
  paper = new Paper.PaperScope();

  mounted() {
    this.paper.setup(this.$refs.defaultCanvas);

    var path = new Paper.Path({
      strokeColor: "#00FF00",
      strokeJoin: "round",
      strokeWidth: 1.5
    });
    path.strokeColor = "red";
    var start = new Paper.Point(100, 100);
    path.moveTo(start);
    path.lineTo(start.add([200, -50]));

    this.paper.view.draw();
  }
}
</script>

<style scoped>
canvas {
  height: 100vh;
  width: 100%;
  background: #ffffff;
}
</style>
