<template>
  <div>
    <v-row no-gutters>
      <v-col :cols="12">
        <v-text-field 
        hide-details
        :solo="solo"
        :label="label"
        :dense="dense"
        :shaped="shaped"
        :filled="filled"
        :outlined="outlined"
        v-model="text"
        @input="onInput($event)">
        <template v-slot:append>
          <v-icon @click="onShowResult" :title="$t('show_chips')">{{ extensionIcon }}</v-icon>
        </template>
        </v-text-field>
      </v-col>
      <v-col v-if="showResult" :cols="12" class="resultZone">
        <v-chip v-for="(data, index) in result" :key="index" small class="chips" close close-icon="close" @click:close="onDeleteUnit(data, index)">{{ data }}</v-chip>
      </v-col>
    </v-row>
  </div>
</template>

<script>
  export default {
    name: "aCsvInput",
    props: {
      solo: {
        type: Boolean,
        default: false
      },
      label: {
        type: String,
        default: undefined
      },
      dense: {
        type: Boolean,
        default: false
      },
      shaped: {
        type: Boolean,
        default: false
      },
      filled: {
        type: Boolean,
        default: false
      },
      outlined: {
        type: Boolean,
        default: false
      },
      value: {
        type: String,
        default: undefined
      }
    },
    data () {
      return {
        text: this.value,
        showResult: false
      }
    },
    computed: {
      result: {
        get() {
          if (this.text !== null && this.text !== undefined) {
            if (this.text.length > 0) {
              if (this.text.includes(",")) {
                return this.text.split(",");
              } else {
                return [this.text];
              }
            }
          }
          return null;
        },
        set(newValue) {
          this.text = newValue.toString();
        }
      },
      extensionIcon () {
        if (this.showResult) {
          return "keyboard_arrow_up";
        } else {
          return "keyboard_arrow_down";
        }
      }
    },
    watch: {
      text () {
        if (this.text !== null && this.text !== undefined) {
          if (typeof this.text === "string") {
            if (this.text.length <= 0) {
              this.$emit("input", "");
            } 
          }
        }
      }
    },
    methods: {
      onInput: function (event) {
        if (this.text.includes(" ")) {
          this.text = this.text.replace(/ /gi, "");
        }
        if (this.text !== null && this.text !== undefined) {
          if (this.text.length > 0) {
            if (this.text.includes(",")) {
              this.$emit("returnArray", this.text.split(","));
            } else {
              this.$emit("returnArray", [this.text]);
            }
          } else {
            return [];
          }
        } else {
          return [];
        }
        this.$emit("input", this.text);
      },
      onShowResult: function () {
        this.showResult = !this.showResult;
      },
      onDeleteUnit: function (search, index) {
        this.result.splice(index, 1);
        this.result = [...this.result];
        this.onInput();
      }
    },
    mounted () {
      this.$nextTick()
      .then(() => {
        this.onInput();
      })
    }
  }
</script>

<style scoped>
.resultZone {
  margin-top: 3px !important;
}
</style>
