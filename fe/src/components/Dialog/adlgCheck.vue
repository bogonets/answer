<template>
  <v-dialog
    v-model="open"
    scrollable 
    persistent :overlay="false"
    max-width="500px"
    transition="dialog-transition"
    :dark="this.$vuetify.theme.dark">
    <v-card>
      <v-card-title primary-title>
        <v-icon color="warning">{{icon}}</v-icon>
        <h3 class="headline mb-0">{{title}}</h3>
      </v-card-title>
      <v-divider></v-divider>
      <v-card-text class="pa-5">
        <p v-for="(message, index) in real_messages" :key="index">
          {{(message)}}
        </p>
      </v-card-text>
      <v-divider></v-divider>
      <v-card-actions>
        <v-btn @click="onCancel">{{$t('cancel')}}</v-btn>
        <v-spacer></v-spacer>
        <v-btn @click="onOk">{{$t('ok')}}</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
/**
 * Confirm check dialog.
 * @author hadoo
 */
export default {
  name: 'AnswerCheckContent',
  props:{
    /**
     * Show and hide dialog.
     */
    open: {
      type: Boolean,
      default: false
    },

    /**
     * Icon (material icons, font awesome icons)
     */
    icon: {
      type: String,
      default: 'warning'
    },

    /**
     * Dialog title.
     */
    title: {
      type: String,
      default: 'warning'
    },

    /**
     * Dialog message.
     */
    messages: {
      type: Array,
      default() { return ['real_continue'] }
    },

    /**
     * Use i18n.
     */
    msgI18n: {
      type: Boolean,
      default: false
    }
  },
  data(){
    return {
    }
  },
  computed:{
    real_messages() {
      if (this.msgI18n) {
        var cvtMsg = [];
        for (var msg of this.messages) {
          cvtMsg.push(this.$t(msg));
        }
        return cvtMsg
      } else {
        return this.messages;
      }
    }
  },
  methods:{
    /**
     * Cancel event for close dialog.
     * @public
     */
    onCancel: function () {
      /**
       * For close dialog.
       * @property {boolean} - failed value false.
       */
      this.$emit("onCancel", false);
    },

    /**
     * Ok event for check answer true.
     */
    onOk: function () {
      /**
       * For answer true about check.
       * @property {boolean} - success value true.
       */
      this.$emit("onOk", true);
    }
  },
  created(){
  },
  mounted(){
  }
}
</script>

<style scoped>

</style>