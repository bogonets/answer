<template>
  <div v-if="header == 'sleep' || header == 'auto' || header == 'on_off'">
    <v-btn :disabled="!operator" v-on:click="onButtonClick(header)">
      {{ getButtonText(item) }}
    </v-btn>
  </div>
  <div v-else-if="header == 'wind_control'">
    <v-dialog
      v-if="operator"
      v-model="dialog"
      persistent
      max-width="300px"
      @click:outside="cancel"
    >
      <template v-slot:activator="{ on, attrs }">
        <div v-bind="attrs" v-on="on">{{ syncedItem }}</div>
      </template>
      <v-card>
        <v-card-title>{{ $t("wind_control") }}</v-card-title>
        <v-select
          v-model="editString"
          :items="airVolumnControl"
          class="mx-5"
          hide-details
          outlined
        ></v-select>
        <v-card-actions>
          <v-spacer />
          <v-btn class="ma-2" v-on:click="save(editString)">
            {{ $t("save") }}
          </v-btn>
          <v-btn class="ma-2" v-on:click="cancel">{{ $t("cancel") }}</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <template v-else>
      <div>{{ syncedItem }}</div>
    </template>
  </div>
  <div v-else>
    <v-dialog
      v-if="operator"
      v-model="dialog"
      persistent
      max-width="300px"
      @click:outside="cancel"
    >
      <template aria-disabled="operator" v-slot:activator="{ on, attrs }">
        <div v-bind="attrs" v-on="on">{{ syncedItem }}</div>
      </template>
      <v-card>
        <v-card-title>{{ $t("change_property") }}</v-card-title>
        <v-text-field
          v-model="editString"
          label="Edit"
          single-line
          class="mx-5"
          outlined
          hide-details
        ></v-text-field>
        <v-card-actions>
          <v-spacer />
          <v-btn class="ma-2" v-on:click="save(editString)">
            {{ $t("save") }}
          </v-btn>
          <v-btn class="ma-2" v-on:click="cancel">{{ $t("cancel") }}</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <template v-else aria-disabled="operator">
      <div>{{ syncedItem }}</div>
    </template>
  </div>
</template>

<script lang="ts">
import { Vue, Component, PropSync, Prop } from "vue-property-decorator";

@Component
export default class TableItem extends Vue {
  @PropSync("item", { type: String }) private syncedItem!: string;
  @Prop() private header!: any;
  @Prop() private serial!: any;

  operator!: boolean;

  editString!: any;
  dialog = false;

  // DoubleClick Event
  clicks = 0;
  delay = 300;
  timer: any;

  // Temp Data
  airVolumnControl = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"];

  buttonText = ["ON", "OFF"];

  created() {
    this.editString = this.syncedItem;
    this.operator = this.$store.getters["project/isOperator"];
  }

  close() {
    console.log("close");
  }

  open() {
    console.log("open");
  }

  cancel() {
    this.editString = this.syncedItem;
    this.dialog = false;
  }

  save(item: any) {
    this.syncedItem = item;
    this.dialog = false;

    let data: [string, any];
    data = [this.header, item];

    const editData = {
      serial: this.serial,
      header: this.header,
      value: item,
    };

    this.$emit("editItem", editData);
  }

  getButtonText(flag: boolean) {
    if (flag) return this.buttonText[0];
    return this.buttonText[1];
  }

  onSave() {
    // this.$refs["editDialog"].isActive = true;
  }
  closeDialog() {}

  onButtonClick(header: string) {
    this.$emit("buttonEvent", { serial: this.serial, header: header });
  }

  btnClick() {
    this.clicks++;
    if (this.clicks === 1) {
      this.timer = setTimeout(() => {
        this.clicks = 0;

        // one Click Event
        console.log("one click");
      }, this.delay);
    } else {
      clearTimeout(this.timer);
      this.clicks = 0;

      // double Click Event
      console.log("double click");
      this.dialog = true;
    }
  }
}
</script>
