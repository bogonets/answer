<i18n lang="yaml">
en:
  header: 'New group'
  subheader: >
    Groups allow you to manage and collaborate across multiple projects.
    Members of a group have access to all of its projects.

ko:
  header: '새로운 그룹'
  subheader: >
    여러 프로젝트를 관리하고 공동 작업할 수 있습니다.
    그룹의 구성원은 모든 프로젝트에 접근할 수 있습니다.
</i18n>

<template>
  <left-title :header="$t('header')" :subheader="$t('subheader')">
    <form-group
      hide-origin-prefix
      hide-cancel-button
      :hide-features="hideFeatures"
      :hide-visibility="hideVisibility"
      :loading="submitLoading"
      @cancel="cancel"
      @ok="onClickOk"
    ></form-group>
  </left-title>
</template>

<script lang="ts">
import {Component, Prop, Emit} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import LeftTitle from '@/components/LeftTitle.vue';
import FormGroup, {GroupItem} from '@/components/FormGroup.vue';
import {CreateGroupQ} from '@recc/api/dist/packet/group';

const REQUEST_TYPE_SELF = 'self';
const REQUEST_TYPE_ADMIN = 'admin';

@Component({
  components: {
    LeftTitle,
    FormGroup,
  },
})
export default class FormGroupNew extends VueBase {
  @Prop({type: Boolean})
  readonly hideFeatures!: boolean;

  @Prop({type: Boolean})
  readonly hideVisibility!: boolean;

  @Prop({type: String, default: REQUEST_TYPE_SELF})
  readonly requestType!: string;

  @Prop({type: Boolean, default: false})
  readonly hideToast!: boolean;

  submitLoading = false;

  @Emit()
  cancel() {
    // EMPTY.
  }

  @Emit('request:success')
  requestSuccess() {
    this.submitLoading = false;
    if (!this.hideToast) {
      this.toastRequestSuccess();
    }
  }

  @Emit('request:failure')
  requestFailure(error) {
    this.submitLoading = false;
    if (!this.hideToast) {
      this.toastRequestFailure(error);
    }
    return error;
  }

  onClickOk(event: GroupItem) {
    const body = {
      slug: event.slug,
      name: event.name,
      description: event.description,
      features: event.features,
      visibility: event.visibility,
    } as CreateGroupQ;

    this.submitLoading = true;
    if (this.requestType === REQUEST_TYPE_SELF) {
      this.requestPostSelfGroups(body);
    } else if (this.requestType === REQUEST_TYPE_ADMIN) {
      this.requestPostAdminGroups(body);
    } else {
      throw Error(`Unknown request type: ${this.requestType}`);
    }
  }

  requestPostAdminGroups(body: CreateGroupQ) {
    this.$api2
      .postAdminGroups(body)
      .then(() => {
        this.requestSuccess();
      })
      .catch(error => {
        this.requestFailure(error);
      });
  }

  requestPostSelfGroups(body: CreateGroupQ) {
    this.$api2
      .postMainGroups(body)
      .then(() => {
        this.requestSuccess();
      })
      .catch(error => {
        this.requestFailure(error);
      });
  }
}
</script>
