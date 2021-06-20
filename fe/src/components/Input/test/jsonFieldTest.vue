<template>
  <div style="width: 100%; height: 100%; border: 1px solid blue;">
    <v-layout row wrap>
      <v-flex xs1>
        <v-btn @click="test">test</v-btn>
      </v-flex>
      <v-flex xs11>
        <a-json-field
        :json="jsonData"
        :tabSize="4"
        :resultObject="true"
        :readonly="false"
        :resize="'vertical'"
        @transData="onChanged"></a-json-field>
      </v-flex>
    </v-layout>
  </div>
</template>
<script>
import aJsonField from "@/components/Input/aJsonField.vue";
export default {
  name: "jsonFieldTester",
  version: "1.0.0",
  props:{

  },
  components:{
    aJsonField
  },
  data(){
    return {
      jsonData: null
    }
  },
  computed:{

  },
  watch:{
  },
  methods:{
    onChanged: function ($event) {
      if (typeof $event === "object") {
        this.jsonData = $event;
      } else if (typeof $event === "string") {
        this.jsonData = JSON.parse($event);
      }
      this.$debug(this.$options.name, "onChanged", "Recieve data:\n", $event);
      this.$debug(this.$options.name, "onChanged", "Recieve data type:\n", typeof $event); 
      this.$debug(this.$options.name, "onChanged", "Changed Data:\n", this.jsonData);
    },
    test: function () {
      if (this.jsonData.key) {
        this.jsonData = {wow: "wowwowowow", how: "howhowhowhow"};
      } else {
        this.jsonData = {key: "keykey", ho: "hoho"};
      }
    }
  },
  created(){

  },
  mounted(){
    var token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1ODEzOTkxMDksImlhdCI6MTU4MTMxMjcwOSwidXNyIjoiYm9nbyJ9.8WgqXKGgRJboDhEWpYECK0BuqhV5iiFtj7MkgNjbBcY"
    var dec = this.$util.decodeToken(token);
    this.jsonData = dec;
  }
}
</script>
<style scoped>
#textarea {
  resize: both;
}

</style>