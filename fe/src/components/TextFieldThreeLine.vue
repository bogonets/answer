<template>
  <name-slot-hint
      :label="label"
  >
    <v-text-field
        class="mt-0 mb-2"
        persistent-hint
        ref="textField"
        dense
        :disabled="disabled"
        :filled="disabled"
        :type="type"
        :autocomplete="autocomplete"
        :rules="rules"
        :prefix="prefix"
        :suffix="suffix"
        :value="value"
        :hint="hint"
        @input="input"
    ></v-text-field>
  </name-slot-hint>
</template>

<script lang="ts">
import {Vue, Component, Prop, Emit, Ref} from 'vue-property-decorator';
import NameSlotHint from '@/components/NameSlotHint.vue';
import {VTextField} from 'vuetify/lib/components/VTextField';

@Component({
  components: {
    NameSlotHint,
  }
})
export default class TextFieldThreeLine extends Vue {
  @Prop({type: String})
  readonly label!: string;

  @Prop({type: String})
  readonly hint!: string;

  @Prop({type: Boolean})
  readonly dense!: boolean;

  @Prop({type: Boolean})
  readonly outlined!: boolean;

  @Prop({type: Boolean})
  readonly disabled!: boolean;

  @Prop({type: String, default: 'text'})
  readonly type!: string;

  @Prop({type: String, default: 'off'})
  readonly autocomplete!: string;

  @Prop({type: String})
  readonly value!: string;

  @Prop({type: String})
  readonly prefix!: string;

  @Prop({type: String})
  readonly suffix!: string;

  @Prop({type: Array})
  readonly rules!: Array<object>;

  @Ref()
  readonly textField!: VTextField;

  get valid(): boolean {
    return this.textField['valid']();
  }

  @Emit()
  input(value) {
    return value;
  }
}
</script>
