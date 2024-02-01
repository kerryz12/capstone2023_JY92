module.exports = {

    devServer: {
      proxy: {
        '/time': {
          target: 'http://localhost:5000',
          changeOrigin: true,
        },
        '/heartrate': {
          target: 'http://localhost:5000',
          changeOrigin: true,
        },
        '/spo2': {
          target: 'http://localhost:5000',
          changeOrigin: true,
        },
        '/temperature': {
          target: 'http://localhost:5000',
          changeOrigin: true,
        },
      },
    },
  };