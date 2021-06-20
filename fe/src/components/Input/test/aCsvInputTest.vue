<template>
  <div style="width: 100%; height: 100%; border: 1px solid cyan; padding: 15px;">
    <a-csv-input
    v-model="csv"
    dense
    shaped
    outlined
    @returnArray="onGetReturnArray($event)">
    </a-csv-input>
    {{ csv }}<br/>
    {{ array }}
  </div>
</template>

<script>
// import aCsvInput from "@/components/Input/aCsvInput.vue";
  export default {
    name: "aCsvInputTest",
    components: {
      // aCsvInput
    },
    data () {
      return {
        csv: "0.5,0.4, 0.1, 0.1",
        array: [],
      }
    },
    methods: {
      onGetReturnArray: function (array) {
        this.array = array;
      }
    }
  }
</script>

<style scoped>

</style>
