<template>
  <div>
    <v-card class="panel">
      <v-list>
        <v-list-group
          v-for="(prop, index) in props"
          :key="index"
          v-model="prop.active"
          no-action
          @click="onPropertySelect(index, prop.active)"
        >
          <template v-slot:activator>
            <v-list-item-title>{{ getTitle(prop) }}</v-list-item-title>
          </template>

          <!-- GreaterThan -->
          <v-list-item class="pl-6 tile" v-if="prop.greaterThanEnable">
            <v-list-item-content>
              <v-list-item-subtitle>{{
                $t("greater_than")
              }}</v-list-item-subtitle>
              <!-- prettier-ignore -->
              <v-text-field dense v-model="prop.greaterThanValue"
              ></v-text-field>
            </v-list-item-content>
          </v-list-item>

          <!-- LessThan -->
          <v-list-item class="pl-6 tile" v-if="prop.lessThanEnable">
            <v-list-item-content>
              <v-list-item-subtitle>{{ $t("less_than") }}</v-list-item-subtitle>
              <v-text-field dense v-model="prop.lessThanValue"></v-text-field>
            </v-list-item-content>
          </v-list-item>

          <!-- WithinRange -->
          <v-list-item class="pl-6 tile" v-if="prop.withinRangeEnable">
            <v-list-item-content>
              <v-list-item-subtitle>{{
                $t("within_range")
              }}</v-list-item-subtitle>
              <v-row no-gutters>
                <v-col dense cols="sm">
                  <v-text-field
                    class="pa-2"
                    tile
                    label="min"
                    v-model="prop.withinRangeValue.min"
                  ></v-text-field>
                </v-col>
                <v-col dense cols="sm">
                  <v-text-field
                    class="pa-2"
                    tile
                    label="max"
                    v-model="prop.withinRangeValue.max"
                  ></v-text-field>
                </v-col>
              </v-row>
            </v-list-item-content>
          </v-list-item>

          <!-- OutOfRange -->
          <v-list-item class="pl-6 tile" v-if="prop.outOfRangeEnable">
            <v-list-item-content>
              <v-list-item-subtitle>{{
                $t("out_of_range")
              }}</v-list-item-subtitle>
              <v-row no-gutters>
                <v-col dense cols="sm">
                  <v-text-field
                    class="pa-2"
                    tile
                    label="min"
                    v-model="prop.outOfRangeValue.min"
                  ></v-text-field>
                </v-col>
                <v-col dense cols="sm">
                  <v-text-field
                    class="pa-2"
                    tile
                    label="max"
                    v-model="prop.outOfRangeValue.max"
                  ></v-text-field>
                </v-col>
              </v-row>
            </v-list-item-content>
          </v-list-item>

          <!-- Threshold -->
          <v-list-item class="pl-6 tile" v-if="prop.thresholdEnable">
            <v-list-item-content>
              <v-list-item-subtitle>{{ $t("threshold") }}</v-list-item-subtitle>
              <v-text-field dense v-model="prop.thresholdValue"></v-text-field>
            </v-list-item-content>
          </v-list-item>

          <!-- RGBColor -->
          <v-list-item class="pl-6" v-if="prop.rgbColorEnable">
            <v-list-item-content>
              <template>
                <v-list-item-subtitle>{{
                  $t("rgb_color")
                }}</v-list-item-subtitle>
                <v-row>
                  <v-spacer></v-spacer>
                  <v-color-picker
                    dense
                    light
                    align-center
                    hide-mode-switch
                    v-model="selectedRGBColor"
                  ></v-color-picker>
                  <v-spacer></v-spacer
                ></v-row>
              </template>
            </v-list-item-content>
          </v-list-item>

          <!-- Line Style -->
          <v-list-item class="pl-6 tile">
            <v-list-item-content>
              <template>
                <v-list-item-subtitle>{{
                  $t("line_style")
                }}</v-list-item-subtitle>
                <v-row>
                  <v-spacer></v-spacer>
                  <v-color-picker
                    hide-inputs
                    hide-mode-switch
                    v-model="selectedLineColor"
                  ></v-color-picker>
                  <v-spacer></v-spacer>
                </v-row>
              </template>
            </v-list-item-content>
          </v-list-item>

          <!-- Capture Button -->
          <v-list-item class="pl-6 tile">
            <v-list-item-content dense>
              <v-btn @click="onCapture()">Capture</v-btn>
            </v-list-item-content>
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
                >
              </template>
              <v-card>
                <v-card-title class="headline">Delete Props</v-card-title>
                <v-card-text>really delete?</v-card-text>
                <v-divider></v-divider>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="grey" text @click="deleteDialog = false"
                    >Cancel</v-btn
                  >
                  <v-btn color="primary" text @click="onDeleteProp"
                    >Accept</v-btn
                  >
                </v-card-actions>
              </v-card>
            </v-dialog>
            <v-btn text color="secondary">Cancel</v-btn>
            <v-btn text color="primary" @click="onSaveProp">Save</v-btn>
          </v-card-actions>
        </v-list-group>
        <v-divider></v-divider>
      </v-list>

      <v-list>
        <v-list-item outline>
          <v-list-item-content>
            <!-- add item dialog -->
            <v-card-actions :class="`d-flex justify-center`">
              <v-dialog v-model="addDialog" width="500">
                <template v-slot:activator="{ on, attr }">
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
                    :items="propertyTitleList"
                    item-text="title"
                    item-value="id"
                    item-key="propertyTitleList"
                    v-model="currentPropertyTitle"
                    label="Selected Property"
                    @change="onSelectedProperty"
                  ></v-select>
                  <v-divider></v-divider>
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="grey" text @click="onCancle">Cancel</v-btn>
                    <v-btn color="primary" text @click="onAddProp(modeId)"
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
import { Vue, Component, Prop, Watch } from "vue-property-decorator";
import SignalButton from "@/components/LambdaWidget/Option/signalButton.vue";
import * as BaseRois from "@/components/Graph/BaseRois.ts";
import { distinctUntilKeyChanged } from "rxjs/operator/distinctUntilKeyChanged";

export class RoisPanelEvent {
  index = -1;
  data: BaseRois.Property | undefined;

  constructor(index, data: BaseRois.Property | undefined = undefined) {
    this.index = index;
    this.data = data;
  }
}

@Component({
  components: {
    SignalButton
  }
})
export default class RoisControlPanel extends Vue {
  /** RoI's information dictionary. */
  @Prop({
    type: BaseRois.RoiInfoDictionary
  })
  readonly roisInfos!: BaseRois.RoiInfoDictionary;

  /** Rois Property */
  private props = new Array<BaseRois.Property>();

  /** Watch values: Color-picker aync data type is object type. */
  private selectedRGBColor = { r: 0, g: 0, b: 255 };
  private selectedLineColor = { r: 0, g: 0, b: 255 };

  private modeId = 0;

  private deleteDialog = false;
  private addDialog = false;

  private items: Array<object> = new Array<object>();
  private currentPropertyTitle: object = {
    id: 0,
    title: this.$t("greater_than")
  };
  private propertyTitleList: Array<object> = [
    { id: 0, title: this.$t("greater_than") },
    { id: 1, title: this.$t("less_than") },
    { id: 2, title: this.$t("within_range") },
    { id: 3, title: this.$t("out_of_range") },
    { id: 4, title: this.$t("threshold") },
    { id: 5, title: this.$t("rgb_color") }
  ];

  private currentListIndex = -1;

  private onPropertySelect(index, active) {
    if (active == undefined || !active) {
      this.currentListIndex = index;
      this.selectedLineColor = this.props[
        index
      ].lineStyleColorValue.toIntegerObject();
      this.selectedRGBColor = this.props[index].rgbColorValue.toIntegerObject();

      this.$emit("select", new RoisPanelEvent(index));
    }
  }

  private getTitle(prop) {
    if (prop.greaterThanEnable) {
      return this.$t("greater_than");
    } else if (prop.lessThanEnable) {
      return this.$t("less_than");
    } else if (prop.withinRangeEnable) {
      return this.$t("within_range");
    } else if (prop.outOfRangeEnable) {
      return this.$t("out_of_range");
    } else if (prop.thresholdEnable) {
      return this.$t("threshold");
    } else if (prop.rgbColorEnable) {
      return this.$t("rgb_color");
    }
  }

  private onSaveProp() {
    this.$emit(
      "save",
      new RoisPanelEvent(
        this.currentListIndex,
        this.props[this.currentListIndex]
      )
    );
  }

  private onDeleteProp() {
    this.deleteDialog = false;
    this.props.splice(this.currentListIndex, 1);

    this.$emit("delete", new RoisPanelEvent(this.currentListIndex));
  }

  private onSelectedProperty(id: number) {
    this.modeId = id;
  }

  private onCapture() {
    this.$emit("capture", new RoisPanelEvent(this.currentListIndex));
  }

  private onCancle() {
    this.addDialog = false;
  }

  private onAddProp(id: number) {
    let prop = new BaseRois.Property();

    if (id == 0) {
      prop.greaterThanEnable = true;
    } else if (id == 1) {
      prop.lessThanEnable = true;
    } else if (id == 2) {
      prop.withinRangeEnable = true;
    } else if (id == 3) {
      prop.outOfRangeEnable = true;
    } else if (id == 4) {
      prop.thresholdEnable = true;
    } else if (id == 5) {
      prop.rgbColorEnable = true;
    }

    this.props.push(prop);
    this.addDialog = false;
  }

  public getRoisInfos() {
    this.$debug(this.$options.name, "setRoisInfos", `Rois : ${this.roisInfos}`);
    return this.roisInfos;
  }

  public setRoisInfos(data) {
    this.$debug(this.$options.name, "setRoisInfos", `Rois : ${data}`);

    for (var key in this.props) {
      delete this.props[key];
    }

    const infos = new BaseRois.RoiInfoDictionary(data);
    infos.elems.forEach((v, k, m) => {
      this.props.push(infos.get(k).property);
    });

    this.$emit("roisinfos", infos);
  }

  @Watch("selectedRGBColor")
  onRGBColorChanged() {
    if (this.currentListIndex != -1) {
      this.props[this.currentListIndex].rgbColorValue.setByInteger(
        this.selectedRGBColor.r,
        this.selectedRGBColor.g,
        this.selectedRGBColor.b
      );
    }
  }

  @Watch("selectedLineColor", { immediate: true })
  onLineColorChanged() {
    if (this.currentListIndex != -1) {
      this.props[this.currentListIndex].lineStyleColorValue.setByInteger(
        this.selectedLineColor.r,
        this.selectedLineColor.g,
        this.selectedLineColor.b
      );
    }
  }
}
</script>

<style scoped>
.panel {
  display: inline-block;
  position: absolute;
  width: 100%;
  height: 100%;
}
.tile {
  background: #424242;
}
</style>
