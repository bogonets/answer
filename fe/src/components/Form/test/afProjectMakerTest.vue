<template>
  <div style="width: 100%; height: 100%;">
    <v-btn text small @click="dialog = !dialog">open</v-btn>
    <v-dialog
    v-model="dialog"
    width="500" height="500" scrollable persistent>
      <af-project-maker @close="dialog = false" :useSelection="true"></af-project-maker>
    </v-dialog>
  </div>
</template>

<script>
import afProjectMaker from "@/components/Form/afProjectMaker.vue";
export default {
  props:{

  },
  components:{
    afProjectMaker
  },
  data(){
    return {
      dialog: false
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

</style>
