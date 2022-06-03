module.exports = {
  transpileDependencies: ['vuetify'],
  runtimeCompiler: true,

  configureWebpack: config => {
    if (process.env.NODE_ENV !== 'production') {
      return {devtool: 'eval-source-map'};
    }
  },

  publicPath: process.env.NODE_ENV === 'production' ? '/app/' : '/',

  pluginOptions: {
    i18n: {
      locale: 'ko',
      fallbackLocale: 'ko',
      localeDir: 'locales',
      enableInSFC: true,
    },
  },

  devServer: {
    proxy: {
      '^/plugins': {
        target: 'http://localhost:20000',
        changeOrigin: true,
      },
    },
  },
};
