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
        mainGroups: '/main/groups',
    };

    @Watch('$vuetify.lang.current')
    updateI18n(newVal: string, oldVal: string) {
        console.debug(`Update i18n: ${oldVal} -> ${newVal}`);
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

    moveToRoot() {
        this.moveTo(this.paths.root);
    }

    moveToSignup() {
        this.moveTo(this.paths.signup);
    }

    moveToSignupAdmin() {
        this.moveTo(this.paths.signupAdmin);
    }

    moveToMain() {
        this.moveTo(this.paths.main);
    }

    moveToMainDashboard() {
        this.moveTo(this.paths.mainDashboard);
    }

    moveToMainConfigAccount() {
        this.moveTo(this.paths.mainConfigAccount);
    }

    moveToMainConfigAccountAppearance() {
        this.moveTo(this.paths.mainConfigAccountAppearance);
    }

    moveToMainConfigAdmin() {
        this.moveTo(this.paths.mainConfigAdmin);
    }

    moveToMainConfigAdminOverview() {
        this.moveTo(this.paths.mainConfigAdminOverview);
    }

    moveToMainConfigAdminUsers() {
        this.moveTo(this.paths.mainConfigAdminUsers);
    }

    moveToMainConfigAdminUsersNew() {
        this.moveTo(this.paths.mainConfigAdminUsersNew);
    }

    moveToMainConfigAdminUsersEdit(username: string) {
        const prefix = this.paths.mainConfigAdminUsersEdit;
        this.moveTo(`${prefix}?username=${username}`);
    }

    moveToMainConfigAdminGroups() {
        this.moveTo(this.paths.mainConfigAdminGroups);
    }

    moveToMainConfigAdminGroupsNew() {
        this.moveTo(this.paths.mainConfigAdminGroupsNew);
    }

    moveToMainConfigAdminGroupsEdit() {
        this.moveTo(this.paths.mainConfigAdminGroupsEdit);
    }

    moveToMainConfigAdminFeatures() {
        this.moveTo(this.paths.mainConfigAdminFeatures);
    }

    moveToMainConfigAdminSettings() {
        this.moveTo(this.paths.mainConfigAdminSettings);
    }

    moveToMainConfigAdminLambdas() {
        this.moveTo(this.paths.mainConfigAdminLambdas);
    }

    moveToMainDev() {
        this.moveTo(this.paths.mainDev);
    }

    moveToMainAbout() {
        this.moveTo(this.paths.mainAbout);
    }

    moveToMainProjects() {
        this.moveTo(this.paths.mainProjects);
    }

    moveToMainProject() {
        this.moveTo(this.paths.mainProject);
    }

    moveToMainGroups() {
        this.moveTo(this.paths.mainGroups);
    }
}
