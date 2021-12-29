<i18n lang="yaml">
en:
  groups: "Groups"
  projects: "Projects"

ko:
  groups: "Groups"
  projects: "Projects"
</i18n>

<template>
  <v-container>

    <span class="ml-2 text--primary text-overline">
      {{ $t('groups') }}
    </span>
    <v-divider></v-divider>
    <table-groups
        hide-filter-input
        hide-new-item-button
        hide-action-edit
        hide-action-move
        clickable-row
        :loading="loading"
        :items="groups"
        @click:row="onClickGroupRow"
    ></table-groups>

    <span v-if="!hideProjects" class="ml-2 text--primary text-overline">
      {{ $t('projects') }}
    </span>
    <v-divider v-if="!hideProjects"></v-divider>
    <table-projects
        v-if="!hideProjects"
        hide-filter-input
        hide-new-item-button
        hide-action-edit
        hide-action-move
        clickable-row
        :loading="loading"
        :items="projects"
        @click:row="onClickProjectRow"
    ></table-projects>

  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import TableGroups from '@/components/TableGroups.vue';
import TableProjects from '@/components/TableProjects.vue';
import type {GroupA} from '@/packet/group';
import type {ProjectA} from '@/packet/project';
import {OEMS_TO_HIDE_ROOT_PROJECT} from '@/packet/oem';

@Component({
  components: {
    TableGroups,
    TableProjects,
  }
})
export default class Root extends VueBase {
  loading = false;
  groups = [] as Array<GroupA>;
  projects = [] as Array<ProjectA>;

  created() {
    if (!this.$localStore.alreadySession) {
      this.moveToSignin();
      return;
    }

    this.requestSetup();
  }

  get hideProjects() {
    return OEMS_TO_HIDE_ROOT_PROJECT.includes(this.$localStore.preference.oem);
  }

  requestSetup() {
    this.loading = true;
    (async () => {
      await this._setup();
    })();
  }

  async _setup() {
    try {
      this.groups = await this.$api2.getMainGroups();
      this.projects = await this.$api2.getMainProjects();
    } catch (error) {
      this.toastRequestFailure(error);
    } finally {
      this.loading = false;
    }
  }

  onClickGroupRow(item: GroupA) {
    this.moveToGroupProjects(item.slug);
  }

  onClickProjectRow(item: ProjectA) {
    this.moveToMain(item.group_slug, item.project_slug);
  }
}
</script>
