<template>
  <div class="optionZone">
    <v-btn :small="small" :icon="!!icon && !name" :color="color" @click="onSignal" :loading="reqSignal">
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
  name: "SignalButton",
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
      default: "Signal"
    },
    propertyName: {
      type: String,
      default: undefined
    },
    signal: {
      type: Object,
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
    lambdaProps: {
      default: undefined
    }
  },
  components:{

  },
  data(){
    return {
      reqSignal: false,
      copySignal: null,
    }
  },
  computed:{
    iconRight () {
      return !this.iconLeft
    }
  },
  methods:{
    onSignal: function () {
      // this.$debug(this.$options.name, "onSignal::To API", "AccessToken:", this.$store.getters["user/getAccessToken"]);
      // this.$debug(this.$options.name, "onSignal::To API", "RefreshToken:", this.$store.getters["user/getRefreshToken"]);
      // this.$debug(this.$options.name, "onSignal::To API", "Selected Project:", this.$store.getters["project/getSelectProject"]);
      this.$debug(this.$options.name, "onSignal::To API", "TaskName:", this.taskName, "LambdaUid:", this.lambdaUid, "propertyName:", this.propertyName);
      this.$debug(this.$options.name, "onSignal::To API", "Signal:", this.copySignal);
      this.reqSignal = true;

      // test.
      // alert(`TaskName: ${this.taskName}\nLambdaUid: ${this.lambdaUid}\npropertyName:${this.propertyName}\nsignal:${JSON.stringify(this.copySignal)}`);
      // this.$emit("signal", "https://i.ebayimg.com/images/g/KncAAOSw1ZJebEl1/s-l640.jpg");
    }
  },
  created(){
    if (this.signal) {
      this.copySignal = this.$util.cloneObject(this.signal);
      if (Object.keys(this.copySignal).length > 0) {
        if (this.copySignal.signalName) {
          if (this.copySignal.signalName.includes("${PROPS.")) {
            var temp = this.copySignal.signalName.split("${PROPS.");
            var parseName = [];
            for (let index = 0; index < temp.length; ++index) {
              if (temp[index].includes("}")) {
                var name = temp[index].split("}");
                parseName.push(name[0]);
              }
            }
            if (parseName.length > 0) {
              if (this.lambdaProps.length > 0) {
                var keywords = {};
                for (let j = 0; j < parseName.length; ++j) {
                  for (let i = 0; i < this.lambdaProps.length; ++i) {
                    if (this.lambdaProps[i].name === parseName[j]) {
                      keywords['${PROPS.' + parseName[j] + '}'] = this.lambdaProps[i].component.value;
                    }
                  }
                }
              }
            }
            var keys = Object.keys(keywords);
            if (keys.length > 0) {
              for (let key of keys) {
                this.copySignal.signalName = this.copySignal.signalName.replace(key, keywords[key]);
              }
            }
          }
        }
        // if (this.copySignal.name) {
        //   this.copySignal.name = this.copySignal.name.replace("${OWN}", this.lambdaUid);
        // }
        // if (this.copySignal.input_queries) {
        //   if (this.copySignal.input_queries.length > 0) {
        //     for (let index = 0; index < this.copySignal.input_queries.length; ++index) {
        //       this.copySignal.input_queries[index] = this.copySignal.input_queries[index].replace("${OWN}", this.lambdaUid);
        //     }
        //   }
        // }
        // if (this.copySignal.output_queries) {
        //   if (this.copySignal.output_queries.length > 0) {
        //     for (let index = 0; index < this.copySignal.output_queries.length; ++index) {
        //       this.copySignal.output_queries[index] = this.copySignal.output_queries[index].replace("${OWN}", this.lambdaUid);
        //     }
        //   }
        // }
        this.copySignal.lambda_name = this.lambdaUid;
      }
    }
  },
  mounted(){
  },
  beforeDestroy(){
  },
  subscriptions() {
		const $reqSignal = this.$watchAsObservable("reqSignal", {immediate: true})
    .pluck("newValue")
    .filter(reqSignal => reqSignal == true) // if signal is true.
    .debounceTime(1000)
    return {
      getBuckets: Observable.combineLatest($reqSignal, reqSignal => ({reqSignal})).flatMap(({reqSignal}) => 
      this.$api.signalLambda(this.$store.getters["user/getAccessToken"], this.$store.getters["user/getRefreshToken"], this.$store.getters["project/getSelectProject"], this.taskName, this.lambdaUid, this.propertyName, this.copySignal)
          .do(res => {
            // success.
            var data = null;
            if (res.headers['content-type']) {
              if (res.headers['content-type'].includes("image")) {
                var bin = Buffer.from(res.data, 'binary').toString('base64');
                var result = `data:${res.headers['content-type']};base64,` + bin;
                data = result;
              } else {
                data = res.data.result.obj;
              }
            } else {
              data = res.data.result.obj;
            }
            this.$emit("signal", data);
          })
          .catch(error => {
            // failed.
						return Observable.of(null);
          })
          .do(() => {
            this.reqSignal = false;
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
