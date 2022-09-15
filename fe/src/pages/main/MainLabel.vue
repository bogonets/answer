<template>
  <div>
    <v-navigation-drawer
      right
      app
      clipped
      permanent
      stateless
      touchless
      :mini-variant.sync="miniWidgets"
    >
      <v-list nav dense>
        <v-list-item link @click.stop="onClickFoldNavigation">
          <v-list-item-icon>
            <v-icon>mdi-toolbox</v-icon>
          </v-list-item-icon>
          <v-list-item-title>도구 모음</v-list-item-title>
          <v-btn icon @click.stop="onClickFoldNavigation">
            <v-icon>mdi-chevron-right</v-icon>
          </v-btn>
        </v-list-item>
        <v-divider></v-divider>
      </v-list>

      <v-expansion-panels class="pl-1" v-model="panels" multiple accordion flat>
        <v-expansion-panel>
          <v-expansion-panel-header>범주 (5)</v-expansion-panel-header>
          <v-expansion-panel-content>
            <v-list dense>
              <v-list-item link v-for="category in categories" :key="category.id">
                <v-list-item-icon>
                  <v-icon dense>
                    {{ category.active ? 'mdi-radiobox-marked' : 'mdi-radiobox-blank' }}
                  </v-icon>
                </v-list-item-icon>
                <v-list-item-title>
                  <v-chip small :color="category.color">{{ category.name }}</v-chip>
                </v-list-item-title>
              </v-list-item>
            </v-list>
          </v-expansion-panel-content>
          <v-divider></v-divider>
        </v-expansion-panel>

        <v-expansion-panel>
          <v-expansion-panel-header>라벨 (2)</v-expansion-panel-header>
          <v-expansion-panel-content>
            <v-list dense class="pr-2">
              <v-list-item link>
                <v-list-item-icon>
                  <v-icon>mdi-checkbox-outline</v-icon>
                </v-list-item-icon>
                <v-list-item-title>
                  <v-chip small color="#E1E1E1">Car</v-chip>
                </v-list-item-title>
                <v-list-item-icon>
                  <v-icon class="mr-1" dense>mdi-vector-polygon</v-icon>
                  <v-icon class="mr-1" dense>mdi-eye</v-icon>
                  <v-icon class="mr-1" dense>mdi-delete</v-icon>
                </v-list-item-icon>
              </v-list-item>

              <v-list-item link>
                <v-list-item-icon>
                  <v-icon>mdi-checkbox-blank-outline</v-icon>
                </v-list-item-icon>
                <v-list-item-title>
                  <v-chip small color="#E1E1E1">Car</v-chip>
                </v-list-item-title>
                <v-list-item-icon>
                  <v-icon class="mr-1" dense>mdi-vector-polygon</v-icon>
                  <v-icon class="mr-1" dense>mdi-eye-off</v-icon>
                  <v-icon class="mr-1" dense>mdi-delete</v-icon>
                </v-list-item-icon>
              </v-list-item>
            </v-list>
          </v-expansion-panel-content>
          <v-divider></v-divider>
        </v-expansion-panel>

        <v-expansion-panel>
          <v-expansion-panel-header>추론 (4)</v-expansion-panel-header>
          <v-expansion-panel-content>
            <v-img
              src="https://www.retouchingvisuals.com/wp-content/uploads/2022/02/Semantic-segmentation-deep-learning.jpg"
            ></v-img>
          </v-expansion-panel-content>
          <v-divider></v-divider>
        </v-expansion-panel>
      </v-expansion-panels>
    </v-navigation-drawer>

    <v-toolbar dense flat>
      <v-btn plain x-small @click="onClickLayouts">
        <v-icon small>mdi-close-circle</v-icon>
      </v-btn>

      <v-btn plain x-small @click="onClickLayouts">
        <v-icon small>mdi-skip-previous</v-icon>
      </v-btn>

      <v-btn plain x-small @click="onClickLayouts">59/100</v-btn>

      <v-btn plain x-small @click="onClickLayouts">
        <v-icon small>mdi-skip-next</v-icon>
      </v-btn>

      <v-divider class="mx-3" vertical></v-divider>

      <v-btn plain x-small @click="onClickLayouts">
        <v-icon small>mdi-content-save</v-icon>
      </v-btn>

      <v-btn plain x-small @click="onClickLayouts">
        <v-icon small>mdi-refresh</v-icon>
      </v-btn>

      <v-divider class="mx-3" vertical></v-divider>

      <v-btn plain x-small @click="onClickLayouts">
        <v-icon small>mdi-cursor-default</v-icon>
      </v-btn>

      <v-btn plain x-small @click="onClickLayouts">
        <v-icon small>mdi-cursor-move</v-icon>
      </v-btn>

      <v-btn plain x-small @click="onClickLayouts">
        <v-icon small>mdi-magnify-plus</v-icon>
      </v-btn>

      <v-btn plain x-small @click="onClickLayouts">
        <v-icon small>mdi-magnify-minus</v-icon>
      </v-btn>

      <v-divider class="mx-3" vertical></v-divider>

      <v-btn plain x-small @click="onClickLayouts">
        <v-icon small>mdi-undo</v-icon>
      </v-btn>

      <v-btn plain x-small @click="onClickLayouts">
        <v-icon small>mdi-redo</v-icon>
      </v-btn>

      <v-divider class="mx-3" vertical></v-divider>

      <v-btn plain x-small @click="onClickLayouts">
        <v-icon small>mdi-vector-polyline</v-icon>
      </v-btn>

      <v-btn plain x-small @click="onClickLayouts">
        <v-icon small>mdi-vector-polygon</v-icon>
      </v-btn>

      <v-btn plain x-small @click="onClickLayouts">
        <v-icon small>mdi-vector-ellipse</v-icon>
      </v-btn>

      <v-divider class="mx-3" vertical></v-divider>

      <v-btn plain x-small @click="onClickLayouts">
        <v-icon small>mdi-image-search</v-icon>
      </v-btn>

      <v-divider class="mx-3" vertical></v-divider>

      <v-btn icon plain small @click="onClickMore">
        <v-icon small>mdi-dots-horizontal</v-icon>
      </v-btn>
    </v-toolbar>
    <v-divider></v-divider>
    <v-progress-linear height="2" value="59"></v-progress-linear>

    <v-alert class="ma-2" dense border="left" type="warning">
      현재, '빛바랜 자'님 께서 작업중 입니다.
    </v-alert>

    <view-port class="d-flex flex-row align-center justify-center">
      <div class="d-flex flex-column align-center justify-center">
        <v-img
          src="https://www.retouchingvisuals.com/wp-content/uploads/2022/02/Semantic-segmentation-deep-learning-b.jpg"
        ></v-img>
      </div>
    </view-port>
  </div>
</template>

<script lang="ts">
import {Component, Ref} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ViewPort from '@/components/ViewPort.vue';

@Component({
  components: {
    ViewPort,
  },
})
export default class MainLabel extends VueBase {
  @Ref()
  readonly root!: HTMLDivElement;

  categories = [
    {
      id: '0',
      name: 'Fire',
      super: 'Fire',
      active: false,
      color: '#FF0000',
    },
    {
      id: '1',
      name: 'Smoke',
      super: 'Fire',
      active: false,
      color: '#808080',
    },
    {
      id: '2',
      name: 'Car',
      super: undefined,
      active: true,
      color: '#E1E1E1',
    },
    {
      id: '3',
      name: 'Bus',
      super: 'Car',
      active: false,
      color: '#8888FF',
    },
    {
      id: '4',
      name: 'Truck',
      super: 'Car',
      active: false,
      color: '#FFBB11',
    },
  ];

  miniWidgets = false;
  panels = [0, 1, 2];

  mounted() {}

  onClickFoldNavigation() {
    this.miniWidgets = !this.miniWidgets;
  }

  onClickLayouts() {}

  onClickMore() {}
}
</script>
