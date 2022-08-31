import Vue from 'vue';
import moment from 'moment-timezone';
import type {SigninA} from '@recc/api/dist/packet/user';

const DEFAULT_DARK = 0;
const DEFAULT_LANG = 'ko';
const DEFAULT_TIMEZONE = 'Asia/Seoul';

function loadApiOriginFromLocalStorage(vue: Vue) {
  const api = vue.$localStore.origin;
  console.debug(`Load api origin: ${api}`);
  vue.$api2.origin = api;
}

function getSystemDarkMode() {
  return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
}

function loadAppearanceFromUserExtraA(
  vue: Vue,
  dark: number,
  lang: string,
  timezone: string,
) {
  console.debug(`Load appearance: dark=${dark}, lang=${lang}, timezone=${timezone}`);

  if (dark) {
    if (dark === 1) {
      vue.$vuetify.theme.dark = true;
    } else if (dark === 2) {
      vue.$vuetify.theme.dark = getSystemDarkMode();
    } else {
      console.warn(`Unsupported dark mode: ${dark}`);
    }
  } else {
    vue.$vuetify.theme.dark = false;
  }

  if (vue.$vuetify.lang.current !== lang) {
    vue.$vuetify.lang.current = lang;
  }
  if (vue.$i18n.locale !== lang) {
    vue.$i18n.locale = lang;
  }
  if (moment.locale() !== lang) {
    moment.locale(lang);
  }

  if (moment.tz.guess() !== timezone) {
    moment.tz.setDefault(timezone);
  }
}

function initApiV2Session(vue: Vue, access: string, refresh: string) {
  vue.$api2.setTokens(access, refresh);
}

// ------------
// Main Process
// ------------

function loadSessionFromLocalStorage(vue: Vue) {
  let dark = vue.$localStore.userDark || DEFAULT_DARK;
  let lang = vue.$localStore.userLang || DEFAULT_LANG;
  let timezone = vue.$localStore.userTimezone || DEFAULT_TIMEZONE;

  if (vue.$localStore.alreadySession) {
    const access = vue.$localStore.access;
    const refresh = vue.$localStore.refresh;
    const userName = vue.$localStore.userName;
    const userDark = vue.$localStore.userDark;
    const userLang = vue.$localStore.userLang;
    const userTimezone = vue.$localStore.userTimezone;
    const preference = vue.$localStore.preference;
    dark = userDark;
    lang = userLang;
    timezone = userTimezone;
    console.assert(!!access);
    console.assert(!!refresh);
    console.assert(!!preference);
    console.info(`Already session information: ${userName}`);

    initApiV2Session(vue, access, refresh);
  } else {
    console.debug('Not exists session from LocalStorage');
  }

  loadApiOriginFromLocalStorage(vue);
  loadAppearanceFromUserExtraA(vue, dark, lang, timezone);
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
  vue.$localStore.clearSession();
  vue.$api2.clearTokens();
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
