<template>
  <div class="storage-main">
		<div class="dashboard-zone">
      <storage></storage>
		</div>
	</div>
</template>

<script>
import Storage from "@/components/Storage/aStorageManager.vue";
export default {
  props:{

  },
  components:{
    Storage
  },
  data(){
    return {

    }
  },
  computed:{

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
.storage-main {
	height: 100% !important;
	/* padding: 25px 25px 25px 25px !important; */
	padding: 10px 10px 10px 10px !important;
	/* border: 1px solid royalblue !important; */
}
.dashboard-zone {
	height: 100% !important;
	/* border: 1px solid yellow !important; */
}
</style>
