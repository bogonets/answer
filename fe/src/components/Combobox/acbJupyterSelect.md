<details>
<summary>Example code</summary>
<div>

```html
<template> <!-- template part -->
  <div>
    <acb-jupyter-select
      :label="label"
      :dense="dense"
      :outline="outline"
      :solo="solo"
      :box="box"
      v-model="item"
      ></acb-jupyter-select>
  </div>
</template>
```
```html
<script>
// script part.
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
      label: "label",
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
      // check change data.
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
```

</div>
</details>
