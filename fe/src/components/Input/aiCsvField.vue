<template>
  <v-combobox
  ref="self"
  :label="label"
  :items="items"
  :outlined="outline"
  :dense="dense"
  multiple
  clearable
  small-chips
  hide-no-data
  hide-selected
  hide-details
  v-model="listData"
  :value="listData"
  @change="transValue"
  @focusout.stop="onFocusout($event)"
  @keydown.capture="onKeyDown($event)"
  >
    <template v-slot:selection="data">
      <v-chip
      small
      :input-value="data.selected"
      close
      @click:close="removeChip(data.item)">
        <span>{{data.item}}</span>
      </v-chip>
    </template>
  </v-combobox>
</template>
<script>
export default {
  props:{
    label: {
      type: String,
      default: undefined
    },
    items: {
      type: Array,
      default: undefined
    },
    preValue: {
      type: String,
      default: null
    },
    outline: {
      type: Boolean,
      default: false
    },
    dense: {
      type: Boolean,
      default: false
    },
    resultArray: {
      type: Boolean,
      default: false
    }
  },
  components:{
  },
  data(){
    return {
      name: "aiCsvField",
      listData: [],
      inputValue: false
    }
  },
  computed:{
  },
  watch: {
  },
  methods:{
    onFocusout: function ($event) {
      this.inputValue = this.$refs.self.$refs.input.value;
      if (this.inputValue) {
        this.inputValue = !!this.inputValue;
      } else {
      }
    },
    transValue: function ($event) {
      if (this.inputValue) {
        if (this.listData.length !== 0) {
          this.$debug(this.name, "transValue", "Input Value is not empty.", "Try delete last value.");
          this.listData.pop();
        }
        this.inputValue = false;
        return;
      }
      this.$debug(this.name, "transValue", "Options: result-array =", this.resultArray);
      if (this.resultArray) {
        if ($event.length !== 0) {
          this.$emit("input", $event);
        } else {
          this.$emit("input", null);
        }
      } else {
        this.$emit("input", this.$util.arrayToCsv($event));
      }
    },
    removeChip: function (chip) {
      if (typeof chip === "number") {
        this.listData.splice(chip, 1);
      } else {
        this.listData.splice(this.listData.indexOf(chip), 1);
      }
      this.listData = [...this.listData];
      this.$debug(this.name, "removeChip", "Remove Chip!");
      this.transValue(this.listData);
    },
    onKeyDown: function (e) {
      if (e.keyCode === 188) { //Comma
        e.preventDefault();
        var enter = new KeyboardEvent('keydown', {
          code: "Enter",
          key: "Enter",
          charCode: 13,
          keyCode: 13,
          view: window
        })
        var self = this.$refs.self;
        self.$refs['input'].dispatchEvent(enter);
      }
    }
  },
  created(){

  },
  mounted() {
    this.$nextTick(() => {
      if (typeof this.$attrs.value === "string") {
        if (this.$attrs.value) {
          if (this.$attrs.value.includes(",")) {
            var tmp = this.$attrs.value.split(",");
            for (var i = 0; i < tmp.length; ++i) {
              this.listData.push(tmp[i]);
            }
          } else {
            this.listData.push(this.$attrs.value);
          }
        }
      } else if (typeof this.$attrs.value === "array" || typeof this.$attrs.value === "object") {
        var tmp = this.$util.cloneObject(this.$attrs.value)
        for (var i in tmp) {
          this.listData.push(tmp[i]);
        }
      }
      this.$debug(this.name, "mounted", "Init Value:", this.$attrs.value, "Type:", typeof this.$attrs.value);
      // if (this.listData) {
      //   this.transValue(this.listData);
      // }
    })
  }
}
</script>
<style scoped>

</style>