const db_ip = "http://127.0.0.1";
// const db_ip = "http://172.17.0.2"
const portNumber = 5984;

module.exports = {
    entry: __dirname + "/react-front-end/src/index.js",
    output: {
        path: __dirname + '/react-front-end/dist',
        filename: 'bundle.js'
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: "babel-loader"
                }
            },
            {
                test: /\.css$/,
                use: [
                    {
                        loader: "style-loader"
                    },
                    {
                        loader: "css-loader",
                        options: {
                            modules: true,
                            importLoaders: 1,
                            localIdentName: "[name]_[local]_[hash:base64]",
                            sourceMap: true,
                            minimize: true
                        }
                    }
                ]
            }
        ]
    },
};
