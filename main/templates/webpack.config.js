/**
 * Created by sa on 16-12-15.
 */
var webpack = require("webpack");
var path = require("path");

module.exports = {
    entry:{
        main:'./main',//path.resolve(__dirname,"main.js"),
        vendors: []
    },
    output:{
        path:"build",
        filename:"[name].js",
        publicPath:"build/"
    },
    devServer: {
        historyApiFallback: true,
        hot: true,
        inline: true,
        stats: { colors: true },
        proxy: {
            '/api/*': {
                target:"http://192.168.0.3:5100",//'http://35.161.236.80:5100',
                changeOrigin: true
            }
        }
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
            "jquery":"./node_modules/jquery/dist/jquery",
            "bootstrapJs":"./node_modules/bootstrap/dist/js/bootstrap",
        }
    },
    externals:{
        'jquery':'window.jQuery'
    },
    plugin:[
        new webpack.HotModuleReplacementPlugin(),
        new webpack.ProvidePlugin({
            $: 'jquery', //加载$全局
            jQuery: 'jquery' //加载$全局
        }),
        new webpack.optimize.CommonsChunkPlugin('vendors', 'vendors.js')
    ]
}
