import theme_default from './theme_default.js'
import theme_test from './theme_test.js'

function install(Vue) {
  Vue.prototype.getThemeList = getThemeList;
  Vue.prototype.applyTheme = applyTheme;
}

export default install;

function getThemeList() {
  let result = new Map();

  /***** Theme List *****/

  result.set('default', theme_default)
  result.set('test', theme_test)

  /*** Theme List End ***/

  return result;
}

function applyTheme(theme_name, vuetify_theme) {
  let theme = getThemeList().get(theme_name)
  let variable;
  if (theme == null || theme == undefined) {
    if (localStorage.theme == undefined) {
      localStorage.theme = 'default'
      for (variable in theme_default) {
        vuetify_theme[variable] = theme_default[variable];
      }
    } else {
      let theme_storage = getThemeList().get(theme_name)
      if (theme_storage == undefined) {
        localStorage.theme = 'default'
        for (variable in theme_default) {
          vuetify_theme[variable] = theme_default[variable];
        }
      } else {
        localStorage.theme = theme_name;
        for (variable in theme_storage) {
          vuetify_theme[variable] = theme_storage[variable];
        }
      }
    }
  } else {
    for (variable in theme) {
      vuetify_theme[variable] = theme[variable];
    }
  }
}