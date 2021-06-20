<template>
  <div id="main" ref="main">
      <img id="viewer" ref="viewer" 
      :alt="$t('no_img')"
      :src="src" 
      :style="'objectFit: ' + ratio"/>
  </div>
</template>
<script>
export default {
  props:{
    /**
		 * Image Ratio ON / OFF.
		 */
    isFill: {
      type: Boolean,
      default: true
    },
    /**
		 * Image Tag Source.
		 */
    src: {
      type: String,
      default: ""
    }
  },
  components:{
  },
  data(){
    return {
      ratio: 'fill', // image ratio type.
      status: false, // image status.
    }
  },
  computed:{
  },
  watch: {
    /**
     * Watch isFill value, Change ratio.
     */
    isFill() {
      if (this.isFill) {
        this.ratio = 'fill';
      } else {
        this.ratio = 'contain';
      }
    },
    // /**
    //  * Watch image src value, Set Image Status.
    //  */
    // src() {
    //   this.isReady();
    // }
  },
  methods:{
    // /**
		//  * Trans Event about Image View Status.
		//  * @param {null} - param is empty.
		//  * @public
		//  * @returns {event} - Image Status TRUE and FALSE.
		//  */
    // isReady: function () {
    //   var img = this.$refs.viewer;
    //   console.log("complete", img.complete);
    //   console.log("naturalWidth", img.naturalWidth);
    //   if (!img.complete || img.naturalWidth === 0) {
    //     this.status = false;
    //   } else {
    //     this.status = true;
    //   }
    //   this.$emit("isReady", this.status);
    // },
    // /**
		//  * Get Image Status.
		//  * @param {null} - param is empty.
		//  * @public
		//  * @returns {status} - Image Status (True or False).
		//  */
    // getStatus: function () {
    //   return this.status;
    // },
    /**
		 * Image Zoom in.
		 * @param {null} - param is empty.
		 * @public
		 * @returns {null}
		 */
    zoomIn: function () {
      var img = this.$refs.viewer;
      var width = img.clientWidth;
      var height = img.clientHeight;
      img.style.width = (width + 100) + 'px';
      img.style.height = (height + 100) + 'px';
    },
    /**
		 * Image Zoom out.
		 * @param {null} - param is empty.
		 * @public
		 * @returns {null}
		 */
    zoomOut: function () {
      var img = this.$refs.viewer;
      var width = img.clientWidth;
      var height = img.clientHeight;
      img.style.width = (width - 100) + 'px';
      img.style.height = (height - 100) + 'px';
    },
    /**
		 * Image Download.
		 * @param {type} - Image Type (jpeg, png, gif ...).
		 * @public
		 * @returns {null}
		 */
    download: function (type) {
      var format = null;
      switch(type) {
        case "image/png": {
          format = "png";
          break;
        }
        case "image/jpeg": {
          format = "jpg";
          break;
        }
        case "image/jpg": {
          format = "jpg";
          break;
        }
        case "image/gif": {
          format = "gif";
          break;
        }
        default: {
          format = "jpg";
          break;
        }
      }
      var main = this.$refs.main;
      var a = document.createElement("a")
        a.style = "display: none"
        a.href = this.src
        a.download = "new_file_name." + format;
        main.appendChild(a)
        a.click()
        setTimeout(function() {
        // 다운로드가 안되는 경우 방지
        main.removeChild(a)
        }, 300);
    }
  },
  created(){
  },
  mounted(){
    // Life Cycle Mounted, Check isFill value and Change ratio value.
    if (this.isFill) {
      this.ratio = 'fill';
    } else {
      this.ratio = 'contain';
    }
  },
}
</script>
<style scoped>
#main {
  position: absolute;
  width: 100%;
  height: 100%;
  overflow: auto;
}
#viewer {
  position: absolute;
  width: 100%;
  height: 100%;
}
</style>