const path = require('path')
const webpack = require('webpack')
const CopyPlugin = require('copy-webpack-plugin')
const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  configureWebpack: {
    resolve: {
      fallback: {
        child_process: false,
        crypto: false,
        fs: false,
        path: false,
        url: false,
        vm: false,
      },
    },
    plugins: [
      new webpack.NormalModuleReplacementPlugin(/^node:/, (resource) => {
        resource.request = resource.request.replace(/^node:/, '')
      }),
      new CopyPlugin({
        patterns: [
          {
            from: path.resolve(
              path.dirname(require.resolve('pyodide/package.json')),
              'pyodide.asm.mjs',
            ),
            to: 'pyodide/pyodide.asm.mjs',
          },
          {
            from: path.resolve(
              path.dirname(require.resolve('pyodide/package.json')),
              'pyodide.asm.wasm',
            ),
            to: 'pyodide/pyodide.asm.wasm',
          },
          {
            from: path.resolve(
              path.dirname(require.resolve('pyodide/package.json')),
              'python_stdlib.zip',
            ),
            to: 'pyodide/python_stdlib.zip',
          },
          {
            from: path.resolve(
              path.dirname(require.resolve('pyodide/package.json')),
              'pyodide-lock.json',
            ),
            to: 'pyodide/pyodide-lock.json',
          },
        ],
      }),
    ],
  },
})
