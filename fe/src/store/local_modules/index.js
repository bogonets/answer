const files = require.context('.', false, /\.js$/)
const local_modules = {}

files.keys().forEach(key => {
    if (key === './index.js') return
    local_modules[key.replace(/(\.\/|\.js)/g, '')] = files(key).default
})

export default local_modules