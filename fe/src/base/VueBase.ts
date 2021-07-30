import { Vue, Watch } from 'vue-property-decorator';
import { RawLocation } from 'vue-router';

export default class VueBase extends Vue {

    readonly paths = {
        root: '/',
        signup: '/signup',
        signupAdmin: '/signup/admin',
        main: '/main',
        mainDashboard: '/main/dashboard',
        mainConfigAccount: '/main/config/account',
        mainConfigAccountAppearance: '/main/config/account/appearance',
        mainConfigAdmin: '/main/config/admin',
        mainConfigAdminOverview: '/main/config/admin/overview',
        mainConfigAdminUsers: '/main/config/admin/users',
        mainConfigAdminUsersNew: '/main/config/admin/users/new',
        mainConfigAdminUsersEdit: '/main/config/admin/users/edit',
        mainConfigAdminGroups: '/main/config/admin/groups',
        mainConfigAdminGroupsNew: '/main/config/admin/groups/new',
        mainConfigAdminGroupsEdit: '/main/config/admin/groups/edit',
        mainConfigAdminFeatures: '/main/config/admin/features',
        mainConfigAdminSettings: '/main/config/admin/settings',
        mainConfigAdminLambdas: '/main/config/admin/lambdas',
        mainDev: '/main/dev',
        mainAbout: '/main/about',
        mainProjects: '/main/projects',
        mainProject: '/main/project',
    };

    @Watch('$vuetify.lang.current')
    updateI18n(newVal: string, oldVal: string) {
        this.$i18n.locale = newVal;
    }

    get currentRoutePath(): string {
        return this.$router.currentRoute.path;
    }

    moveTo(location: RawLocation) {
        if (this.$router.currentRoute.path === location.toString()) {
            return;
        }

        this.$router.push(location).catch((reason: any) => {
            if (reason.name !== 'NavigationDuplicated') {
                throw reason;
            }
        })
    }

    moveToMainPage() {
        this.moveTo(this.paths.main);
    }

    moveToSignUpPage() {
        this.moveTo(this.paths.signup);
    }

    moveToSignUpAdminPage() {
        this.moveTo(this.paths.signupAdmin);
    }

    moveToUsersEditPage(username: string) {
        const prefix = this.paths.mainConfigAdminUsersEdit;
        this.moveTo(`${prefix}?username=${username}`);
    }
}
