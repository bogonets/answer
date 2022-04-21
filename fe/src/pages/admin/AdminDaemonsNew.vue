<i18n lang="yaml">
en:
  header: 'New Daemon'
  subheader: 'A daemon is a program that runs in the background.'

ko:
  header: '새로운 데몬'
  subheader: '데몬은 백그라운드에서 실행되는 프로그램 입니다.'
</i18n>

<template>
  <v-container>
    <toolbar-breadcrumbs :items="navigationItems"></toolbar-breadcrumbs>
    <v-divider></v-divider>
    <left-title :header="$t('header')" :subheader="$t('subheader')">
      <form-daemon
        hide-cancel-button
        :loading-plugin="loadingPlugins"
        :disable-plugin="loadingPlugins"
        :loading-submit="loadingSubmit"
        :disable-submit-button="loadingSubmit"
        :plugins="plugins"
        @ok="onClickOk"
      ></form-daemon>
    </left-title>
  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarBreadcrumbs from '@/components/ToolbarBreadcrumbs.vue';
import LeftTitle from '@/components/LeftTitle.vue';
import FormDaemon from '@/components/FormDaemon.vue';
import type {DaemonA, CreateDaemonQ} from '@/packet/daemon';

@Component({
  components: {
    ToolbarBreadcrumbs,
    LeftTitle,
    FormDaemon,
  },
})
export default class AdminDaemonsNew extends VueBase {
  readonly navigationItems = [
    {
      text: 'Admin',
      disabled: false,
      href: () => this.moveToAdmin(),
    },
    {
      text: 'Daemons',
      disabled: false,
      href: () => this.moveToAdminDaemons(),
    },
    {
      text: 'New',
      disabled: true,
    },
  ];

  loadingPlugins = false;
  loadingSubmit = false;
  plugins = [] as Array<string>;

  created() {
    this.updatePlugins();
  }

  updatePlugins() {
    this.loadingPlugins = true;
    this.$api2
      .getAdminDaemonPlugins()
      .then(items => {
        this.loadingPlugins = false;
        this.plugins = items;
      })
      .catch(error => {
        this.loadingPlugins = false;
        this.toastRequestFailure(error);
      });
  }

  onClickOk(event: DaemonA) {
    const body = {
      plugin: event.plugin,
      slug: event.slug,
      name: event.name,
      address: event.address,
      description: event.description,
      enable: event.enable,
    } as CreateDaemonQ;

    this.loadingSubmit = true;
    this.$api2
      .postAdminDaemons(body)
      .then(() => {
        this.loadingSubmit = false;
        this.toastRequestSuccess();
        this.moveToBack();
      })
      .catch(error => {
        this.loadingSubmit = false;
        this.toastRequestFailure(error);
      });
  }
}
</script>
