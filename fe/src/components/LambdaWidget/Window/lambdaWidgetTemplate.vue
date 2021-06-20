<template>
  <v-card class="lambdaWidgetCard">
    <v-toolbar dense height="55px">
      <slot name="topLeft">
      </slot>
      <v-spacer></v-spacer>
      <slot name="topCenter">
      </slot>
      <v-spacer></v-spacer>
      <slot name="topRight">
      </slot>
    </v-toolbar>

    <div class="bodyZone">
      <slot name="body"></slot>
		</div>

    <v-footer dense absolute height="55px">
      <slot name="footerLeft"></slot>
      <v-spacer></v-spacer>
      <slot name="footerCenter"></slot>
      <v-spacer></v-spacer>
      <slot name="footerRight"></slot>
    </v-footer>
  </v-card>
</template>

<script>
export default {
  name: "LambdaWidgetTemplate",
  props:{

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

  },
  created(){

  },
  mounted(){

  }
}
</script>

<style scoped>
.lambdaWidgetCard {
  width: 100%;
  height: 100%;
}
.bodyZone {
  position: absolute;
  display: inline-block;
	width: 100%;
	height: calc(100% - 110px);
  top: 55px;
}
</style>