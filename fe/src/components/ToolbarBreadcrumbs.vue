<template>
  <v-toolbar flat dense height="32">
    <v-breadcrumbs class="pa-0" :items="currentItems">

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
import {Component, Prop, Watch} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';

@Component
export default class ToolbarBreadcrumbs extends VueBase {

  @Prop({ type: Array, default: () => [] })
  readonly items!: Array<object>;

  currentItems = [] as Array<object>;

  mounted() {
    this.updateItems();
  }

  updateItems() {
    if (this.items.length >= 3 && this.$vuetify.breakpoint.smAndUp) {
      this.currentItems = this.items;
    } else {
      this.currentItems = [
        this.items[0],
        {
          text: '...',
          disabled: false,
          href: this.onClickEllipsis,
        },
        this.items[this.items.length - 1],
      ];
    }
  }

  onClickEllipsis() {
  }

  onClickNavigation(href) {
    if (typeof href === 'function') {
      href.call();
    } else {
      this.moveTo(href);
    }
  }
}
</script>
