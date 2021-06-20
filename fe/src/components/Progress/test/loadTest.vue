<template>
  <div style="width: 100%; height: 100%;">
    <v-loader :loadList="list" :serialize="true" @allComplete="allSuccess"></v-loader>
  </div>
</template>
<script>
import vLoader from "@/components/Progress/processProgress.vue";
export default {
  props:{

  },
  components:{
    vLoader
  },
  data(){
    return {
      list: [
        { 
          name: "Check initialized API.",
          func: () => { 
            return new Promise((resolve, reject) => {
              setTimeout(() => {
                for (var i = 0; i < 9000; ++i) {
                  resolve(true);
                }
              }, 5000)
              })
          },
          complete: false,
          onError: (e) => { console.log("ERROREEROROROR", e); }
        },
        { 
          name: "Check Existed Admin.",
          func: () => { 
            return new Promise((resolve, reject) => 
              setTimeout(() => {
                for (var i = 0; i < 9000; ++i) {
                  resolve(true);
                }
              }, 7000)
            )
          },
          complete: false,
          onError: () => {
            alert("Is not existed Admin. Go to create admin page.");
            this.$router.push("/craeteadmin");
          }
        }
      ]
    }
  },
  computed:{

  },
  methods:{
    allSuccess: function (complete) {
      console.log("ALL COMPLETE !!!! ", complete);
    }
  },
  created(){
  },
  mounted(){

  }
}
</script>
<style scoped lang="">

</style>