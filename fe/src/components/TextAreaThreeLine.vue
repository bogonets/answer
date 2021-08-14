<template>
  <name-slot-hint
      :label="label"
      :hint="hint"
  >
    <v-textarea
        hide-details
        :disabled="disabled"
        :outlined="outlined"
        :filled="filled"
        :auto-grow="autoGrow"
        :rows="rows"
        :row-height="rowHeight"
        :value="value"
        @input="input"
    ></v-textarea>
  </name-slot-hint>
</template>

<script lang="ts">
import {Vue, Component, Prop, Emit} from 'vue-property-decorator';
import NameSlotHint from '@/components/NameSlotHint.vue';

@Component({
  components: {
    NameSlotHint,
  }
})
export default class TextFieldThreeLine extends Vue {
  @Prop({type: String, default: ''})
  readonly label!: string;

  @Prop({type: String, default: ''})
  readonly hint!: string;

  @Prop({type: Boolean, default: false})
  readonly disabled!: boolean;

  @Prop({type: Boolean, default: false})
  readonly outlined!: boolean;

  @Prop({type: Boolean, default: false})
  readonly filled!: boolean;

  @Prop({type: Boolean, default: false})
  readonly autoGrow!: boolean;

  @Prop({type: Number})
  readonly rows!: number;

  @Prop({type: Number})
  readonly rowHeight!: number;

  @Prop({type: String, default: ''})
  readonly value!: string;

  @Emit()
  input(value: string) {
    return value;
  }
}
</script>
