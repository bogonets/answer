<template>
  <div class="main">
    <v-container class="container" fluid>
      <v-card-title>{{ $t("project_member") }}</v-card-title>
      <v-card>
        <v-card-title>{{ $t("add_member") }}</v-card-title>
        <label class="mx-4">ID</label>
        <v-autocomplete
          prepend-inner-icon="fas fa-search"
          outlined
          dense
          class="mx-4 mt-2"
          v-model="addId"
          :items="projectIds"
        ></v-autocomplete>
        <label class="mx-4">{{ $t("authentication") }}</label>
        <v-select
          v-model="addAuth[$vuetify.lang.current]"
          :items="auths"
          outlined
          dense
          :item-text="$vuetify.lang.current"
          class="mx-4 mt-2"
        ></v-select>
        <v-card-actions>
          <v-btn :disabled="isProjectId()" @click="addProjectMember()">
            {{ $t("add") }}
          </v-btn>
        </v-card-actions>
      </v-card>
      <v-card class="mt-4">
        <v-card-title>{{ $t("member_list") }}</v-card-title>
        <v-list flat>
          <v-subheader>
            {{ projectName }} {{ $t("project_member") }}
            <v-spacer></v-spacer>
            <v-autocomplete
              prepend-inner-icon="fas fa-search"
              hide-details
              dense
              outlined
              v-model="searchMemberId"
              :items="projectMembers"
              item-text="id"
              clearable
            >
            </v-autocomplete>
          </v-subheader>
          <v-list-item
            v-for="member in projectMembers"
            :key="member.id"
            class="blue-box"
            v-show="isSearchId(member.id, searchMemberId)"
          >
            <v-list-item-title class="mx-2">
              <v-icon>fas fa-user-circle</v-icon>
              {{ member.id }}
            </v-list-item-title>
            <v-list-item-subtitle>
              <v-spacer></v-spacer>
              <v-select
                dense
                outlined
                hide-details
                v-model="member.auth[$vuetify.lang.current]"
                :items="auths"
                :item-text="$vuetify.lang.current"
                v-on:change="editMemberAuth(member.id, member.auth)"
              ></v-select>
            </v-list-item-subtitle>
            <v-list-item-action>
              <v-btn icon class="mr-6" @click="deleteProjectMember(member.id)">
                <v-icon>fas fa-trash-alt</v-icon>
              </v-btn>
            </v-list-item-action>
          </v-list-item>
        </v-list>
      </v-card>
    </v-container>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import axios from "axios";

@Component
export default class AuthManagement extends Vue {
  private BASE_URL = this.$api.getUrl();
  private TIMEOUT = 3000;

  private projectName = this.$store.getters["project/getSelectProject"];
  private auths = [
    { ko: "관리자", en: "administrator" },
    { ko: "부관리자", en: "operator" },
    { ko: "게스트", en: "guest" },
  ]; 
  
  private projectIds = [];
  private projectMembers = Array();
  private searchMemberId = "";

  private addId = "";
  private addAuth = { ko: "게스트", en: "guest" };

  created() {
  }

  mounted() {
    this.getProjectIds();
    this.getProjectMembers();
  }

  isSearchId(list, id) {
    if (list) {
      if (id) {
        return list.includes(id);
      } else {
        return true;
      }
    }
  }

  isProjectId() {
    if (this.addId.length > 0) return false;
    return true;
  }

  searchProjectMembers() {
    if (this.searchMemberId != null && this.searchMemberId.length > 0) {
    } else {
      return this.projectMembers;
    }
  }

  // api
  async getProjectIds() {
    const projectName = this.$store.getters["project/getSelectProject"];
    const url = `/api/v1/extra/airjoy/project/${projectName}/ids`;
    const access = this.$store.getters["user/getAccessToken"];
    const instance = axios.create({
      baseURL: this.BASE_URL,
      timeout: this.TIMEOUT,
      headers: { Authorization: "Bearer " + access },
    });

    var result = await instance.get(url).then((response) => {
      return response.data.result;
    });

    this.projectIds = result;
  }

  async getProjectMembers() {
    const projectName = this.$store.getters["project/getSelectProject"];
    const url = `/api/v1/extra/airjoy/project/${projectName}/members`;
    const access = this.$store.getters["user/getAccessToken"];
    const instance = axios.create({
      baseURL: this.BASE_URL,
      timeout: this.TIMEOUT,
      headers: { Authorization: "Bearer " + access },
    });

    var result = await instance.get(url).then((response) => {
      return response.data.result;
    });
    this.projectMembers = result;
    this.searchProjectMembers = result;
  }

  async addProjectMember() {
    const projectName = this.$store.getters["project/getSelectProject"];
    const url = `/api/v1/extra/airjoy/project/${projectName}/member/add`;
    const access = this.$store.getters["user/getAccessToken"];
    const instance = axios.create({
      baseURL: this.BASE_URL,
      timeout: this.TIMEOUT,
      headers: { Authorization: "Bearer " + access },
    });

    var data = {
      id: this.addId,
      auth: this.addAuth,
    };

    var result = await instance.post(url, data).then((response) => {
      return response.data.result;
    });
  }

  async editMemberAuth(id: string, auth: string) {
    const projectName = this.$store.getters["project/getSelectProject"];
    const url = `/api/v1/extra/airjoy/project/${projectName}/member/auth/edit`;
    const access = this.$store.getters["user/getAccessToken"];
    const instance = axios.create({
      baseURL: this.BASE_URL,
      timeout: this.TIMEOUT,
      headers: { Authorization: "Bearer " + access },
    });

    var data = {
      id: id,
      auth: auth,
    };

    var result = await instance.post(url, data).then((response) => {
      return response.data.result;
    });
  }

  async deleteProjectMember(id: string) {
    const projectName = this.$store.getters["project/getSelectProject"];
    const url = `/api/v1/extra/airjoy/project/${projectName}/member/delete`;
    const access = this.$store.getters["user/getAccessToken"];
    const instance = axios.create({
      baseURL: this.BASE_URL,
      timeout: this.TIMEOUT,
      headers: { Authorization: "Bearer " + access },
    });

    var data = {
      id: id,
    };

    var result = await instance.post(url, data).then((response) => {
      return response.data.result;
    });
  }
}
</script>

<style scoped>
.main {
  height: 100%;
  padding: 10px 10px 10px 10px;
}
.container {
  height: 100%;
  padding: 10px 10px 10px 10px;
  background-color: rgba(125, 125, 125, 0.2);
}
/* .blue-box {
  border: 1px solid blue;
} */
</style>
