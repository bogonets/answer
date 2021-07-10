<template>
  <div class="appTitleContainer" ref="container">
    <span class="appTitle" ref="content">{{ upperCase ? title.toUpperCase() : title }}</span>
  </div>
</template>

<script>
  export default {
    name: "AppTitle",
    props: {
      /**
       * Title text.
       */
      title: {
        type: String,
        default: "answer"
      },
      /**
       * Title text uppercase.
       */
      upperCase: {
        type: Boolean,
        default: true
      },
      /**
       * CSS Font size : number px.
       */
      fontSize: {
        type: Number,
        default: 35
      },
      /**
       * CSS Font style : italic, oblique etc..
       */
      fontStyle: {
        type: String,
        default: 'italic'
      },
      /**
       * Text shadow style : width px, height px, color.
       */
      textShadow: {
        type: String,
        default: undefined
      }
    },
    data () {
      return {
      }
    },
    created () {
    },
    mounted () {
      this.$nextTick()
      .then(() => {
        if (this.$refs.content) {
          this.$refs.content.style['font-size'] = `${this.fontSize}px`;
          this.$refs.content.style['font-style'] = this.fontStyle;
          if (this.textShadow) {
            this.$refs.content.style['text-shadow'] = this.textShadow;
          }
        }
      })
    },
    beforeDestroy () {
    },
    methods: {
    }
  }
</script>

<style scoped>
.appTitleContainer {
  width: fit-content;
}

.appTitle {
  font-family: Impact, Haettenschweiler, 'Arial Narrow Bold', sans-serif;
  -ms-user-select: none;
  -moz-user-select: -moz-none;
  -webkit-user-select: none;
  -khtml-user-select: none;
  user-select: none;
}
</style>
