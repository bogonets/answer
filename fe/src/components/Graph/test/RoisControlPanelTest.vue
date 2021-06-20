<template>
  <div>
    <v-card>
      <!-- <v-list>
        <v-list-item dense>
            <v-row :class="`d-flex align-center`">
              <signal-button></signal-button>
              <v-spacer></v-spacer>
              <v-switch :label="$t('show_rois')"></v-switch>
            </v-row>
        </v-list-item>
        <v-divider></v-divider>
      </v-list> -->
      <v-list>
        <v-list-group
          v-for="(item, index) in items"
          :key="index"
          v-model="item.active"
          no-action
        >
          <template v-slot:activator>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </template>
          <v-list-item
            class="pl-6 tile"
            v-for="(prop, index) in item.props"
            background-color="primary"
            :key="index"
          >
            <v-list-item-content dense>
              <!-- <v-list-item-title>{{ prop.title}}</v-list-item-title> -->
              <v-btn
                v-if="prop.type === 'button'"
                @click="relayMeta(prop.name)"
                >{{ prop.name }}</v-btn
              >
              <div v-if="isList(prop.valid)">
                <v-select
                  v-model="prop.value"
                  dense
                  menu-props="auto"
                  :items="getListFromValid(prop.valid)"
                ></v-select>
              </div>
              <v-text-field
                v-bind:label="prop.title"
                dense
                v-if="
                  prop.type === 'text' ||
                    (prop.type === 'float' && !isList(prop.valid))
                "
                v-model="prop.value"
              ></v-text-field>
              <template v-if="prop.type === 'array'">
                <v-list-item-subtitle>{{ prop.title }}</v-list-item-subtitle>
                <v-row no-gutters>
                  <v-col
                    dense
                    v-for="(item, index) in prop.defaultValue"
                    :key="index"
                    cols="sm"
                  >
                    <v-text-field class="pa-2" tile value="item">
                    </v-text-field></v-col
                ></v-row>
              </template>
              <template v-if="prop.type === 'color'">
                <v-list-item-subtitle>{{ prop.title }}</v-list-item-subtitle>
                <v-color-picker
                  width="100%"
                  background-color="transparent"
                  dense
                  hide-inputs
                  hide-canvas
                  hide-mode-switch
                  :show-swatches="false"
                ></v-color-picker
              ></template>
            </v-list-item-content>
            <v-card-actions></v-card-actions>
          </v-list-item>
          <v-card-actions>
            <!-- delete dialog 추후 component 화 -->
            <v-dialog v-model="deleteDialog" width="500">
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  :class="'mr-auto'"
                  text
                  color="error"
                  v-bind="attrs"
                  v-on="on"
                  >Delete</v-btn
                ></template
              >
              <v-card>
                <v-card-title class="headline">Delete Props</v-card-title>
                <v-card-text>really delete?</v-card-text>
                <v-divider></v-divider>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="grey" text @click="deleteDialog = false"
                    >Cancel</v-btn
                  >
                  <v-btn color="primary" text @click="deleteProp">Accept</v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
            <v-btn text color="secondary">Cancel</v-btn>
            <v-btn text color="primary">Save</v-btn>
          </v-card-actions>
        </v-list-group>
        <v-divider></v-divider>
      </v-list>
      <v-list>
        <v-list-item outline>
          <v-list-item-content>
            <!-- <v-select
              v-model="selectItem"
              :items="modeItems"
              item-text="title"
              item-value="id"
              item-key="modeItems"
              label="Select Mode"
              @change="changeMode"
            ></v-select> -->
            <!-- add item dialog -->
            <v-card-actions :class="`d-flex justify-center`">
              <v-dialog v-model="addDialog" width="500">
                <template v-slot:activator="{ on, attr }">
                  <!-- <v-btn icon @click="addItem(modeId)"> -->
                  <v-btn icon v-bind="attr" v-on="on">
                    <v-icon>
                      add
                    </v-icon>
                  </v-btn>
                </template>
                <v-card>
                  <v-card-title class="headline">Add Props</v-card-title>
                  <v-select
                    width="300px"
                    v-model="selectItem"
                    :items="modeItems"
                    item-text="title"
                    item-value="id"
                    item-key="modeItems"
                    label="Select Mode"
                    @change="changeMode"
                  ></v-select>
                  <v-divider></v-divider>
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="grey" text @click="addDialog">Cancel</v-btn>
                    <v-btn color="primary" text @click="addItem(modeId)"
                      >Accept</v-btn
                    >
                  </v-card-actions>
                </v-card>
              </v-dialog>
            </v-card-actions>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-card>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import Component from "vue-class-component";
import SignalButton from "@/components/LambdaWidget/Option/signalButton.vue";

@Component({
  components: {
    SignalButton
  }
})
export default class TestTemplate extends Vue {
  mounted() {
    this.setTestItems();
  }

  private deleteDialog = false;
  private addDialog = false;
  private modeId = 0;
  private selectItem: object = {
    id: 0,
    title: "[OCR] Input < Return"
  };
  private modeItems: Array<object> = [
    { id: 0, title: "Input < Return" },
    { id: 1, title: "Input > Return" },
    { id: 2, title: "Input < Return < Input" },
    { id: 3, title: "Return < Input < Return" },
    { id: 4, title: "Image Match" },
    { id: 5, title: "Color Match" }
  ];
  private items: Array<object> = Array<object>();
  private props: Array<object> = [
    {
      id: 0,
      name: "range_over",
      // title: "range over",
      title: "range over",
      value: 0,
      defaultValue: "0",
      type: "float"
    },
    {
      id: 1,
      name: "range_under",
      title: "range under",
      value: 0,
      defaultValue: "0",
      type: "float"
    },
    {
      id: 2,
      name: "range_between",
      title: "range between",
      value: [],
      defaultValue: [100, 1000],
      type: "array"
    },
    {
      id: 3,
      name: "range_outside",
      title: "range outside",
      value: [],
      defaultValue: [100, 1000],
      type: "array"
    },
    {
      id: 4,
      name: "threshold",
      title: "threshold",
      value: "0.8",
      defaultValue: "0.8",
      type: "float"
    },
    {
      id: 5,
      name: "match_color",
      title: "match color",
      value: "",
      defaultValue: "",
      type: "color"
    },
    {
      id: 6,
      name: "capture",
      title: "capture",
      type: "button",
      default: true
    },
    {
      id: 7,
      name: "line_style",
      title: "line style",
      type: "color",
      default: true
    }
  ];

  private deleteProp() {
    this.deleteDialog = false;
  }

  private changeMode(id: number) {
    this.modeId = id;
  }

  private relayMeta(guiName: string) {
    if (guiName == "roi_setting") {
    } else if (guiName == "capture") {
    }
  }

  private addItem(id: number) {
    // api 구현 필요
    var item = {
      id: this.items.length + 1,
      title: this.props[id]["title"],
      props: [this.props[id]]
    };

    for (var prop of this.props) {
      if (prop["default"]) {
        item.props.push(prop);
      }
    }

    this.items.push(item);
    this.addDialog = false;
  }

  private isList(valid: object): boolean {
    if (valid && valid.hasOwnProperty("list")) {
      return true;
    } else {
      return false;
    }
  }

  private getListFromValid(valid: object): any {
    if (this.isList(valid)) {
      return valid["list"].split(";");
    } else [];
  }

  setTestItems() {
    this.items.push({
      // lambda id
      id: 1,
      title: "ROIs Template",
      props: this.props
    });
  }
}
</script>
<style scoped>
.tile {
  background: #424242;
}
</style>
