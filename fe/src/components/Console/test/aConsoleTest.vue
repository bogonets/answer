<template>
  <div style="width: 100%; height: 100%;">
    <!-- TEST code -->
    <!-- <a-console ref="console" @fileLoad="fileLoad" @close="$emit('close')"></a-console> -->
    <a-console ref="console" @close="$emit('close')"></a-console>
  </div>
</template>

<script>
import aConsole from "@/components/Console/aConsole.vue";
export default {
  props:{

  },
  components:{
    aConsole
  },
  data(){
    return {
      repeat: null,
      inputText: ''
    }
  },
  computed:{

  },
  methods:{
    addConsole: function (text) {
      if (this.$refs.console) {
        this.$refs.console.addConsole(`${text}`);
      }
    },

    // TEST.
    fileLoad: function () {
      var a = document.createElement("input");
      a.setAttribute("type", "file");
      a.click();
      var self = this;
      a.addEventListener("change", evt => {
        var file = evt.target.files[0];
        var reader = new FileReader();
        reader.onload = function() {
          self.inputText = reader.result;
          self.repeat = setInterval(() => {
            self.addConsole(self.inputText);
          }, 200);
        };
        reader.readAsText(file);
      });
    }
  },
  created(){
  },
  mounted(){
  },
  beforeDestroy(){
    if (this.repeat) {
      clearInterval(this.repeat);
      this.repeat = null;
    }
  }
}
</script>

<style scoped>

</style>
