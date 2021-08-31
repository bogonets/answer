<i18n lang="yaml">
en:
  user:
    unknown: "[Unknown User]"
  overview: "Overview"
  appearance: "Appearance"

ko:
  user:
    unknown: "[알수없는 사용자]"
  overview: "개요"
  appearance: "외관"
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
          <v-avatar color="accent" size="24">{{ usernameAvatar }}</v-avatar>
        </v-list-item-icon>
        <v-list-item-title>
          {{ username }}
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

        <v-list-item link @click.stop="overview">
          <v-list-item-icon>
            <v-icon>mdi-developer-board</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('overview') }}
          </v-list-item-title>
        </v-list-item>

        <v-list-item link @click.stop="appearance">
          <v-list-item-icon>
            <v-icon>mdi-eye</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('appearance') }}
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

  @Prop({type: Number, default: 0})
  readonly value!: number;

  mini = false;

  get username(): string {
    const username = this.$localStore.user.username;
    if (username) {
      return username;
    }
    return this.$t('user.unknown').toString();
  }

  get usernameAvatar(): string {
    return this.username[0].toUpperCase();
  }

  onClickFoldNavigation() {
    this.mini = !this.mini;
  }

  @Emit()
  input(index: number) {
    return index;
  }

  @Emit('click:overview')
  overview() {
    if (!this.noDefault) {
      this.moveToSelf();
    }
  }

  @Emit('click:appearance')
  appearance() {
    if (!this.noDefault) {
      this.moveToSelfAppearance();
    }
  }
}
</script>