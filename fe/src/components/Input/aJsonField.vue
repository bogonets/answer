<template>
  <div id="div" ref="jsonField">
    <textarea id="textarea" ref="textarea" v-model="text" :readonly="readonly"></textarea>
    <v-btn-toggle multiple id="buttonGroup">
      <v-btn small icon id="copy" @click.stop="onCopy" :title="$t('copy')"><v-icon size="18">fas fa-copy</v-icon></v-btn>
      <v-divider v-if="!readonly" vertical></v-divider>
      <v-btn v-if="!readonly" small icon id="clear" @click.stop="onClear" :title="$t('clear')"><v-icon size="20">clear</v-icon></v-btn>
    </v-btn-toggle>
    <transition name="fade">
    <span v-if="message" id="message" :style="{color: messageColor}">{{ message }}</span>
    </transition>
  </div>
</template>

<script>
export default {
  name: "aJsonField",
  version: "0.9.0",
  props:{
    /**
     * You want to view data.
     */
    json: {
      type: Object,
      default: undefined
    },
    /**
     * Readonly.
     */
    readonly: {
      type: Boolean,
      default: false,
    },
    /**
     * JSON Format Tab Size.
     */
    tabSize: {
      type: Number,
      default: 2
    },
    /**
     * Change string and object about result data.
     */
    resultObject: {
      type: Boolean,
      default: true
    },
    /**
     * textarea resize options. "none", "vertical", "horizontal", "both"
     */
    resize: {
      type: String,
      default: "vertical"
    }
  },
  components:{

  },
  data(){
    return {
      color: {success: "rgb(120, 120, 250)", error: "rgb(236, 95, 86)", copy: "rgb(80, 160, 80)"},
      text: null,
      timeout: null,
      message: null,
      messageColor: null,
      msgTimeout: null,
    }
  },
  computed:{
  },
  watch: {
    json () { // props json data watch -> change string data.
      if (this.json) {
        this.text = JSON.stringify(this.json, null, this.tabSize);
      }
    },
    text () {
      this.timeout = setTimeout(() => {
        var obj = null;
        try {
          obj = JSON.parse(this.text);
          this.onSuccess(obj);
          /**
           * Trans result data.
           * @type {emit}
           * @param {object} - result data.
           */
          this.$emit("transData", obj);
        } catch (e) {
          this.onError(e);
        }
      }, 800);
    },
    message () {
      if (this.message) {
        if (this.message.includes("Error")) {
          return;
        }
        this.msgTimeout = setTimeout(() => {
          this.message = null;
        }, 2000);
      }
    }
  },
  methods:{
    /**
     * Text Copy at Clipboard.
     * @public
     * @param {null}
     */
    onCopy: function () {
      var textarea = this.$refs.textarea;
      if (textarea) {
        textarea.select();
        textarea.setSelectionRange(0, 99999);
        document.execCommand("copy");
        this.message = "Copied.";
        this.messageColor = this.color.copy;
      } else {
        this.message = "Copy Failed.";
        this.messageColor = this.color.error;
        this.$warn(this.$options.name, "onCopy", "textarea is ", textarea);
      }
    },

    /**
     * Text All clean.
     * @public
     * @param {null}
     */
    onClear: function () {
      this.text = "";
    },

    /**
     * Json Parse Success. Display Success message.
     * @public
     * @param {object} - JSON Data.
     */
    onSuccess: function (obj) {
      this.message = "Success.";
      this.messageColor = this.color.success;
    },

    /**
     * Json Parse Error. Display Error message.
     * @public
     * @param {error} - Error Message.
     */
    onError: function (e) {
      this.message = "Error. Not Matched JSON Format.";
      this.messageColor = this.color.error;
      this.$error(this.$options.name, "onError", e);
    }
  },
  created(){
    if (this.json) {
      this.text = JSON.stringify(this.json, null, this.tabSize);
    }
  },
  mounted(){
    if (this.$refs.textarea) {
      this.$refs.textarea.style.resize = this.resize;
      if (this.resize === "vertical") {
        this.$refs.jsonField.style.width = "100%";
      } else if (this.resize === "horizontal") {
        this.$refs.jsonField.style.height = "100%";
      } 
      // else if (this.resize === "both" || this.resize === "none") {
      //   this.$refs.jsonField.style.width = "100%";
      //   this.$refs.jsonField.style.height = "100%";
      // }
    } else {
      setTimeout(() => {
        if (this.$refs.textarea) {
          this.$refs.textarea.style.resize = this.resize;
          if (this.resize === "vertical") {
            this.$refs.jsonField.style.width = "100%";
          } else if (this.resize === "horizontal") {
            this.$refs.jsonField.style.height = "100%";
          } 
          // else if (this.resize === "both" || this.resize === "none") {
          //   this.$refs.jsonField.style.width = "100%";
          //   this.$refs.jsonField.style.height = "100%";
          // }
        }
      }, 600);
    }
  },
  beforeDestroy() {
    if (this.timeout !== null) {
      clearTimeout(this.timeout);
      this.timeout = null;
    }
    if (this.msgTimeout) {
      clearTimeout(this.msgTimeout);
      this.msgTimeout = null;
    }
    if (this.message) {
      this.message = null;
    }
  }
}
</script>

<style scoped>
#div{
  display: inline-block;
  position: relative;
}
#buttonGroup {
  margin: 0;
  padding: 0;
  position: absolute;
  top: 5px;
  right: 20px;
}
#copy{
  width: 22px;
  height: 22px;
}
#clear{
  width: 22px;
  height: 22px;
}

#textarea{
  display:block;
  resize: both;
  min-width: 180px;
  min-height: 57px;
  width: 100%;
  height: 100%;
  outline: none;
  border: 2px solid;
  border-radius: 4px;
}
#textarea::selection {
  background: none;
  color: unset;
}
#textarea::-moz-selection {
  background: none;
  color: unset;
}
#textarea:focus {
  border-color: rgb(75, 117, 204);
  outline: none;
}
#message {
  margin-left: 5px;
  font-size: 10px;
}

/* Transition */
.fade-enter-active {
	transition: opacity 0.6s;
}
.fade-leave-active {
	transition: opacity 0.6s;
}
.fade-enter,
.fade-leave-to {
	opacity: 0;
}

</style>