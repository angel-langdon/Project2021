const withImages = require("next-images");
module.exports = withImages({
  basePath: "/project2021-costomize",
  webpack(config, options) {
    return config;
  },
});
