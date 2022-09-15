<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <p :class="subtitleClass">
          클라우드 또는 데이터베이스 저장소를 레이블 지정 작업의 소스 또는 완료된 주석의
          대상으로 사용합니다.
        </p>
      </v-col>

      <v-col cols="6">
        <p :class="titleClass">원본 저장소</p>
        <v-btn @click="onClickAddInfo">원본 저장소 설정</v-btn>

        <v-card class="mt-4">
          <v-card-subtitle>
            <p>
              Type: AWS S3
              <br />
              Address: 192.168.0.100:8080
              <br />
              Bucket: Source
              <br />
              Path: /Downloads/images
              <br />
              Filter: .*\.jpg
              <br />
              Last Sync: May 16, 2022 ∙ 10:25:26
            </p>
          </v-card-subtitle>
          <v-card-actions>
            <v-btn>Sync Storage</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>

      <v-col cols="6">
        <p :class="titleClass">결과 저장소</p>
        <v-btn @click="onClickAddInfo">결과 저장소 설정</v-btn>

        <v-card class="mt-4">
          <v-card-subtitle>
            <p>
              Type: FTP
              <br />
              Address: 192.168.0.8:20
              <br />
              Path: /latest/labels
              <br />
              Last Sync: May 16, 2022 ∙ 10:25:27
            </p>
          </v-card-subtitle>
          <v-card-actions>
            <v-btn>Sync Storage</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <v-dialog
      v-model="showAddInfoDialog"
      persistent
      max-width="560px"
      no-click-animation
      @keydown.esc.stop="onClickAddInfoCancel"
    >
      <v-card>
        <v-card-title class="mb-1">저장소 연결</v-card-title>
        <v-card-subtitle>저장소 연결을 위한 정보를 입력합니다.</v-card-subtitle>

        <v-divider></v-divider>

        <v-container>
          <v-form ref="form" lazy-validation>
            <v-list flat>
              <v-list-item>
                <v-select
                  dense
                  outlined
                  :items="['AWS S3', 'GDrive', 'WebDAV', 'SMB', 'NFS', 'FTP', 'Server']"
                  value="AWS S3"
                  hide-details
                ></v-select>
              </v-list-item>

              <v-list-item>
                <v-text-field
                  label="Title"
                  hint="화면에 출력될 저장소 이름"
                  persistent-hint
                ></v-text-field>
              </v-list-item>

              <v-list-item>
                <v-text-field
                  label="Address"
                  hint="S3 Endpoint Address"
                  persistent-hint
                ></v-text-field>
              </v-list-item>

              <v-list-item>
                <v-text-field
                  label="Bucket Name"
                  hint="저장될 S3 버킷 이름"
                  persistent-hint
                ></v-text-field>
              </v-list-item>

              <v-list-item>
                <v-text-field
                  label="Path"
                  hint="작업 경로"
                  persistent-hint
                ></v-text-field>
              </v-list-item>

              <v-list-item>
                <v-text-field
                  label="File Filter Regex"
                  hint="필터링을 위한 정규표현식"
                  persistent-hint
                ></v-text-field>
              </v-list-item>

              <v-list-item>
                <v-text-field
                  label="Access Key ID"
                  hint="S3 에 접속하기 위한 아이디"
                  persistent-hint
                ></v-text-field>
              </v-list-item>

              <v-list-item>
                <v-text-field
                  label="Secret Access Key"
                  hint="S3 에 접속하기 위한 비밀번호"
                  persistent-hint
                ></v-text-field>
              </v-list-item>

              <v-list-item>
                <v-switch hide-details dense inset label="Recursive scan"></v-switch>
              </v-list-item>
            </v-list>
          </v-form>
        </v-container>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="second" class="mr-1">
            <v-icon left>mdi-sync</v-icon>
            Sync
          </v-btn>
          <v-btn color="second" class="mr-1" @click="onClickAddInfoCancel">
            Cancel
          </v-btn>
          <v-btn color="primary" @click="onClickAddInfoOk">Submit</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import {TITLE_CLASS} from '@/styles/title';
import {SUBTITLE_CLASS} from '@/styles/subtitle';

@Component
export default class MainStorage extends VueBase {
  private readonly titleClass = TITLE_CLASS;
  private readonly subtitleClass = SUBTITLE_CLASS;

  showAddInfoDialog = false;

  onClickAddInfo() {
    this.showAddInfoDialog = true;
  }

  onClickAddInfoCancel() {
    this.showAddInfoDialog = false;
  }

  onClickAddInfoOk(event) {
    // EMPTY.
  }
}
</script>
