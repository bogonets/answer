<template>
	<div class="projectsMain" :style="this.$backgroundColor()">
		<!-- <a-project-table :showPrivate="true" :showDescription="true"></a-project-table> -->
		<a-project-table></a-project-table>
	</div>
</template>

<script>
import aProjectTable from "@/components/Table/aProjectTable.vue";
export default {
	props:{

	},
	components:{
		aProjectTable
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
.projectsMain {
	height: 100%;
}
</style>