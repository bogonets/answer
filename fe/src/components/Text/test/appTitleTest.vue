<template>
  <div style="width: 100%; height: 100%;">
    <app-title :title="'answerrr'" :upperCase="true" :fontSize="35" :textShadow="'2px 2px red'"></app-title>
  </div>
</template>

<script>
import appTitle from "@/components/Text/appTitle.vue";
  export default {
    components: {
      appTitle
    }
  }
</script>

<style scoped>
</style>
