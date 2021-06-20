<template>
  <v-app>
    <v-layout align-center justify-center>
    <v-card style="padding: 15px;">
      <app-title :title="'answer'" :upperCase="true" :fontSize="35" :textShadow="'2px 2px grey'"></app-title>
      <v-card-title primary-title>
        <div style="width: 100%;" class="text-center">
          <h3>404 Not Found</h3>
          <span>페이지를 찾을 수 없습니다.</span>
        </div>
      </v-card-title>
      <v-card-actions>
        <v-btn block @click="onClickLogin" small color="success">{{ $t('goto_login') }}</v-btn>
      </v-card-actions>
    </v-card>
    </v-layout>
  </v-app>
</template>

<script>
/**
 * 404 Not Found 페이지입니다.
 * 지정된 주소 외 잘못된 주소로 접근 시 나타납니다.
 * @author zilhak, 2019-01-09
 * 
 */
export default {
  name: 'NotFound',
  methods: {
      onClickLogin: function () {
          this.$router.push('/');
      }
  }
}
</script>

<style scoped>
  .logo-style {
    left:10px;
    margin-left: 40%;
  }
  .content-style {
    text-align: center;
  }
</style>