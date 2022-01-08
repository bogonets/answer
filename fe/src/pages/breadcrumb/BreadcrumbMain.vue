<template>
  <toolbar-breadcrumbs
      :items="items"
  ></toolbar-breadcrumbs>
</template>

<script lang="ts">
import {Component, Prop} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarBreadcrumbs from '@/components/ToolbarBreadcrumbs.vue';

@Component({
  components: {
    ToolbarBreadcrumbs,
  }
})
export default class BreadcrumbMain extends VueBase {
  @Prop({type: String, default: ''})
  readonly name!: string;

  private readonly items = [
    {
      text: this.$route.params.group,
      disabled: false,
      href: () => this.moveToGroup(),
    },
    {
      text: this.$route.params.project,
      disabled: false,
      href: () => this.moveToMain(),
    },
    {
      text: this.name,
      disabled: true,
    },
  ];
}
</script>
