<details>
<summary>Example code</summary>
<div>

```html
<template>
  <div style="width: 100%; height: 100%;">
    <a-console ref="console" @close="$emit('close')"></a-console>
  </div>
</template>
```
```html
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
    }
  },
  computed:{

  },
  methods:{
    addConsole: function (text) {
      if (this.$refs.console) {
        this.$refs.console.addConsole(`${text}`);
      }
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
```

</div>
</details>
