<template>
  <div class="optionZone">
    <v-btn :small="small" :icon="!!icon && !name" :color="color" @click="onControlRead" :loading="signal">
      <v-icon v-if="!!icon && iconLeft" :left="true">{{ icon }}</v-icon>
      <span v-if="!!name">{{ name }}</span>
      <v-icon v-if="!!icon && iconRight" :right="true">{{ icon }}</v-icon>
    </v-btn>
  </div>
</template>

<script>
import axios from 'axios'
import { Observable } from "rxjs";
export default {
  name: "ControlReadButton",
  props:{
    small: {
      type: Boolean,
      default: false
    },
    icon: {
      type: String,
      default: null
    },
    iconLeft: {
      type: Boolean,
      default: true
    },
    color: {
      type: String,
      default: undefined
    },
    name: {
      type: String,
      default: "Read"
    },
    propertyName: {
      type: String,
      default: undefined
    },

    // Auto.
    taskName: {
      type: String,
      default: undefined,
    },
    lambdaUid: {
      type: String,
      default: undefined
    },
  },
  components:{

  },
  data(){
    return {
      signal: false,
    }
  },
  computed:{
    iconRight () {
      return !this.iconLeft
    }
  },
  methods:{
    onControlRead: function () {
      // this.$debug(this.$options.name, "onControlRead::To API", "AccessToken:", this.$store.getters["user/getAccessToken"]);
      // this.$debug(this.$options.name, "onControlRead::To API", "RefreshToken:", this.$store.getters["user/getRefreshToken"]);
      // this.$debug(this.$options.name, "onControlRead::To API", "Selected Project:", this.$store.getters["project/getSelectProject"]);
      this.$debug(this.$options.name, "onControlRead::To API", "TaskName:", this.taskName, "LambdaUid:", this.lambdaUid, "propertyName:", this.propertyName);
      this.signal = true;

      // Test.
      // alert(`TaskName: ${this.taskName}\nLambdaUid: ${this.lambdaUid}\npropertyName:${this.propertyName}`);
      // this.$emit("transData", "0.07,0.14,0.85,0.70");
    }
  },
  created(){
  },
  mounted(){
  },
  beforeDestroy(){
  },
  subscriptions() {
		const $signal = this.$watchAsObservable("signal", {immediate: true})
    .pluck("newValue")
    .filter(signal => signal == true) // if signal is true.
    .debounceTime(1000)
    return {
      getBuckets: Observable.combineLatest($signal, signal => ({signal})).flatMap(({signal}) => 
      this.$api.getPropertyValue(this.$store.getters["user/getAccessToken"], this.$store.getters["user/getRefreshToken"], this.$store.getters["project/getSelectProject"], this.taskName, this.lambdaUid, this.propertyName)
          .do(res => {
            // success.
            // if data includes whitespace => delete whitespace.
            this.$emit("transData", res.result.obj);
          })
          .catch(error => {
            // failed.
						return Observable.of(null);
          })
          .do(() => {
            this.signal = false;
          })
      )
    }
  }
}
</script>

<style scoped>
.optionZone {
  margin: 5px 10px;
}
</style>
