const TITLE = "Answer Docs."
const BUILD_DIR = "docs";
module.exports = {
    // set your styleguidist configuration here
    styleguideDir: BUILD_DIR,
    title: TITLE,
    // components: 'src/components/**/[A-Z]*.vue',
    // defaultExample: true,
    sections: [
        {
            name: 'Components',
            description: "Answer Components.",
            sections: [
                { name: "Canvas", components: "./src/components/Canvas/*.vue" },
                { name: "Combobox", components: "./src/components/Combobox/*.vue" },
                { name: "Component", components: "./src/components/Component/*.vue" },
                { name: "Console", components: "./src/components/Console/*.vue" },
                { name: "Dashboard", components: "./src/components/Dashboard/*.vue" },
                { name: "Dialog", components: "./src/components/Dialog/*.vue" },
                { name: "Drawer", components: "./src/components/Drawer/*.vue" },
                { name: "Dropbox", components: "./src/components/Dropbox/*.vue" },
                { name: "Form", components: "./src/components/Form/*.vue" },
                { name: "Icons", components: "./src/components/Icons/*.vue" },
                { name: "Image", components: "./src/components/Image/*.vue" },
                { name: "Input", components: "./src/components/Input/*.vue" },
                { name: "LambdaWidget", components: "./src/components/LambdaWidget/*.vue" },
                { name: "List", components: "./src/components/List/*.vue" },
                { name: "Picker", components: "./src/components/Picker/*.vue" },
                { name: "Progress", components: "./src/components/Progress/*.vue" },
                { name: "Setting", components: "./src/components/Setting/*.vue" },
                { name: "Storage", components: "./src/components/Storage/*.vue" },
                { name: "Table", components: "./src/components/Table/*.vue" },
                { name: "Text", components: "./src/components/Text/*.vue" },
                { name: "Timer", components: "./src/components/Timer/*.vue" },
                { name: "Titlebar", components: "./src/components/Titlebar/*.vue" },
                { name: "Video", components: "./src/components/Video/*.vue" },
                { name: "VisualGraph", components: "./src/components/VisualGraph/*.vue" },
                { name: "Graph", components: "./src/components/Graph/*.vue" },
            ]
        },
        {
            name: 'Widgets',
            description: "Answer Widgets.",
            components: "./src/widgets/*.vue"
        }
    ],
    // webpackConfig: {
    //   // custom config goes here
    // },
    exampleMode: 'expand'
}
