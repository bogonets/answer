<template>
  <v-card min-width="350px">
    <v-card-title>
      <span class="headline">{{ infos.titles[$store.getters['language/getLanguage']] || infos.name }}</span>
      <v-spacer></v-spacer>
    </v-card-title>
    <v-card-subtitle v-if="infos.version" style="padding-bottom: 5px; font-weight: bold;">
      <v-card-actions style="margin: 0px; padding: 0px;">
        <div class="subtitle--version">
          <span>{{ 'version - ' + infos.version }}</span>
        </div>
        <v-spacer v-if="infos.license"></v-spacer>
        <div v-if="infos.license" class="subtitle--license">
          <span>{{ infos.license }}</span>
        </div>
      </v-card-actions>
    </v-card-subtitle>
    <v-divider></v-divider>
    <v-card-text>
      <v-container fluid grid-list-lg ref="viewZone">
        <!-- @slot this is viewer (content) zone. -->
        <slot name="view">
          <v-layout row wrap>
            <v-flex xs12 md6 v-if="infos.descriptions">
             <div v-if="infos.name" class="subInfo">
                <span>{{ $t('lambdaInfo.original_name') }}&nbsp;:&nbsp;</span>
                <span>{{ infos.name }}</span>
              </div>
              <div v-if="infos.author" class="subInfo">
                <span>{{ $t('lambdaInfo.author') }}&nbsp;:&nbsp;</span>
                <span>{{ infos.author }}</span>
              </div>
              <!-- <div v-if="infos.documentation_mime" class="subInfo">
                <span>{{ $t('lambdaInfo.mime_type') }}&nbsp;:&nbsp;</span>
                <span>{{ infos.documentation_mime }}</span>
              </div> -->
              <div v-if="infos.engines" class="subInfo">
                <span>{{ $t('lambdaInfo.engines') }}&nbsp;:&nbsp;</span>
                <span>{{ infos.engines }}</span>
              </div>
              <div v-if="infos.use_system_packages !== null && infos.use_system_packages !== undefined" class="subInfo">
                <span>{{ $t('lambdaInfo.use_system_packages') }}&nbsp;:&nbsp;</span>
                <span>{{ infos.use_system_packages ? $t('lambdaInfo.use') : $t('lambdaInfo.unuse') }}</span>
              </div>
              <div v-if="infos.bugs" class="subInfo">
                <span>{{ $t('lambdaInfo.bug_report') }}&nbsp;:&nbsp;</span>
                <span>{{ infos.bugs }}</span>
              </div>
              <div v-if="infos.homepage" class="subInfo">
                <span>{{ $t('lambdaInfo.homepage') }}&nbsp;:&nbsp;</span>
                <a :href="infos.homepage" target="_blank">{{ infos.homepage }}</a>
              </div> 
            </v-flex>
            <v-flex xs12 md6>
              <div class="subInfo--description" style="height: 100%;">
                <v-sheet class="subInfo--description__title">
                  <span>{{ $t('lambdaInfo.descriptions') }}</span>
                </v-sheet>
                <pre style="white-space: pre-line;">{{ infos.descriptions[$store.getters['language/getLanguage']] || infos.descriptions }}</pre>
              </div>
            </v-flex>
          </v-layout>
        </slot>
      </v-container>
    </v-card-text>
    <v-divider></v-divider>
    <v-card-actions>
      <!-- @slot this is Options (buttons) zone. -->
      <slot name="options">
        <v-btn text @click="onClose">
          <span>{{ $t('close') }}</span>
        </v-btn>
      </slot>
    </v-card-actions>
    <v-icon v-if="isDialog" size="20" class="close--icon" @click="$emit('close')">close</v-icon>
  </v-card>
</template>

<script>
export default {
  props:{
    /**
     * This is info value of Lambda template.
     */
    infos: {
      type: Object
    }
  },
  components:{

  },
  data(){
    return {

    }
  },
  computed:{

  },
  methods:{
    /**
     * Close event. For close dialog.
     * @public
     */
    onClose: function () {
      this.$debug(this.$options.name, "onClose", "Emit event!");
      /**
       * Close event. Transfer event to parent element.
       * @type {emit}
       * @param {null}
       */
      this.$emit("onClose");
    }
  },
  created(){

  },
  mounted(){
    
  }
}
</script>
<style scoped>
.subtitle--version {
  font-size: 15px;
  color: grey;
}
.subtitle--license {
  font-size: 15px;
  color: burlywood;
}
.subInfo--description__title {
  position: absolute;
  top: -12px;
}
.subInfo--description {
  display: inline-block;
  position: relative;
  border: 1px solid;
  border-radius: 10px;
  padding: 10px;
  width: 100%;
  font-weight: bold;
}
</style>