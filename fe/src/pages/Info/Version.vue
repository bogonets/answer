<template>
  <div>
    <v-container v-if="useContainer" grid-list-lg id="versionPage">
      <v-layout row wrap>
        <v-flex xs12>
          <v-card id="cardUnit">
            <v-card-title id="title">
              <strong :style="{color: core.titleColor}">{{core.title}}</strong>
              <v-spacer></v-spacer>
              <strong :style="{color: core.titleColor}">{{'v.' + core.version}}</strong>
            </v-card-title>
          </v-card>
        </v-flex>
        <v-flex xs12>
          <v-card id="cardUnit">
            <v-card-title id="title">
              <strong :style="{color: api.titleColor}">{{api.title}}</strong>
              <v-spacer></v-spacer>
              <strong :style="{color: api.titleColor}">{{'v.' + api.version}}</strong>
            </v-card-title>
          </v-card>
        </v-flex>
        <v-flex xs12>
          <v-card id="cardUnit">
            <v-card-title id="title">
              <strong :style="{color: web.titleColor}">{{web.title}}</strong>
              <v-spacer></v-spacer>
              <strong :style="{color: web.titleColor}">{{'v.' + web.version}}</strong>
            </v-card-title>
          </v-card>
        </v-flex>
      </v-layout>
      <v-card-actions style="padding: 0; border: 1px solid red;">
        <v-spacer></v-spacer>
        <!-- Bogonets.com -->
        <!-- <a id="homepage" href="https://www.bogonets.com" target="_blank" title="https://www.bogonets.com">
          <img src="@/assets/bogonet_logo.png" width="180" height="50"/>
        </a> -->
        <!-- Answer homepage -->
        <a id="homepage" href="https://answer.bogonets.com" target="_blank" title="https://answer.bogonets.com" style="padding-top: 10px;">
          <app-title :title="'answer'" :upperCase="true" :fontSize="35" :textShadow="'2px 2px grey'"></app-title>
        </a>
      </v-card-actions>
    </v-container>
    <div v-else>
      <v-layout row wrap>
        <v-flex xs12 class="ma-bt-10">
          <v-card id="cardUnit">
            <v-card-title id="title">
              <strong :style="{color: core.titleColor}">{{core.title}}</strong>
              <v-spacer></v-spacer>
              <strong :style="{color: core.titleColor}">{{'v.' + core.version}}</strong>
            </v-card-title>
          </v-card>
        </v-flex>
        <v-flex xs12 class="ma-bt-10">
          <v-card id="cardUnit">
            <v-card-title id="title">
              <strong :style="{color: api.titleColor}">{{api.title}}</strong>
              <v-spacer></v-spacer>
              <strong :style="{color: api.titleColor}">{{'v.' + api.version}}</strong>
            </v-card-title>
          </v-card>
        </v-flex>
        <v-flex xs12 class="ma-bt-10">
          <v-card id="cardUnit">
            <v-card-title id="title">
              <strong :style="{color: web.titleColor}">{{web.title}}</strong>
              <v-spacer></v-spacer>
              <strong :style="{color: web.titleColor}">{{'v.' + web.version}}</strong>
            </v-card-title>
          </v-card>
        </v-flex>
      </v-layout>
      <v-card-actions style="padding: 0">
        <v-spacer></v-spacer>
        <!-- Bogonets.com -->
        <!-- <a id="homepage" href="https://www.bogonets.com" target="_blank" title="https://www.bogonets.com">
          <img src="@/assets/bogonet_logo.png" width="180" height="50"/>
        </a> -->
        <!-- Answer homepage -->
        <a id="homepage" href="https://answer.bogonets.com" target="_blank" title="https://answer.bogonets.com" style="padding-top: 10px;">
          <app-title :title="'answer'" :upperCase="true" :fontSize="35" :textShadow="'2px 2px grey'"></app-title>
        </a>
      </v-card-actions>
    </div>
  </div>
</template>

<script>
import { Observable } from "rxjs";
export default {
  name: "AnswerVersionPage",
  props:{
    useContainer: {
      type: Boolean,
      default: true
    }
  },
  components:{

  },
  data(){
    return {
      coreSignal: false,
      apiSignal: false,

      core : {
        title: "Core",
        titleColor: "cyan",
        version: "version",
        describe: {
          docLabel: "Core Documentation",
          url: "https://github.com/osom8979",
          author: "Osom8979",
          detail: "This is Answer`s core.\nMake from C++"
        }
      },
      api: {
        title: "API",
        titleColor: "greenyellow",
        version: "version",
        describe: {
          docLabel: "API Documentation",
          url: "https://github.com/wooruang",
          author: "Wooruang",
          detail: "Thie is Answer`s API.\nMake from Scala"
        }
      },
      web: {
        title: "WEB",
        titleColor: "burlywood",
        version: this.$version,
        describe: {
          docLabel: "Web Documentation",
          url: "http://127.0.0.1:6060",
          author: "Hadoo",
          detail: "This is Answer`s WEB.\nMake from Vuejs"
        }
      },
    }
  },
  computed:{

  },
  methods:{
    // gotoProject: function () {
    //   this.$router.push(this.$page.project);
    // }
  },
  created(){
    this.coreSignal = true;
    this.apiSignal = true;
  },
  mounted(){
    this.$nextTick()
    .then(() => {
      console.debug(`%c${this.web.title} v${this.web.version}`, `color: ${this.web.titleColor}; font-weight: bold; font-size: 20px; border: 1px solid ${this.web.titleColor}; padding: 5px;`);
    })
  },
  subscriptions() {
		const $coreSignal = this.$watchAsObservable("coreSignal", {immediate: true})
		.pluck("newValue")
    .filter(coreSignal => coreSignal == true) // if signal is true.
    const $apiSignal = this.$watchAsObservable("apiSignal", {immediate: true})
		.pluck("newValue")
    .filter(apiSignal => apiSignal == true) // if signal is true.
    return {
      coreResult: Observable.combineLatest($coreSignal, coreSignal => ({coreSignal}))
      .flatMap(({coreSignal}) =>
        this.$api.getCoreVersion()
        .do(res => { 
          this.$debug(this.$options.name, "subscriptions::getCoreVersion", "Core Version response:", res);
          var version = res.result.obj.info;
          this.core.version = version;
          console.debug(`%c${this.core.title} v${this.core.version}`, `color: ${this.core.titleColor}; font-weight: bold; font-size: 20px; border: 1px solid ${this.core.titleColor}; padding: 5px;`);
        })
        .catch(err => {
          this.$error(this.$options.name, "subscriptions::getCoreVersion", JSON.parse(JSON.stringify(err)));
          return Observable.of(null);
        })
        .do(() => this.coreSignal = false)
      ),
      apiResult: Observable.combineLatest($apiSignal, apiSignal => ({apiSignal}))
      .flatMap(({apiSignal}) =>
        this.$api.getApiVersion()
        .do(res => { 
          this.$debug(this.$options.name, "subscriptions::getApiVersion", "API Version response:", res);
          var version = res.result.obj.info;
          this.api.version = version;
          console.debug(`%c${this.api.title} v${this.api.version}`, `color: ${this.api.titleColor}; font-weight: bold; font-size: 20px; border: 1px solid ${this.api.titleColor}; padding: 5px;`);
        })
        .catch(err => {
          this.$error(this.$options.name, "subscriptions::getApiVersion", err);
          return Observable.of(null);
        })
        .do(() => this.apiSignal = false)
      )
    }
  }
}
</script>

<style scoped>
#versionPage {
  width: 100%;
  height: 100%;
  padding-top: 10px;
  padding-bottom: 10px;
  -ms-user-select: none;
	-moz-user-select: -moz-none;
	-webkit-user-select: none;
	-khtml-user-select: none;
	user-select: none;
}
#back {
  cursor: pointer;
  width: fit-content;
  height: fit-content;
  padding-left: 15px;
  padding-right: 15px;
  padding-top: 5px;
  padding-bottom: 5px;
  border-radius: 8px;
}
#back:hover {
  background-color: rgba(125, 125, 125, 0.3);
}
#back:active {
  background-color: rgba(125, 125, 125, 0.9);
}
#cardUnit {
  width: 100%;
  height: 100%;
}
#cardBogo {
  width: 100%;
  height: 100%;
}
#title {
  font-size: 25px;
}
#describe {
  padding: 10px;
  word-break: break-all;
  font-size: 15px;
}
#homepage {
  text-decoration: underline;
  color: rgb(153, 193, 67);
  /* background: linear-gradient(to right, #fff 80%, rgb(153, 193, 67) 20%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent; */
}
.ma-bt-10 {
	margin-bottom: 10px;
}
</style>