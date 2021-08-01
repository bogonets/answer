<template>
  <v-toolbar flat dense height="32">
    <v-breadcrumbs class="pa-0" :items="items">

      <template v-slot:divider>
        <v-icon>mdi-chevron-right</v-icon>
      </template>

      <template v-slot:item="{ item }">
          <span v-if="item.disabled" class="text-overline">
            {{ item.text }}
          </span>
        <a v-else class="text-overline" @click="onClickNavigation(item.href)">
          {{ item.text }}
        </a>
      </template>

    </v-breadcrumbs>
  </v-toolbar>
</template>

<script lang="ts">
import { Component, Prop } from 'vue-property-decorator';
import VueBase from '@/base/VueBase';

@Component
export default class ToolbarNavigation extends VueBase {

  @Prop({ type: Array, default: () => [] })
  readonly items!: Array<object>;

  onClickNavigation(href) {
    this.moveTo(href);
  }
}
</script>
