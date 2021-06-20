<template>
  <v-app-bar>
    <v-card id="main-detail">
      <v-card-title style="margin: 0; padding: 0;">
        <v-toolbar height="24">
          <span>setting</span>
        </v-toolbar>
      </v-card-title>
      <transition name="fade">
        <template v-for="item in items">
          <v-card-text :key="item.title" v-if="item.active">
            <template v-for="subItem in item.items">
              <v-text-field
                :key="subItem.title"
                :value="subItem.title"
                :label="subItem.title"
              >
              </v-text-field>
            </template>
          </v-card-text>
        </template>
      </transition> 
      </v-card >
      </v-app-bar>
</template>
<script>
import Vue from "vue";
import Component from "vue-class-component";

@Component
export default class RoiNavigationTest extends Vue {
  items = [];
  showWidget = false;

  mounted() {
    this.items.push(this.testData());
    // this.items.push(this.testData());
  }
  testData() {
    var data = {
      id: 1,
      uid: "uid",
      title: "title1",
      active: true,
      action: "local_activity",
      items: [
        {
          id: 12,
          title: "button",
          type: "button"
        },
        {
          id: 10,
          title: "text",
          type: "text",
          value: "isData"
        },
        {
          id: 10,
          title: "text(null)",
          type: "text",
          value: ""
        }
      ]
    };
    return data;
  }
}
</script>
