<template>
  <div style="width: 100%; height: 100%;">
    <acb-jupyter-select
    :dense="dense"
    :outline="outline"
    :solo="solo"
    :box="box"
    v-model="item"
    ></acb-jupyter-select>
  </div>
</template>
<script>
import acbJupyterSelect from "@/components/Combobox/acbJupyterSelect";
export default {
  name: "acbJupyterSelectTest",
  props:{

  },
  components:{
    acbJupyterSelect
  },
  data(){
    return {
      dense: true,
      outline: true,
      solo: false,
      box: false,
      item: null
    }
  },
  computed:{

  },
  watch: {
    item() {
      this.$debug(this.$options.name, "watch::item", "Item Change:", this.item);
    }
  },
  methods:{

  },
  created(){

  },
  mounted(){

  }
}
</script>
<style scoped>

</style>