import {Vue, Component} from 'vue-property-decorator';

@Component
export default class StorePermission extends Vue {
    get isLayoutRead() {
        return this.$sessionStore.permissionLayoutRead;
    }

    get isLayoutWrite() {
        return this.$sessionStore.permissionLayoutWrite;
    }

    get isStorageRead() {
        return this.$sessionStore.permissionStorageRead;
    }

    get isStorageWrite() {
        return this.$sessionStore.permissionStorageWrite;
    }

    get isManagerRead() {
        return this.$sessionStore.permissionManagerRead;
    }

    get isManagerWrite() {
        return this.$sessionStore.permissionManagerWrite;
    }

    get isGraphRead() {
        return this.$sessionStore.permissionGraphRead;
    }

    get isGraphWrite() {
        return this.$sessionStore.permissionGraphWrite;
    }

    get isMemberRead() {
        return this.$sessionStore.permissionMemberRead;
    }

    get isMemberWrite() {
        return this.$sessionStore.permissionMemberWrite;
    }

    get isSettingRead() {
        return this.$sessionStore.permissionSettingRead;
    }

    get isSettingWrite() {
        return this.$sessionStore.permissionSettingWrite;
    }
}
