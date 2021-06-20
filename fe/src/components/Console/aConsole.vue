<template>
<v-card class="consoleCard" ref="consoleCard" @mousewheel="onWheel($event)">
  <v-toolbar height="36" class="elevation-4 toolbar">
    <v-icon size="20">fas fa-terminal</v-icon>
    <v-spacer></v-spacer>
    <!-- TESTER -->
    <!-- <v-btn small icon color="primary" @click="fileLoad">
      <v-icon v-html="'fas fa-folder-open'"></v-icon>
    </v-btn> -->
    <v-spacer></v-spacer>
    <v-btn small icon @click="onCopy(null)"><v-icon size="18">fas fa-copy</v-icon></v-btn>
    <v-btn small icon @click="onDownload"><v-icon size="18">fas fa-download</v-icon></v-btn>
    <slot name="addOptionButton">
      <v-btn small icon @click="$emit('close')"><v-icon>close</v-icon></v-btn>
    </slot>
  </v-toolbar>
  <div ref="consoleSheet" class="consoleSheet" id="consoleSheet" v-html="text">
  </div>
</v-card>
</template>

<script>
// Mouse scroll event 적용이 필요. (스크롤을 제일 아래로 내렸을 때 최신 갱신 되는 텍스트를 보여주기.)
/**
 * Error Display board. (From API and CORE).
 * @author hadoo
 */
export default {
  name: "AnswerConsole",
  props:{
    /**
     * Background color value.
     */
    backgroundColor: {
      type: String,
      default: "rgba(125, 125, 125, 0.3)"
    },

    /**
     * Max lines.
     */
    maxLines: {
      type: Number,
      default: 10000
    }
  },
  components:{

  },
  data(){
    return {
      ansiUp: null,
      text: "",
      numberOflines: 0,
      autoScroll: true
    }
  },
  computed:{
    dark() {
      return this.$vuetify.theme.dark;
    }
  },
  methods:{
    // TEST.
    // fileLoad: function () {
    //   this.$emit('fileLoad');
    // },

    /**
     * Add console text.
     * @public
     * @param {string} - input consle text.
     */
    addConsole: function (text) {
      if (this.ansiUp) {
        this.text += this.ansiUp.ansi_to_html(text) + "<br/>";
        this.numberOflines++;
        if (this.numberOflines > this.maxLines) {
          this.text = "";
          this.numberOflines = 0;
        }
        if (this.autoScroll) {
          this.$nextTick()
          .then(() => {
            this.$refs.consoleSheet.scrollTop = this.$refs.consoleSheet.scrollHeight;
          })
        }
      } else {
        this.$warn(this.$options.name, "addConsole", "Wrong initialize.");
      }
    },

    /**
     * Text Copy at Clipboard.
     * @public
     * @param {boolean} - Copy to clipboard.
     */
    onCopy: function (isCopy) {
      var copy;
      if (isCopy === null || isCopy === undefined) {
        copy = true;
      } else {
        copy = !!isCopy;
      }
      
      var elm = this.$refs.consoleSheet;
      // for Internet Explorer

      if(document.body.createTextRange) {
        var range = document.body.createTextRange();
        range.moveToElementText(elm);
        range.select();
        range.setSelectionRange(0, 99999);
        if (copy) {
          document.execCommand("Copy");
        }
        // alert("Copied div content to clipboard");
        return range;
      } else if(window.getSelection) {
        // other browsers
        var selection = window.getSelection();
        var range = document.createRange();
        range.selectNodeContents(elm);
        selection.removeAllRanges();
        selection.addRange(range);
        if (copy) {
          document.execCommand("Copy");
        }
        // alert("Copied div content to clipboard");
        return selection;
      }
      return null;
    },

    /**
     * Downlaod console data - FileType: Text.log
     * @public
     */
    onDownload: function() {
      var clip = this.onCopy(false);
      if (!clip) {
        return;
      }
      var blob = new Blob([clip.focusNode.innerText], { type: "text/plain" });
      var downloader = document.createElement("a");
      downloader.style = "display: none";
      downloader.href = URL.createObjectURL(blob);
      var date = new Date();
      var year = date.getFullYear().toString();
      var month = (date.getMonth() + 1).toString();
      var day = date.getDate();
      downloader.download = year + "_" + month + "_" + day + "_" + ".log";
      // eslint-disable-next-line no-undef
      var self = this;
      var main = this.$refs.consoleCard;
      main.$el.appendChild(downloader);
      downloader.click();
      setTimeout(function() {
        // 다운로드가 안되는 경우 방지
        // eslint-disable-next-line no-undef
        main.$el.removeChild(downloader);
        self.clearClipboard();
      }, 300);
      this.$debug(
        this.$options.name,
        "onDownload",
        "Save console text. File:",
        year + "_" + month + "_" + day + "_" + ".log"
      );
    },

    /**
     * Mouse wheel event.
     * @public
     * @param {mouseWheelEvent} - For auto view latest.
     */
    onWheel: function (wheel) {
      if (wheel.deltaY < 0) {
        this.autoScroll = false;
      } else {
        this.autoScroll = this.$refs.consoleSheet.scrollHeight - this.$refs.consoleSheet.scrollTop === this.$refs.consoleSheet.clientHeight;
      }
    }
  },
  created(){
    var a = require("ansi_up");
    this.ansiUp = new a.default;
  },
  mounted(){
    this.$nextTick()
    .then(() => {
      this.$refs.consoleCard.$el.style.backgroundColor = this.backgroundColor;
    })
  }
}
</script>

<style scoped>
.consoleCard {
  width: 100%;
  height: 100%;
}
.toolbar >>> .v-toolbar__content {
  padding: 0;
  padding-left: 10px;
  padding-right: 10px;
  margin: 0;
}
.menu {
  margin-left: 2px;
  margin-right: 2px;
}
.consoleSheet {
  position: absolute;
  max-height: calc(100% - 36px);
  top: 36px;
  width: 100%;
  overflow-y: auto;
  text-shadow:
    -1px -1px 0 #000,
    1px -1px 0 #000,
    -1px 1px 0 #000,
    1px 1px 0 #000; 
}
</style>
