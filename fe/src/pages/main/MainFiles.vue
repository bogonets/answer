<i18n lang="yaml">
en:
  tools:
    copy: 'Copy'
    cut: 'Cut'
    paste: 'Paste'
  msg:
    empty: 'Unselected files.'

ko:
  tools:
    copy: '복사'
    cut: '잘라내기'
    paste: '붙여넣기'
  msg:
    empty: '선택한 파일이 없습니다.'
</i18n>

<template>
  <div>
    <v-toolbar dense flat>
      <v-spacer></v-spacer>
      <v-btn icon small @click="onClickCopy">
        <v-icon>mdi-content-copy</v-icon>
      </v-btn>
      <v-btn icon small @click="onClickCut">
        <v-icon>mdi-content-cut</v-icon>
      </v-btn>
      <v-btn icon small @click="onClickPaste">
        <v-icon>mdi-content-paste</v-icon>
      </v-btn>
      <v-btn icon small @click="onClickRename">
        <v-icon>mdi-rename-box</v-icon>
      </v-btn>
      <v-btn icon small @click="onClickUpload">
        <v-icon>mdi-upload</v-icon>
      </v-btn>
      <v-btn icon small @click="onClickDownload">
        <v-icon>mdi-download</v-icon>
      </v-btn>
      <v-btn icon small @click="onClickSync">
        <v-icon>mdi-sync</v-icon>
      </v-btn>
    </v-toolbar>
    <v-divider></v-divider>

    <v-row no-gutters>
      <v-col cols="12" sm="4">
        <v-treeview
          dense
          v-model="tree"
          :open="initiallyOpen"
          :items="items"
          activatable
          item-key="name"
          open-on-click
        >
          <template v-slot:prepend="{item, open}">
            <v-icon v-if="!item.file">
              {{ open ? 'mdi-folder-open' : 'mdi-folder' }}
            </v-icon>
            <v-icon v-else>
              {{ icons[item.file] }}
            </v-icon>
          </template>
        </v-treeview>
      </v-col>

      <v-divider vertical></v-divider>

      <v-col cols="0" sm="8">
        <view-port v-if="true" class="d-flex flex-row align-center justify-center">
          <div class="d-flex flex-column align-center justify-center">
            <v-icon x-large>mdi-file</v-icon>
            <span class="text--secondary text-subtitle-2">
              {{ $t('msg.empty') }}
            </span>
          </div>
        </view-port>

        <view-port v-if="false" class="d-flex flex-row">
          <v-container class="pa-1">
            <v-item-group v-model="selected" multiple>
              <v-row>
                <v-col v-for="(item, i) in files" :key="i" cols="12" md="6">
                  <v-item v-slot="{active, toggle}">
                    <v-img
                      class="text-right pa-2"
                      height="150"
                      :src="item.src"
                      @click="toggle"
                    >
                      <v-btn icon dark>
                        <v-icon>
                          {{
                            active
                              ? 'mdi-checkbox-marked'
                              : 'mdi-checkbox-blank-outline'
                          }}
                        </v-icon>
                      </v-btn>
                    </v-img>
                  </v-item>
                  <span class="d-block ma-1 text-center text--primary text-body-2">
                    {{ item.name }}
                  </span>
                </v-col>
              </v-row>
            </v-item-group>
          </v-container>
        </view-port>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ViewPort from '@/components/ViewPort.vue';

@Component({
  components: {
    ViewPort,
  },
})
export default class MainFiles extends VueBase {
  readonly icons = {
    html: 'mdi-language-html5',
    js: 'mdi-nodejs',
    json: 'mdi-code-json',
    md: 'mdi-language-markdown',
    pdf: 'mdi-file-pdf',
    png: 'mdi-file-image',
    txt: 'mdi-file-document-outline',
    xls: 'mdi-file-excel',
  };

  selected = [];
  files = [
    // {
    //   src: require('@/assets/temp/image38.jpeg'),
    //   name: 'image38.jpeg',
    // },
    // {
    //   src: require('@/assets/temp/image41.jpeg'),
    //   name: 'image41.jpeg',
    // },
    // {
    //   src: require('@/assets/temp/image42.jpeg'),
    //   name: 'image42.jpeg',
    // },
    // {
    //   src: require('@/assets/temp/image45.jpeg'),
    //   name: 'image45.jpeg',
    // },
    // {
    //   src: require('@/assets/temp/image46.jpeg'),
    //   name: 'image46.jpeg',
    // },
  ];

  cwd = '';
  initiallyOpen = [''];
  tree = [];
  items = [
    {
      name: '.git',
    },
    {
      name: 'node_modules',
    },
    {
      name: 'public',
      children: [
        {
          name: 'static',
          children: [
            {
              name: 'logo.png',
              file: 'png',
            },
          ],
        },
        {
          name: 'favicon.ico',
          file: 'png',
        },
        {
          name: 'index.html',
          file: 'html',
        },
      ],
    },
    {
      name: '.gitignore',
      file: 'txt',
    },
    {
      name: 'babel.config.js',
      file: 'js',
    },
    {
      name: 'package.json',
      file: 'json',
    },
    {
      name: 'README.md',
      file: 'md',
    },
    {
      name: 'vue.config.js',
      file: 'js',
    },
    {
      name: 'yarn.lock',
      file: 'txt',
    },
  ];

  miniNavigation = false;

  onClickFoldNavigation() {
    this.miniNavigation = !this.miniNavigation;
  }

  onClickCopy() {}

  onClickCut() {}

  onClickPaste() {}

  onClickRename() {}

  onClickUpload() {}

  onClickDownload() {}

  onClickSync() {}
}
</script>
