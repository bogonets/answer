<i18n lang="yaml">
en:
  group:
    unknown: "[Unknown Group]"
  projects: "Projects"
  members: "Members"
  settings: "Settings"

ko:
  group:
    unknown: "[알수없는 그룹]"
  projects: "프로젝트"
  members: "회원 관리"
  settings: "그룹 설정"
</i18n>

<template>
  <v-navigation-drawer
      app
      clipped
      permanent
      stateless
      touchless
      :mini-variant.sync="mini"
  >
    <v-list nav dense>

      <!-- User Profile -->
      <v-list-item link @click.stop="onClickFoldNavigation">
        <v-list-item-icon>
          <v-avatar color="accent" size="24">{{ groupAvatar }}</v-avatar>
        </v-list-item-icon>
        <v-list-item-title>
          {{ groupSlug }}
        </v-list-item-title>
        <v-btn icon @click.stop="onClickFoldNavigation">
          <v-icon>mdi-chevron-left</v-icon>
        </v-btn>
      </v-list-item>

      <v-divider></v-divider>

      <v-list-item-group
          mandatory
          color="primary"
          :value="value"
          @change="input"
      >

        <v-list-item link @click.stop="projects">
          <v-list-item-icon>
            <v-icon>mdi-clipboard-check-multiple</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('projects') }}
          </v-list-item-title>
        </v-list-item>

        <v-list-item v-if="!hideMembers" link @click.stop="members">
          <v-list-item-icon>
            <v-icon>mdi-account-group</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('members') }}
          </v-list-item-title>
        </v-list-item>

        <v-list-item v-if="!hideSettings" link @click.stop="settings">
          <v-list-item-icon>
            <v-icon>mdi-cogs</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('settings') }}
          </v-list-item-title>
        </v-list-item>

      </v-list-item-group>
    </v-list>
  </v-navigation-drawer>
</template>

<script lang="ts">
import {Component, Emit, Prop} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';

@Component
export default class MainAccount extends VueBase {

  @Prop({type: Boolean, default: false})
  readonly noDefault!: boolean;

  @Prop({type: Boolean, default: false})
  readonly hideMembers!: boolean;

  @Prop({type: Boolean, default: false})
  readonly hideSettings!: boolean;

  @Prop({type: Number, default: 0})
  readonly value!: number;

  mini = false;

  get groupSlug(): string {
    const name = this.$route.params.group;
    if (name) {
      return name;
    }
    return this.$t('group.unknown').toString();
  }

  get groupAvatar(): string {
    // return this.groupSlug[0].toUpperCase();
    const name = this.$route.params.group;
    if (name) {
      return name[0].toUpperCase();
    }
    return '?';
  }

  mounted() {
    console.log(`this.$route.params.group: ${this.$route.params.group}`);
  }

  onClickFoldNavigation() {
    this.mini = !this.mini;
  }

  @Emit()
  input(index: number) {
    return index;
  }

  @Emit('click:projects')
  projects() {
    if (!this.noDefault) {
      this.moveToGroup(this.$route.params.group);
    }
  }

  @Emit('click:members')
  members() {
    if (!this.noDefault) {
      this.moveToGroupMembers(this.$route.params.group);
    }
  }

  @Emit('click:settings')
  settings() {
    if (!this.noDefault) {
      this.moveToGroupSettings(this.$route.params.group);
    }
  }
}
</script>
