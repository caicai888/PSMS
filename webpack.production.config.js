/**
 * Created by sa on 16-12-15.
 */
var webpack = require("webpack");
var path = require("path");

module.exports = {
    entry:{
        main:path.resolve(__dirname,"main.js"),
        vendors: ['jquery']
    },
    output:{
        path:"build",
        filename:"[name].js",
        publicPath:"build/"
    },
    module:{
      loaders:[
          {test:/\.css/,loader:'style!css'},
          {test:/\.(png|jpg)$/,loader:'url-loader?limit=8192&name=img/[hash:8].[name].[ext]'},
          {test:/\.js[x]?$/,loader:'babel-loader',exclude:'/node_modules/'}
      ]
    },
    resolve:{
        extensions:['','.js','.jsx',".css"],
        alias:{

        }
    },
    externals:{
        'jquery':'window.jQuery'
    },
    devtool: 'cheap-source-map',
    plugin:[
        new webpack.optimize.UglifyJsPlugin({
            compress: {
                warnings: false
            },
            minimize: true
        }),
        new webpack.DefinePlugin({
            'process.env': {
                NODE_ENV: JSON.stringify('production')
            }
        }),//避免出现重复的模块
        new webpack.optimize.CommonsChunkPlugin('vendors', 'vendors.js')
    ]
}
