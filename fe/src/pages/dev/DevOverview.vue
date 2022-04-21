<i18n lang="yaml">
en:
  python: 'Python {0}'

ko:
  python: 'Python {0}'
</i18n>

<template>
  <v-container>
    <v-progress-linear
      absolute
      top
      color="primary"
      v-show="loading"
      :indeterminate="loading"
    ></v-progress-linear>

    <toolbar-breadcrumbs :items="breadcrumbs"></toolbar-breadcrumbs>
    <v-divider></v-divider>

    <v-row class="mt-2">
      <v-col cols="auto">
        <card-button>
          <v-icon large>mdi-language-python</v-icon>
          <span class="text--secondary text-subtitle-2 text-no-wrap">
            {{ $t('python', [item.python]) }}
          </span>
        </card-button>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarBreadcrumbs from '@/components/ToolbarBreadcrumbs.vue';
import CardButton from '@/components/CardButton.vue';
import {VersionsA} from '@/packet/system';

@Component({
  components: {
    ToolbarBreadcrumbs,
    CardButton,
  },
})
export default class DevOverview extends VueBase {
  private readonly breadcrumbs = [
    {
      text: 'Dev',
      disabled: false,
      href: () => this.moveToDev(),
    },
    {
      text: 'Overview',
      disabled: true,
    },
  ];

  loading = false;
  item = {} as VersionsA;

  created() {
    this.loading = true;
    this.$api2
      .getDevSystemVersions()
      .then(item => {
        this.loading = false;
        this.item = item;
      })
      .catch(error => {
        this.loading = false;
        this.toastRequestFailure(error);
      });
  }
}
</script>
