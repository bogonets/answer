<template>
  <v-content>
			<v-container fluid fill-height>
				<v-layout align-center justify-center>
					<v-flex xs12 sm8 md6>
            <v-signup-admin></v-signup-admin>
					</v-flex>
				</v-layout>
			</v-container>
</v-content>
</template>

<script>
import vSignupAdmin from "@/components/Form/afSignupAdmin.vue"
// import vSignupAdmin from "@/components/Form/test/SignupAdminTest.vue"

export default {
  props:{

  },
  components:{
    vSignupAdmin
  },
  data(){
    return {

    }
  },
  computed:{

  },
  methods:{

  },
  created(){

  },
  mounted(){

  }
}
</script>

<style scoped>

</style>