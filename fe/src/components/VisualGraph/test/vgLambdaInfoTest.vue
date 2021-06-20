<template>
  <div style="width: 100%; height: 100%">
    <vg-lambda-info :infos="infos"></vg-lambda-info>
  </div>
</template>

<script>
import vgLambdaInfo from "@/components/VisualGraph/vgLambdaInfo.vue";
export default {
  props:{

  },
  components:{
    vgLambdaInfo
  },
  data(){
    return {
      infos: {
        "author": "zer0",
        "backend": "builtin",
        "bugs": "https://answer.bogonets.com/",
        "dependencies": [],
        "descriptions": 
        {
          "en": "Displays the current time as an image.",
          "ko": "\ud604\uc7ac \uc2dc\uac04\uc744 \uc774\ubbf8\uc9c0\ub85c \ucd9c\ub825\ud55c\ub2e4."
        },
        "documentation_mime": "text",
        "documentations": {},
        "engines": "1.0.2",
        "homepage": "https://answer.bogonets.com/",
        "keywords": 
        [
          "builtin"
        ],
        "license": "Bogonet License",
        "meta": "",
        "name": "clock_image",
        "titles": 
        {
          "en": "Clock Image",
          "ko": "\uc2dc\uacc4 \uc774\ubbf8\uc9c0"
        },
        "use_system_packages": true,
        "version": "1.0.2"
      }
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
