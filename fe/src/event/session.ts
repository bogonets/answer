import Vue from 'vue';
import moment from 'moment-timezone';
import type {SigninA, UserA, UserExtraA} from '@/packet/user';
import type {PreferenceA} from '@/packet/preference';

function loadApiOriginFromLocalStorage(vue: Vue) {
    const api = vue.$localStore.origin;
    console.debug(`Load api origin: ${api}`);
    vue.$api2.origin = api;
}

function loadAppearanceFromUserExtraA(vue: Vue, extra: UserExtraA) {
    const dark = extra.dark;
    const lang = extra.lang;
    const timezone = extra.timezone;
    console.debug(`Load appearance: dark=${dark}, lang=${lang}, timezone=${timezone}`);

    if (typeof dark !== 'undefined') {
        if (vue.$vuetify.theme.dark !== dark) {
            vue.$vuetify.theme.dark = dark;
        }
    }

    if (typeof lang !== 'undefined') {
        if (vue.$vuetify.lang.current !== lang) {
            vue.$vuetify.lang.current = lang;
        }
        if (vue.$i18n.locale !== lang) {
            vue.$i18n.locale = lang;
        }
        if (moment.locale() !== lang) {
            moment.locale(lang);
        }
    }

    if (typeof timezone !== 'undefined') {
        if (moment.tz.guess() !== timezone) {
            moment.tz.setDefault(timezone);
        }
    }
}

function getUserExtraFromLocalStorage(vue: Vue) {
    return {
        dark: vue.$localStore.dark,
        lang: vue.$localStore.lang,
        timezone: vue.$localStore.timezone,
    } as UserExtraA;
}

function initApiV1Session(
    vue: Vue,
    access: string,
    refresh: string,
    user: UserA,
) {
    vue.$store.commit('user/login', {
        accessToken: access,
        refreshToken: refresh,
        id: user.username || '',
        email: user.email || '',
        phone: user.phone1 || '',
    });
}

function initApiV2Session(
    vue: Vue,
    access: string,
    refresh: string,
    user: UserA,
    preference: PreferenceA,
) {
    vue.$api2.setDefaultSession(access, refresh, user, preference);
}

// ------------
// Main Process
// ------------

function loadSessionFromLocalStorage(vue: Vue) {
    const userExtra = getUserExtraFromLocalStorage(vue);
    if (vue.$localStore.alreadySession) {
        const access = vue.$localStore.access;
        const refresh = vue.$localStore.refresh;
        const user = vue.$localStore.user;
        const preference = vue.$localStore.preference;
        console.assert(!!access);
        console.assert(!!refresh);
        console.assert(!!user);
        console.assert(!!user.username);
        console.assert(!!preference);
        console.info(`Already session information: ${user.username}`)

        initApiV1Session(vue, access, refresh, user);
        initApiV2Session(vue, access, refresh, user, preference);

        if (user.extra) {
            if (user.extra.dark) {
                userExtra.dark = user.extra.dark;
            }
            if (user.extra.lang) {
                userExtra.lang = user.extra.lang;
            }
            if (user.extra.timezone) {
                userExtra.timezone = user.extra.timezone;
            }
        } else {
            console.debug('Not exists user\'s extra');
        }
    } else {
        console.debug('Not exists session from LocalStorage');
    }

    loadApiOriginFromLocalStorage(vue);
    loadAppearanceFromUserExtraA(vue, userExtra);
}

function saveSessionToLocalStorage(vue: Vue, signin: SigninA) {
    const access = signin.access;
    const refresh = signin.refresh;
    const user = signin.user;
    const preference = signin.preference;
    console.assert(!!access);
    console.assert(!!refresh);
    console.assert(!!user);
    console.assert(!!preference);

    vue.$localStore.access = access;
    vue.$localStore.refresh = refresh;
    vue.$localStore.user = user;
    vue.$localStore.preference = preference;
}

function clearSessionInLocalStorage(vue: Vue) {
    vue.$store.commit('user/logout');
    vue.$localStore.clearSession();
    vue.$api2.clearDefaultSession();
}

// -------------
// Export events
// -------------

export function onCreateApplicationEvent(vue: Vue) {
    console.debug('[EVENT] Create Application');
    loadSessionFromLocalStorage(vue);
}

export function onSigninEvent(vue: Vue, signin: SigninA) {
    console.debug('[EVENT] Sign In');
    saveSessionToLocalStorage(vue, signin);
    loadSessionFromLocalStorage(vue);
}

export function onSignoutEvent(vue: Vue) {
    console.debug('[EVENT] Sign Out');
    clearSessionInLocalStorage(vue);
}
