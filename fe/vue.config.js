module.exports = {
  transpileDependencies: ["vuetify"],
  runtimeCompiler: true,
  configureWebpack: config => {
    if (process.env.NODE_ENV !== "production") {
      return { devtool: "source-map" };
    }
  }
};
